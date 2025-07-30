import asyncio
import json
import os
import random
import signal
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime
from typing import Any, Dict, Optional

import aiohttp
import requests
import zmq

from arbor.server.core.config import Settings


class InferenceManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.process = None
        self.launch_kwargs = {}
        self.last_activity = None
        self.restarting = False
        self._shutting_down = False
        self.current_model = None
        self.inference_count = 0
        self._session = None
        self.worker_urls = []
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        if self._shutting_down:
            print("\nForced exit during cleanup...")
            os._exit(1)

        print("\nReceived signal to terminate. Cleaning up...")
        self._shutting_down = True
        self.kill()
        sys.exit(0)

    def is_server_running(self):
        return self.process is not None

    def is_server_restarting(self):
        return self.restarting

    def launch(
        self,
        model: str,
        launch_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ):
        if self.is_server_running():
            print("Server is already launched.")
            return

        launch_kwargs = launch_kwargs or self.launch_kwargs

        prefixes = ["openai/", "huggingface/", "local:", "arbor:"]
        for prefix in prefixes:
            if model.startswith(prefix):
                model = model[len(prefix) :]

        retries = 0
        while retries < max_retries:
            try:
                print(
                    f"Attempt {retries + 1} of {max_retries} to launch server for model {model}"
                )
                print(
                    f"Grabbing a free port to launch an SGLang server for model {model}"
                )
                router_port = get_free_port()
                dp_worker_base_port = get_free_port()
                worker_urls_port = get_free_port()  # Get a port for worker URLs

                timeout = launch_kwargs.get("timeout", 1800)
                my_env = os.environ.copy()
                my_env["CUDA_VISIBLE_DEVICES"] = (
                    self.settings.arbor_config.inference.gpu_ids
                )
                n_gpus = self.settings.arbor_config.inference.gpu_ids.count(",") + 1
                command = f"python -m arbor.server.services.inference.sgl_router_launch_server --model-path {model} --dp-size {n_gpus} --port {router_port} --host 0.0.0.0 --disable-radix-cache --router-dp-worker-base-port {dp_worker_base_port} --worker-urls-port {worker_urls_port}"
                print(f"Running command: {command}")
                if launch_kwargs.get("max_context_length"):
                    command += (
                        f" --context-length {launch_kwargs['max_context_length']}"
                    )

                # We will manually stream & capture logs.
                process = subprocess.Popen(
                    command.replace("\\\n", " ").replace("\\", " ").split(),
                    text=True,
                    stdout=subprocess.PIPE,  # We'll read from pipe
                    stderr=subprocess.STDOUT,  # Merge stderr into stdout
                    env=my_env,
                )

                # A threading.Event to control printing after the server is ready.
                # This will store *all* lines (both before and after readiness).
                print(f"SGLang server process started with PID {process.pid}.")
                stop_printing_event = threading.Event()
                logs_buffer = []

                def _tail_process(proc, buffer, stop_event):
                    while True:
                        line = proc.stdout.readline()
                        if not line and proc.poll() is not None:
                            # Process ended and no new line
                            break
                        if line:
                            buffer.append(line)
                            # Print only if stop_event is not set
                            if not stop_event.is_set():
                                print(f"[SGLang LOG] {line}", end="")

                # Start a background thread to read from the process continuously
                thread = threading.Thread(
                    target=_tail_process,
                    args=(process, logs_buffer, stop_printing_event),
                    daemon=True,
                )
                thread.start()

                # Get worker URLs before waiting for server
                try:
                    worker_urls = get_worker_urls(worker_urls_port)
                    print(f"Received worker URLs: {worker_urls}")
                    self.worker_urls = worker_urls
                except TimeoutError as e:
                    raise Exception(f"Failed to get worker URLs: {e}")

                # Wait until the server is ready (or times out)
                base_url = f"http://localhost:{router_port}"
                try:
                    wait_for_server(base_url, timeout=timeout)
                except TimeoutError:
                    # If the server doesn't come up, we might want to kill it:
                    process.kill()
                    raise

                # Once server is ready, we tell the thread to stop printing further lines.
                stop_printing_event.set()

                # A convenience getter so the caller can see all logs so far (and future).
                def get_logs() -> str:
                    # Join them all into a single string, or you might return a list
                    return "".join(logs_buffer)

                # Let the user know server is up
                print(f"Server ready on random port {router_port}!")

                self.launch_kwargs["api_base"] = f"http://localhost:{router_port}/v1"
                self.launch_kwargs["api_key"] = "local"
                self.get_logs = get_logs
                self.process = process
                self.thread = thread
                self.current_model = model

                # If we get here, the launch was successful
                return

            except Exception as e:
                retries += 1
                print(
                    f"Failed to launch server (attempt {retries} of {max_retries}): {str(e)}"
                )
                # Clean up any failed processes
                if "process" in locals():
                    try:
                        process.kill()
                    except:
                        pass
                if retries == max_retries:
                    raise Exception(
                        f"Failed to launch server after {max_retries} attempts"
                    ) from e
                # Wait a bit before retrying
                time.sleep(min(2**retries, 30))  # Exponential backoff, max 30 seconds

    def kill(self):
        from sglang.utils import terminate_process

        if self.process is None:
            print("No running server to kill.")
            return

        process = self.process
        thread = self.thread

        # Clear references first
        self.process = None
        self.thread = None
        self.get_logs = None
        self.last_activity = None

        try:
            # Handle nested signal case
            if self._shutting_down:
                process.kill()  # Go straight to SIGKILL if we're shutting down
            else:
                terminate_process(process)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print(
                        "Process did not terminate after 10 seconds, forcing with SIGKILL..."
                    )
                    process.kill()

            process.wait(timeout=5)

            if thread and thread.is_alive():
                thread.join(timeout=5)

        except Exception as e:
            print(f"Error during cleanup: {e}")
            try:
                process.kill()  # Final attempt to kill
            except:
                pass

        print("Server killed.")

    async def run_inference(self, request_json: dict):
        model = request_json["model"]
        prefixes = ["openai/", "huggingface/", "local:", "arbor:"]
        for prefix in prefixes:
            if model.startswith(prefix):
                model = model[len(prefix) :]
        print(f"Running inference for model {model}")
        # Monkeypatch:
        if model != self.current_model:
            print(f"Model changed from {model} to {self.current_model}")
            model = self.current_model
            request_json["model"] = model

        # Update last_activity timestamp
        self.last_activity = datetime.now()

        if self.process is None or self.launch_kwargs.get("api_base") is None:
            raise RuntimeError("Server is not running. Please launch it first.")

        if self.restarting:
            while self.restarting:
                print("Inference is paused while server is restarting...")
                await asyncio.sleep(5)
            request_json["model"] = self.current_model

        url = f"{self.launch_kwargs['api_base']}/chat/completions"
        try:
            self.inference_count += 1
            session = await self._ensure_session()
            async with session.post(url, json=request_json) as response:
                content = await response.content.read()
                return json.loads(content)
        except aiohttp.ClientError as e:
            print(f"Connection error: {type(e).__name__}: {str(e)}")
            # Try to close and recreate the session on error
            if self._session:
                await self._session.close()
                self._session = None
            return None
        except json.decoder.JSONDecodeError:
            print(f"JSON Decode Error during inference: {content}")
            return {
                "error": "JSON Decode Error",
                "content": content if content else "Content is null",
            }
        except Exception as e:
            print(f"Error during inference: {e}")
            raise
        finally:
            self.inference_count -= 1

    def update_model(self, output_dir):
        print("Restarting server with new model...")
        self.restarting = True

        # Close existing session and reset inference count
        if self._session:
            # Create a new event loop if one doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Run the session closure in the event loop
            loop.run_until_complete(self._session.close())
            self._session = None
        self.inference_count = 0

        tik = time.time()
        # self.kill()
        # print("Just killed server")
        # time.sleep(5)

        # Check that output directory exists and was created successfully
        print(f"Checking that output directory {output_dir} exists")
        if not os.path.exists(output_dir):
            raise RuntimeError(
                f"Failed to save model - output directory {output_dir} does not exist"
            )

        print("Directly updating weights from disk")
        for worker_url in self.worker_urls:
            print(f"Updating weights from disk for worker {worker_url}")
            try:
                response = requests.post(
                    f"{worker_url}/update_weights_from_disk",
                    json={"model_path": output_dir},
                )
                response_json = response.json()
                print(f"Response from update_weights_from_disk: {response_json}")
                # TODO: Check that the response is successful
            except Exception as e:
                print(f"Error during update_weights_from_disk: {e}")
                print(f"Full error during update_weights_from_disk: {str(e)}")
                if hasattr(e, "response") and e.response is not None:
                    print(f"Response status code: {e.response.status_code}")
                    print(f"Response text: {e.response.text}")
        self.current_model = output_dir

        # print("Launching new server")
        # self.launch(output_dir, self.launch_kwargs)
        tok = time.time()
        self.restarting = False
        print(f"Time taken to update model: {tok - tik} seconds")

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(
                total=None
            )  # No timeout...If it hangs, this might be the issue.
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session


def get_free_port() -> int:
    """
    Return a free TCP port on localhost.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


def wait_for_server(base_url: str, timeout: int = None) -> None:
    """
    Wait for the server to be ready by polling the /v1/models endpoint.

    Args:
        base_url: The base URL of the server (e.g. http://localhost:1234)
        timeout: Maximum time to wait in seconds. None means wait forever.
    """
    start_time = time.time()
    while True:
        try:
            response = requests.get(
                f"{base_url}/v1/models",
                headers={"Authorization": "Bearer None"},
            )
            if response.status_code == 200:
                # A small extra sleep to ensure server is fully up.
                time.sleep(5)
                break

            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError("Server did not become ready within timeout period")
        except requests.exceptions.RequestException:
            # Server not up yet, wait and retry
            time.sleep(1)


def get_worker_urls(zmq_port: int, timeout: float = 30.0) -> list:
    print(f"Attempting to get worker URLs on port {zmq_port} with timeout {timeout}s")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{zmq_port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    # Set a timeout for receiving
    socket.setsockopt(zmq.RCVTIMEO, int(timeout * 1000))

    try:
        print("Waiting for worker URLs message...")
        message = socket.recv_json()
        print(f"Received message: {message}")
        if message.get("type") == "worker_urls":
            return message["urls"]
        else:
            raise ValueError(f"Unexpected message type: {message.get('type')}")
    except zmq.error.Again:
        raise TimeoutError(f"Timeout waiting for worker URLs on port {zmq_port}")
    finally:
        socket.close()
        context.term()

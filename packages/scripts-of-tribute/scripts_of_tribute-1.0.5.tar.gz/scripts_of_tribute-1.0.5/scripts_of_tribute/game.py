import atexit
import multiprocessing

import os
import platform
import requests
import zipfile
import stat
from pathlib import Path
import signal
import time
from typing import List
from scripts_of_tribute.base_ai import BaseAI
from scripts_of_tribute.runner import run_game_runner
from scripts_of_tribute.server import run_grpc_server

class Game:
    def __init__(self):
        self.bots: List[BaseAI] = []
        self.processes: List[multiprocessing.Process] = []

        atexit.register(self._cleanup_processes)

    def register_bot(self, bot_instance: BaseAI):
        # We register bots here, because some run invokes might involve C# native bots, so we always pass str there
        self.bots.append(bot_instance)

    def run(
        self,
        bot1Name: str,
        bot2Name: str,
        start_game_runner=True,
        runs=1,
        threads=1,
        enable_logs="NONE",
        log_destination="",
        seed=None,
        timeout=30,
        base_client_port=50000,
        base_server_port=49000
    ):
        bot1 = next((bot for bot in self.bots if bot.bot_name == bot1Name), None)
        bot2 = next((bot for bot in self.bots if bot.bot_name == bot2Name), None)
        self.processes = []
        if bot1 is not None or bot2 is not None:
            self.processes.extend(self._run_bot_instances(bot1, bot2, threads, base_client_port, base_server_port))
        if start_game_runner:
            game_runner_dir = Path.home() / ".scripts_of_tribute" / "GameRunner"
            try:
                executable_path = self._find_executable(game_runner_dir)
            except FileNotFoundError:
                print("GameRunner not found. Downloading...")
                game_runner_dir = self._download_game_runner()
                executable_path = self._find_executable(game_runner_dir)

            if any([bot1Name == bot.bot_name for bot in self.bots]):
                bot1Name = "grpc:" + bot1Name
            if any([bot2Name == bot.bot_name for bot in self.bots]):
                bot2Name = "grpc:" + bot2Name
            time.sleep(5) # give servers some time to start
            # game_runner_process = multiprocessing.Process(
            #     target=run_game_runner,
            #     name='GameRunner',
            #     args=(executable_path, bot1Name, bot2Name, runs, threads, enable_logs, log_destination, seed, timeout),
            #     #daemon=True
            # )
            run_game_runner(executable_path, bot1Name, bot2Name, runs, threads, enable_logs, log_destination, seed, timeout)
        try:
            for p in self.processes:
                p.join()  # Wait for all processes to finish
        except KeyboardInterrupt:
            print("Server interrupted by user.")
            for p in self.processes:
                p.terminate()  # Terminate all processes on interruption

    def _run_bot_instances(
        self,
        bot1: BaseAI | None,
        bot2: BaseAI | None,
        num_threads: int,
        base_client_port: int,
        base_server_port: int,
    ):
        processes = []
        for i in range(num_threads):
            client_port1 = base_client_port + i
            server_port1 = base_server_port + i
            client_port2 = base_client_port + num_threads + i
            server_port2 = base_server_port + num_threads + i

            p = multiprocessing.Process(
                target=run_grpc_server,
                name=f"{bot1.bot_name if bot1 else 'C# bot'} - {bot2.bot_name if bot2 else 'C# bot'} on {(client_port1, client_port2)}, {(server_port1, server_port2)}",
                args=(bot1, bot2, (client_port1, client_port2), (server_port1, server_port2)),
                #daemon=True
            )
            p.start()
            processes.append(p)

        return processes


    def _cleanup_processes(self):
        print("Cleaning up all processes...")

        for p in self.processes:
            if p.is_alive():
                print(f"Terminating {p.name} (PID {p.pid})")
                p.terminate()
                p.join(timeout=5)
                
                if p.is_alive():
                    print(f"Forcing kill on {p.name} (PID {p.pid})")
                    os.kill(p.pid, signal.SIGKILL)

        self.processes.clear()

    def _download_game_runner(self, version=None):
        system = platform.system()
        if system == "Windows":
            zip_name = f"GameRunner-win-x64.zip"
        elif system == "Linux":
            zip_name = f"GameRunner-linux-x64.zip"
        elif system == "Darwin":  # macOS
            zip_name = f"GameRunner-osx-x64.zip"
        else:
            raise NotImplementedError(f"Unsupported platform: {system}")
        
        if version is None:
            print("Fetching latest GameRunner version...")
            response = requests.get("https://api.github.com/repos/ScriptsOfTribute/ScriptsOfTribute-Core/releases/latest")
            response.raise_for_status()
            version = response.json()["tag_name"]
            print(f"Latest version: {version}")

        url = f"https://github.com/ScriptsOfTribute/ScriptsOfTribute-Core/releases/download/{version}/{zip_name}"

        target_dir = Path.home() / ".scripts_of_tribute" / "GameRunner"
        target_dir.mkdir(parents=True, exist_ok=True)

        zip_path = target_dir / zip_name

        print(f"Downloading GameRunner from {url}...")
        response = requests.get(url)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            f.write(response.content)

        print(f"Extracting GameRunner to {target_dir}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_dir)

        os.remove(zip_path)

        print(f"GameRunner downloaded and extracted to {target_dir}")
        return target_dir

    def _find_executable(self, directory):
        system = platform.system()
        if system == "Windows":
            executable_name = "GameRunner.exe"
        elif system == "Linux":
            executable_name = "GameRunner"
        elif system == "Darwin":
            executable_name = "GameRunner"
        else:
            raise NotImplementedError(f"Unsupported platform: {system}")

        for root, _, files in os.walk(directory):
            if executable_name in files:
                executable_path = Path(root) / executable_name
                # Make the executable executable (Linux/macOS)
                if system != "Windows":
                    st = os.stat(executable_path)
                    os.chmod(executable_path, st.st_mode | stat.S_IEXEC)
                return executable_path

        raise FileNotFoundError(f"Could not find {executable_name} in {directory}")
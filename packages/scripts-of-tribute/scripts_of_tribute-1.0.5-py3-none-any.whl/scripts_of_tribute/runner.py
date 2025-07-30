from pathlib import Path
import subprocess

def run_game_runner(path: Path, bot1: str, bot2: str, runs=1, threads=1, enable_logs="NONE", log_destination="", seed=None, timeout=30):
    args = [path, bot1, bot2]
    args += ["-n", str(runs)]
    args += ["-t", str(threads)]
    args += ["-l", enable_logs]
    if log_destination:
        args += ["-d", log_destination]
    if seed:
        args += ["-s", str(seed)]
    args += ["-to", str(timeout)]
    try:
        result = subprocess.run(
            args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(path.parent)
        )
        print(f"{result.stdout}")
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running GameRunner:\n{e.stderr}")
        raise RuntimeError(e)


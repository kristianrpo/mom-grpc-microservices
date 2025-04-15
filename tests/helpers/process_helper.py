# service_helpers.py
import subprocess
import os
import signal
import time

def start_process(script_name, cwd_path, wait=2):
    """
    Start a process given its script name and working directory.
    :param script_name: Name of the script to run.
    :param cwd_path: Path to the directory where the script is located.
    :param wait: Time to wait for the process to start (default is 2 seconds).
    :return: The process object.
    """
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("..")

    proc = subprocess.Popen(
        ["python3", script_name],
        cwd=os.path.abspath(os.path.join("..", cwd_path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )
    time.sleep(wait)
    return proc

def stop_process(proc):
    """
    Stop a process given its process object.
    :param proc: The process object.
    """
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    time.sleep(1)
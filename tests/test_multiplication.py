from helpers.process_helper import start_process, stop_process
from helpers.command_helper import build_submit_command
import os
import ast
import subprocess
import json
import re
import time

def test_inmediate_response():
    """
    Should return the result of the multiplication service immediately when it is running.
    """
    proc = start_process("multiplication_service.py", "micro_services/micro_service_multiplication")
    
    try:
        cmd = build_submit_command("test_client", "MultiplicationService", 1, 2)
        result = subprocess.run(cmd, cwd="../client", capture_output=True, text=True)

        match = re.search(r'Immediate response received: (.*)', result.stdout)
        assert match, "❌ The expected response was not found"

        data = json.loads(match.group(1))
        
        assert data["status"] == "COMPLETED", f"❌ Expected status is COMPLETED, but got {data['status']}"
        assert data["product"] == 2.0, f"❌ Expected product is 2.0, but got {data['product']}"
        print(f"✅ Test passed with status {data['status']} and product {data['product']}")
    
    finally:
        stop_process(proc)


def test_delayed_response_from_queue():
    """
    Should process the enqueued task and return the result when the service starts after submission.
    """
    cmd = build_submit_command("test_client", "MultiplicationService", 1, 2)
    proc_client = subprocess.Popen(cmd, cwd="../client", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    time.sleep(5)

    proc_service = start_process("multiplication_service.py", "micro_services/micro_service_multiplication")

    try:
        stdout, stderr = proc_client.communicate(timeout=30)
        match = re.search(r"received: (.*)", stdout)
        if match:
            response_str = match.group(1)
            outer_response = ast.literal_eval(response_str)
            inner_response = json.loads(outer_response["response"])
            data = json.loads(inner_response)
            assert data["status"] == "COMPLETED", f"❌ Expected status is COMPLETED, but got {data['status']}"
            assert data["result"] == 2.0, f"❌ Expected product is 2.0, but got {data['result']}"

        print(f"✅ Test passed with product {data['result']} and status {data['status']}")

    finally:
        stop_process(proc_service)


def test_timeout_when_service_never_starts():
    """
    Should allow inspection after killing the client that didn't respond in time.
    """
    cmd = build_submit_command("test_client", "MultiplicationService", 1, 2)
    proc_client = subprocess.Popen(cmd, cwd="../client", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)

    time.sleep(32)
    stop_process(proc_client)
    stdout, stderr = proc_client.communicate()
    assert "timeout reached" in stdout.lower(), "❌ Timeout not detected as expected"
    assert "no response received" in stdout.lower(), "❌ Expected 'no response received' message"

    print("✅ Timeout behavior verified correctly when service is inactive.")
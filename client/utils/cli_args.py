import argparse

def parse_client_args():
    """
    Retrive the client ID and service name from command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True, help="Client ID")
    parser.add_argument("--service", required=True, help="Service name")
    args = parser.parse_args()
    return args
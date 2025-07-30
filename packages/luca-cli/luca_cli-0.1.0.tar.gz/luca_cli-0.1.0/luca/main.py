"""Main file for the client."""

import json
import os
import requests
import sys

CLIENT_KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".luca")
LOCAL_KB_PATH = os.path.join(CLIENT_KB_DIR, "kb.txt")

SERVER_URL = "http://45.33.41.244:8000"

def ensure_kb_dir():
    """Ensure the client's KB directory exists."""
    if not os.path.exists(CLIENT_KB_DIR):
        os.makedirs(CLIENT_KB_DIR)


def sync_kb():
    """Sync the knowledge base from the server."""
    ensure_kb_dir()
    response = requests.get(f"{SERVER_URL}/kb")
    response.raise_for_status()
    with open(LOCAL_KB_PATH, "w") as f:
        f.write(json.loads(response.content)["text"])


def update_kb(content: str):
    """Update the knowledge base."""
    kb_text = json.loads(content)["text"]
    with open(LOCAL_KB_PATH, "w") as f:
        f.write(kb_text)


def init():
    """Initialize the client and the server."""
    print("Initializing the client...")
    request_params = {
        "WANDB_API_KEY": None,
        "WANDB_ENTITY": None
    }
    try:
        response = requests.post(f"{SERVER_URL}/init", json=request_params)
        response.raise_for_status()
        update_kb(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error initializing server: {e}")


def main(argv):
    """Main function."""
    if len(argv) == 1:
        print("Usage: luca <command> or luca <prompt>")
        print("Commands:")
        print("  init: Initialize the client and the server.\n")
        print("Examples:")
        print("  luca init")
        print("  luca 'Research papers on reinforcement learning.'")
        return
    if argv[1] == "init":
        init()
    else:
        # User query
        prompt = argv[1]
        response = requests.post(f"{SERVER_URL}/query", json={"prompt": prompt})
        response.raise_for_status()
        print(json.loads(response.content)["text"])
        

def entrypoint():
    """Entry point for the CLI tool."""
    main(sys.argv)


if __name__ == "__main__":
    entrypoint()

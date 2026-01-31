import threading
import time
from typing import Generator
import pytest
import requests
from werkzeug.serving import make_server

@pytest.fixture(scope="session")
def base_url() -> Generator[str, None, None]:
    from app.api import app
    server = make_server("127.0.0.1", 0, app)

    class ServerThread(threading.Thread):
        def __init__(self):
            super().__init__(daemon=True)
        def run(self):
            server.serve_forever()

    thread = ServerThread()
    thread.start()
    host, port = server.server_address
    url = f"http://{host}:{port}"

    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            r = requests.get(f"{url}/api/accounts", timeout=0.5)
            if r.status_code in (200, 404):
                break
        except Exception:
            time.sleep(0.05)

    yield url
    server.shutdown()
    thread.join(timeout=2)

@pytest.fixture(autouse=True)
def cleanup_registry(base_url: str) -> Generator[None, None, None]:
    _delete_all_accounts(base_url)
    yield
    _delete_all_accounts(base_url)

def _delete_all_accounts(base_url: str) -> None:
    try:
        resp = requests.get(f"{base_url}/api/accounts", timeout=2)
        if resp.status_code != 200:
            return
        for acc in resp.json():
            pesel = acc.get("pesel")
            if pesel:
                requests.delete(f"{base_url}/api/accounts/{pesel}", timeout=2)
    except Exception:
        pass

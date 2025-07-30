import requests

BASE_URL = "http://127.0.0.1:8600"
AGENT_ID = "test-agent-123"
CONTAINER_FILE_PATH = "/etc/hostname"
CONTAINER_FOLDER_PATH = "/etc"
LOCAL_ARCHIVE_PATH = "./etc_folder.tar"

def test_create_session():
    print("Creating session...")
    resp = requests.post(f"{BASE_URL}/session/create", json={"agent_id": AGENT_ID})
    print(resp.json())

def test_run_command():
    print("Running command...")
    payload = {
        "agent_id": AGENT_ID,
        "command": ["echo", "Hello, World!"]
    }
    resp = requests.post(f"{BASE_URL}/command/run", json=payload)
    print(resp.json())

def test_get_file():
    print("Getting file...")
    payload = {
        "agent_id": AGENT_ID,
        "path": CONTAINER_FILE_PATH
    }
    resp = requests.post(f"{BASE_URL}/file/get", json=payload)
    print(resp.json())

def test_get_folder():
    print("Getting folder...")
    payload = {
        "agent_id": AGENT_ID,
        "container_path": CONTAINER_FOLDER_PATH,
        "local_path": LOCAL_ARCHIVE_PATH
    }
    resp = requests.post(f"{BASE_URL}/folder/get", json=payload)
    print(resp.json())

def test_download_folder():
    print("Downloading folder archive...")
    resp = requests.get(f"{BASE_URL}/folder/download", params={"local_path": LOCAL_ARCHIVE_PATH})
    if resp.status_code == 200:
        with open("downloaded_folder.tar", "wb") as f:
            f.write(resp.content)
        print("Folder downloaded successfully as downloaded_folder.tar")
    else:
        print("Failed to download folder:", resp.json())

def test_stop_session():
    print("Stopping session...")
    resp = requests.post(f"{BASE_URL}/session/stop", json={"agent_id": AGENT_ID})
    print(resp.json())

if __name__ == "__main__":
    test_create_session()
    test_run_command()
    test_get_file()
    test_get_folder()
    test_download_folder()
    test_stop_session()

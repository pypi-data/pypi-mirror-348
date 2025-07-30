import psutil
import time
import os
import uuid
import requests
from . import config

def get_status(model):
    return {
        "device_id": get_device_id(),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent
        # "hostname": socket.gethostname(),
        # "os": platform.system(),
        # "os_version": platform.version(),
        # "disk_usage": f"{psutil.disk_usage('/').percent}%",
        # "uptime_seconds": int(time.time() - psutil.boot_time()),
        # "model": get_model_metadata(model)
    }

def get_model_metadata(model):
    return {
        "type": str(model.__class__.__name__),
        "framework": "pytorch",  # or detect dynamically later
        "version": getattr(model, '__version__', "1.0.0"),  # customizable
        "hash": "fake_hash_123abc"  # placeholder for checksum or git SHA
    }

def get_device_id():
    if os.path.exists(config.DEVICE_ID_FILE):
        with open(config.DEVICE_ID_FILE, 'r') as f:
            return f.read().strip()
    else:
        new_id = str(uuid.uuid4())
        with open(config.DEVICE_ID_FILE, 'w') as f:
            f.write(new_id)
        return new_id

def post_status(model):
    status = get_status(model)
    try:
        url = config.BACKEND_URL.rstrip('/') + '/status'
        response = requests.post(url, json=status)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

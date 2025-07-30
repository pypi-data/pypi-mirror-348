import os
import psutil

def collect_container():
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_usage": psutil.virtual_memory().used,
        "container_id": os.getenv("HOSTNAME", "unknown"),
        "file_exists": {},
        "mounts": [],
    }

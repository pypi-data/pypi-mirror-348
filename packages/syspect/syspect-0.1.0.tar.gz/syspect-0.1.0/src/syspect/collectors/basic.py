# import psutil
# import os

# def collect_data():
#     return {
#         "cpu_percent": psutil.cpu_percent(interval=0.5),
#         "mounts": [mnt.mountpoint for mnt in psutil.disk_partitions()],
#         "file_exists": {
#             "/etc/myapp/config.yml": os.path.exists("/etc/myapp/config.yml"),
#             "/etc/myapp/credentials": os.path.exists("/etc/myapp/credentials"),
#         }
#     }

def collect_basic():
    return {
        "cpu_percent": 92,
        "file_exists": {
            "/etc/myapp/config.yml": True,
            "/etc/myapp/credentials": True,
        },
        "mounts": ["/mnt/data", "/mnt/stale_backup"],
    }
def collect_web(requests_served=0, error_count=0, config={}):
    return {
        "web_requests": requests_served,
        "web_error_count": error_count,
        "config_loaded": config,
        "file_exists": {},
    }

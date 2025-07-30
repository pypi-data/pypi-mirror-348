from syspect.rules.missing_config import check_config_files

def test_check_config_files_pass():
    ctx = {
        "file_exists": {
            "/etc/myapp/config.yml": True,
            "/etc/myapp/credentials": True
        }
    }
    result = check_config_files(ctx)
    assert result["severity"] in ("info", "ok")

def test_check_config_files_fail():
    ctx = {
        "file_exists": {
            "/etc/myapp/config.yml": False,
            "/etc/myapp/credentials": False
        }
    }
    result = check_config_files(ctx)
    assert "Missing config files" in result["summary"]
    assert result["severity"] == "critical"

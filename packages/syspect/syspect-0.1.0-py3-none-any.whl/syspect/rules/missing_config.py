from syspect.rule_registry import rule

@rule
def check_config_files(data):
    missing = []
    for path in ["/etc/myapp/config.yml", "/etc/myapp/credentials"]:
        if not data.get('file_exists', {}).get(path):
            missing.append(path)

    if missing:
        return {
            "id": "MISSING_CONFIG",
            "summary": f"Missing config files: {', '.join(missing)}",
            "severity": "critical"
        }
    else:
        # Explicitly return an OK/info dictionary if no issue found
        return {
            "id": "CONFIG_OK",
            "summary": "All required config files are present.",
            "severity": "info"
        }

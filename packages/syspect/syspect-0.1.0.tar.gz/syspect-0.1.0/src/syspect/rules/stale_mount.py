from syspect.rule_registry import rule

@rule
def detect_stale_mount(data):
    mounts = data.get('mounts', [])
    for mount in mounts:
        if 'stale' in mount.lower():
            return {
                "id": "STALE_MOUNT",
                "summary": f"Stale mount detected: {mount}",
                "severity": "error"
            }
        else:
            # Explicitly return an OK/info dictionary if no issue found
            return {
                "id": "MOUNT_OK",
                "summary": "No stale mounts detected.",
                "severity": "info"
            }

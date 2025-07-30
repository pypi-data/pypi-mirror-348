from syspect.engine import run_diagnostic
from syspect.insights import Insight

# Test Scenario 1: High CPU usage
context_1 = {
    "cpu_percent": 92,
    "file_exists": {
        "/etc/myapp/config.yml": True,
        "/etc/myapp/credentials": True
    },
    "mounts": []
}

# Test Scenario 2: Missing config files
context_2 = {
    "cpu_percent": 45,
    "file_exists": {
        "/etc/myapp/config.yml": False,
        "/etc/myapp/credentials": False
    },
    "mounts": []
}

# Test Scenario 3: Stale mount
context_3 = {
    "cpu_percent": 10,
    "file_exists": {
        "/etc/myapp/config.yml": True,
        "/etc/myapp/credentials": True
    },
    "mounts": ["/mnt/data", "stale_mount"]
}

# Combine all for a rich demo
scenarios = {
    "High CPU": context_1,
    "Missing Configs": context_2,
    "Stale Mount": context_3,
}

for name, ctx in scenarios.items():
    print(f"\n=== Scenario: {name} ===")
    results = run_diagnostic(ctx, verbose=True)

    for res in results:
        if res.success and res.insight:
            insight = res.insight
            # insight is an Insight object here
            sev = insight.severity.upper() if hasattr(insight, "severity") else "INFO"
            summary = getattr(insight, "summary", None)
            if not summary and hasattr(insight, "title"):
                summary = insight.title
            if not summary:
                summary = str(insight)
            print(f"[{sev}] {summary}")
        elif res.error:
            print(f"[ERROR] Rule '{res.rule}' failed: {res.error}")
        else:
            print(f"[OK] Rule '{res.rule}' passed with no issues.")

from syspect.rule_registry import rule

@rule
def high_cpu_usage(data):
    cpu_percent = data.get('cpu_percent')
    if cpu_percent and cpu_percent > 85:
        return {
            "id": "HIGH_CPU",
            "summary": f"High CPU usage: {cpu_percent}%",
            "severity": "warning"
        }
    else:
        # Explicitly return an OK/info dictionary if no issue found
        return {
            "id": "CPU_OK",
            "summary": "CPU usage is within normal range.",
            "severity": "info"
        }

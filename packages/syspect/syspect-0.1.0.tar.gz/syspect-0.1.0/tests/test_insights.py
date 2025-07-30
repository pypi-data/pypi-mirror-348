from syspect.insights import Insight, Severity

i = Insight(
    id="cpu.high",
    title="High CPU Usage",
    description="CPU usage is over 90% for the last 5 minutes.",
    severity=Severity.CRITICAL,
    metadata={"cpu_percent": "93.5"}
)

print(i)
print(i.to_dict())

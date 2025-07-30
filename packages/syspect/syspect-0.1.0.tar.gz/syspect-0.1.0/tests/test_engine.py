from syspect.engine import run_diagnostic
from syspect.insights import Result, Insight

def test_run_diagnostic_basic():
    context = {
        "cpu_percent": 50,
        "file_exists": {
            "/etc/myapp/config.yml": True,
            "/etc/myapp/credentials": True,
        },
        "mounts": []
    }
    results = run_diagnostic(context)
    assert isinstance(results, list)
    assert all(isinstance(r, (Result, Insight)) for r in results)

    for res in results:
        if isinstance(res, Result):
            assert hasattr(res, "rule")
            assert hasattr(res, "success")
        elif isinstance(res, Insight):
            assert hasattr(res, "id")
            assert hasattr(res, "title")
            assert hasattr(res, "severity")

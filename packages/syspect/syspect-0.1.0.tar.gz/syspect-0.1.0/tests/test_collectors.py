from syspect.collectors import collect_data


def test_basic_collector():
    data = collect_data(mode="basic")
    assert "cpu_percent" in data
    assert "file_exists" in data


def test_container_collector():
    data = collect_data(mode="container")
    assert "cpu_percent" in data
    assert "memory_usage" in data
    assert "container_id" in data


def test_web_collector():
    data = collect_data(mode="web", requests_served=1000, error_count=5)
    assert data["web_requests"] == 1000
    assert data["web_error_count"] == 5


def test_custom_collector():
    def fake_collector(**kwargs):
        return {"custom_key": 42}

    data = collect_data(mode="custom", collector=fake_collector)
    assert data["custom_key"] == 42

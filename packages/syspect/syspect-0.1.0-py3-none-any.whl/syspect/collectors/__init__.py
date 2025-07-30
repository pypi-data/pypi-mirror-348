# syspect/collectors/__init__.py

from syspect.collectors.basic import collect_basic
from syspect.collectors.container import collect_container
from syspect.collectors.web import collect_web

def collect_data(mode: str = "basic", **kwargs):
    if mode == "basic":
        return collect_basic()
    elif mode == "container":
        return collect_container(**kwargs)
    elif mode == "web":
        return collect_web(**kwargs)
    elif mode == "custom":
        # Accept user-provided callable as `collector` in kwargs
        collector = kwargs.get("collector")
        if callable(collector):
            return collector(**kwargs)
        raise ValueError("For mode='custom', provide a callable `collector`.")
    else:
        raise ValueError(f"Unsupported mode: {mode}")

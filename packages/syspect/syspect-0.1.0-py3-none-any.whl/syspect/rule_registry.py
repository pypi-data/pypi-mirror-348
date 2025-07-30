import functools

registered_rules = []

def rule(func):
    """Decorator to register a diagnostic rule."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    wrapper._is_syspect_rule = True
    registered_rules.append(wrapper)
    return wrapper

def get_registered_rules():
    return registered_rules

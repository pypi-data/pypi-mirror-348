from importlib.util import spec_from_file_location, module_from_spec

def load_custom_rules(path: str):
    from syspect.rule_registry import get_registered_rules

    spec = spec_from_file_location("custom_rules", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get rules with _is_syspect_rule and only register those that are not already present
    custom_rules = [
        func for name, func in vars(module).items()
        if callable(func) and getattr(func, "_is_syspect_rule", False)
    ]

    if not custom_rules:
        raise ValueError(f"No @rule-decorated functions found in {path}")

    # Remove duplicates based on function identity
    unique_custom_rules = list({id(r): r for r in custom_rules}.values())

    return unique_custom_rules

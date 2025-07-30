from syspect.rule_registry import get_registered_rules
import traceback
from typing import Callable, List, Dict, Any, Union, Optional
from syspect.insights import Result, Insight, Severity

SystemContext = Dict[str, Any]  # Represents gathered system metadata
Rule = Callable[[SystemContext], Union[Result, dict]]  # Allows dict or Result return


class RuleEngine:
    def __init__(self):
        self.rules: List[Rule] = []

    def register(self, rule: Rule):
        """Register a rule with the engine."""
        if rule not in self.rules:
            self.rules.append(rule)

    def _normalize_result(self, raw: Union[Result, dict], rule_name: str) -> Result:
        if isinstance(raw, Result):
            return raw
        elif isinstance(raw, dict):
            # Safely create Insight from dict
            id_ = raw.get("id", rule_name)
            summary = raw.get("summary", "")
            severity_str = raw.get("severity", "info")
            try:
                severity = Severity(severity_str.lower())
            except ValueError:
                severity = Severity.INFO
            insight = Insight(
                id=id_,
                title=summary,
                description=raw.get("description", summary),
                severity=severity,
                metadata=raw.get("metadata", {}),
            )
            return Result(
                rule=rule_name,
                success=True,
                insight=insight,
                error=None,
            )
        else:
            # Unexpected return type from rule
            return Result(
                rule=rule_name,
                success=False,
                insight=None,
                error=f"Rule returned unsupported type: {type(raw)}",
            )

    def run(self, context: SystemContext) -> List[Insight]:
        """Run all rules and collect successful insights only."""
        insights = []
        for rule in self.rules:
            try:
                raw = rule(context)
                res = self._normalize_result(raw, rule.__name__)
                if res.success and res.insight:
                    insights.append(res.insight)
            except Exception as e:
                print(f"Error in rule {rule.__name__}: {e}")
                traceback.print_exc()
        return insights

    def run_verbose(self, context: SystemContext) -> List[Result]:
        """Run all rules and return verbose result, including errors."""
        results = []
        for rule in self.rules:
            try:
                raw = rule(context)
                res = self._normalize_result(raw, rule.__name__)
                results.append(res)
            except Exception as e:
                results.append(Result(
                    rule=rule.__name__,
                    success=False,
                    insight=None,
                    error=str(e),
                ))
        return results


def load_default_rules(engine: RuleEngine):
    """Load all rules registered via the @rule decorator."""
    for r in get_registered_rules():
        engine.register(r)


def run_diagnostic(
    context: SystemContext,
    verbose: bool = False,
    custom_rules: Optional[List[Rule]] = None,
    load_defaults: bool = True
) -> List[Union[Result, Insight]]:
    import syspect.rules  # Ensures all @rule decorators are triggered

    print('[*] Initializing rule engine...')
    engine = RuleEngine()

    if load_defaults:
        print('[*] Loading default registered rules...')
        load_default_rules(engine)

    if custom_rules:
        print(f'[*] Registering {len(custom_rules)} custom rules...')
        for rule in custom_rules:
            engine.register(rule)

    if verbose:
        return engine.run_verbose(context)
    else:
        return engine.run(context)


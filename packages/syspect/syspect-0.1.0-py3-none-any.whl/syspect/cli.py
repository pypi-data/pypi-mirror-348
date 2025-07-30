import json
import click
from syspect.collectors import collect_data
from syspect.engine import run_diagnostic
from syspect.utils.custom_loader import load_custom_rules
from syspect.insights import Result, Insight
from dataclasses import asdict
import syspect.rules  # Ensure rules are registered


@click.command()
@click.option('--json', 'as_json', is_flag=True, help='Output results in JSON format.')
@click.option('--all', 'show_all', is_flag=True, help='Show all rules including passed ones.')
@click.option('--summary', is_flag=True, help='Only show summary of results.')
@click.option('--rules', is_flag=True, help='List all registered rules and exit.')
@click.option('--output', type=click.Path(), help='Write output to a file.')
@click.option('--verbose/--no-verbose', default=True, help='Enable or disable verbose rule execution.')
@click.option('--custom-rule', type=click.Path(exists=True), help="Path to Python file containing custom rule(s).")
def main(as_json, show_all, summary, rules, output, verbose, custom_rule):
    """Run diagnostics using syspect rules."""

    if rules:
        from syspect.rule_registry import get_registered_rules
        output_lines = ["[*] Available Rules:\n"]
        for rule in get_registered_rules():
            output_lines.append(f"- {rule.__name__} : {rule.__doc__ or 'No description'}")
        content = "\n".join(output_lines)
        print(content)
        if output:
            with open(output, "w") as f:
                f.write(content + "\n")
        return

    print("[*] Collecting system data...")
    context = collect_data(mode="basic")

    custom_rules = []
    if custom_rule:
        print(f"[*] Loading custom rules from: {custom_rule}")
        custom_rules = load_custom_rules(custom_rule)
        print(f"[*] Registered {len(custom_rules)} custom rule(s).")

    print("[*] Running diagnostics...\n")
    results = run_diagnostic(context, verbose=verbose, custom_rules=custom_rules)

    if summary:
        total = len(results)
        if verbose:
            passed = len([r for r in results if r.success and not r.insight])
            failed = len([r for r in results if r.error])
            insights_count = len([r for r in results if r.insight])
        else:
            # Non-verbose: results are Insight only
            passed = 0  # no Result objects
            failed = 0
            insights_count = len(results)

        summary_text = (
            f"Total Rules: {total}, Passed: {passed}, "
            f"Errors: {failed}, Insights: {insights_count}"
        )
        print(summary_text)
        if output:
            with open(output, "w") as f:
                f.write(summary_text + "\n")
        return

    output_lines = []

    if as_json:
        # Convert dataclasses to dicts for JSON serialization
        def serialize_result(r):
            if isinstance(r, Result):
                d = asdict(r)
                if r.insight:
                    d['insight'] = asdict(r.insight)
                return d
            elif isinstance(r, Insight):
                return asdict(r)
            else:
                return str(r)

        output_content = json.dumps([serialize_result(r) for r in results], indent=2)
        print(output_content)
        if output:
            with open(output, "w") as f:
                f.write(output_content + "\n")
        return
    else:
        for res in results:
            if isinstance(res, Result):
                if res.success and res.insight:
                    sev = res.insight.severity.value.upper()
                    line = f"[{sev}] {res.insight.title} - {res.insight.description}"
                elif res.error:
                    line = f"[ERROR] Rule '{res.rule}' failed: {res.error}"
                elif show_all:
                    line = f"[OK] Rule '{res.rule}' passed with no issues."
                else:
                    continue
            elif isinstance(res, Insight):
                sev = res.severity.value.upper()
                line = f"[{sev}] {res.title} - {res.description}"
            else:
                # Unknown type, fallback string
                line = str(res)

            print(line)
            output_lines.append(line)

        if output:
            with open(output, "w") as f:
                f.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    main()

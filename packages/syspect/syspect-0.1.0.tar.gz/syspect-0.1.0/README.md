# Syspect – A Lightweight Rule Engine for Self-Diagnosing Python Apps

**Syspect** is a modular diagnostic engine designed to bring observability and self-awareness to Python applications. It offers a flexible, rule-based system that evaluates runtime context to provide actionable diagnostics — whether you're running a CLI tool, web service, system daemon, or containerized app.

At its core is a lightweight rule engine that processes system or application context through built-in or custom diagnostic rules, delivering structured insights in formats like JSON, plain text, or logs.

---

## Features

- **Rule-Based Diagnostics**  
  Define rules with a simple `@rule` decorator including metadata like severity, summary, and insight details.

- **Pluggable Collectors**  
  Collect system context from various layers — system state, containers, environments, or custom inputs.

- **Custom Rule Support**  
  Dynamically load your own diagnostic rules from Python files at runtime.

- **Versatile Execution**  
  Runs seamlessly across CLI tools, web apps, containers, and desktop or cloud environments.

- **Built-in Rules**  
  Includes core diagnostics for CPU usage, memory, mounts, and configuration files.

- **Flexible Output**  
  Choose between JSON, plain text, summaries, or file-based outputs for integration or reporting.

- **Extensible Architecture**  
  Add new collectors, rules, and output renderers with minimal overhead.

- **Minimal Dependencies**  
  Lightweight and modular by design — easy to adopt, integrate, and extend.

---

## Installation

To install for local development:

```bash
git clone https://github.com/rahulXs/syspect.git
cd syspect
pip install -e .
```

For PyPI installation:

```bash
pip install syspect
```

---

## Usage

### CLI

```bash
syspect --help
```

```bash
syspect
```
This will collect system data, run all built-in rules, and print the results to your terminal.

### CLI Options

```bash
Option	Description
--json	Output results in JSON format
--all	Show all rules, including passing checks
--summary	Display a summary only, omitting full output
--rules	List all registered rules and exit
--output <file>	Write the output to a file
--verbose / --no-verbose	Toggle detailed execution logs (default: --verbose)
--custom-rule <path>	Load custom rule file(s) and include in evaluation
```

### Python

```python
from syspect.collectors import collect_data
from syspect.engine import run_diagnostic
from syspect.insights import Result, Insight

# Collect system data
context = collect_data()

# Run diagnostics
results = run_diagnostic(context)

# Print results
```

---

### Flow Summary

1. User runs the CLI.
2. CLI calls collect_data(), generating a context dictionary.
3. CLI initializes the RuleEngine.
4. Engine dynamically loads rules via the @rule decorator registry.
5. Each rule runs against the collected context and returns:
    - A dictionary containing id, summary, and severity, or
    - A structured Result object.
6. Engine aggregates valid insights and diagnostic errors.
7. CLI outputs results to the terminal (or to JSON/file if specified).

---

### Roadmap

Planned enhancements:
- Rule discovery from external sources or plugin registries
- Rule tagging, filtering, and metadata-driven execution
- Execution DAGs (Directed Acyclic Graphs) for rule dependency resolution
- Plugin interface for third-party rule modules

---

### Contributing

Pull requests are welcome. Please open an issue first to discuss the change if it's architecture-related or non-trivial.

Please make sure to update tests as appropriate.

---

### License
Syspect is licensed under the MIT License. You are free to use, modify, and distribute it with attribution.
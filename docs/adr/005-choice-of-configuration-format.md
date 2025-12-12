# ADR-005: Choice of Configuration Format

## Status

Accepted

## Context

The project requires a way to store configuration parameters, such as API keys, model names, and file paths. The configuration format should be human-readable and easy to parse.

## Decision

We have chosen to use **YAML** as the configuration format for this project. A `config/settings.yaml` file will be used to store the configuration parameters.

## Consequences

### Pros

*   **Human-readable:** YAML is a human-readable data serialization format that is easy to understand and edit.
*   **Hierarchical:** YAML supports hierarchical data structures, which is useful for organizing configuration parameters.
*   **Comments:** YAML supports comments, which can be used to document the configuration parameters.

### Cons

*   **Requires a library:** Parsing YAML requires a third-party library like `PyYAML`. However, this is a lightweight dependency that is easy to install.

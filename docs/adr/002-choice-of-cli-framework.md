# ADR-002: Choice of CLI Framework

## Status

Accepted

## Context

The project requires a command-line interface (CLI) to allow users to run evaluations, generate prompts, and analyze results. The CLI framework should be easy to use, have good documentation, and support modern Python features like type hints.

## Decision

We have chosen to use **Typer** as the CLI framework for this project.

## Consequences

### Pros

*   **Easy to Use:** Typer is built on top of Click and is very easy to use. It uses Python type hints to define commands and options, which makes the code clean and self-documenting.
*   **Good Documentation:** Typer has excellent documentation with plenty of examples.
*   **Modern:** Typer is a modern CLI framework that is actively maintained.
*   **Automatic Help Generation:** Typer automatically generates help messages for commands and options.

### Cons

*   **Less flexible than Click:** Typer is less flexible than its underlying framework, Click. However, for the scope of this project, the features provided by Typer are sufficient.

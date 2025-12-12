# ADR-006: Choice of Testing Framework

## Status

Accepted

## Context

The project requires a testing framework to write and run unit tests for the code. The testing framework should be easy to use and integrate well with the Python ecosystem.

## Decision

We have chosen to use **Pytest** as the testing framework for this project.

## Consequences

### Pros

*   **Simple and Pythonic:** Pytest has a simple and intuitive syntax that is easy to learn and use.
*   **Powerful Features:** Pytest has a rich set of features, including fixtures, parametrization, and powerful assertions.
*   **Good Ecosystem:** Pytest has a large ecosystem of plugins that can be used to extend its functionality.
*   **Excellent for Data Science:** Pytest is widely used in the data science community and integrates well with libraries like Pandas and NumPy.

### Cons

*   **Less "standard" than unittest:** While Pytest is very popular, the `unittest` module is part of the Python standard library. However, Pytest is considered by many to be the de-facto standard for testing in Python.

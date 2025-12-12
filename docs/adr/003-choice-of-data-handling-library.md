# ADR-003: Choice of Data Handling Library

## Status

Accepted

## Context

The project requires a library to handle the ground truth dataset, which is in CSV format. The library should be able to read and parse the CSV file, and provide a convenient way to access the data.

## Decision

We have chosen to use **Pandas** for handling the data in this project.

## Consequences

### Pros

*   **Powerful and Flexible:** Pandas is a powerful library for data manipulation and analysis. It provides a `DataFrame` object that is easy to work with and supports a wide range of operations.
*   **Excellent CSV Support:** Pandas has excellent support for reading and writing CSV files.
*   **Widely Used:** Pandas is the de-facto standard for data analysis in Python, and it is well-documented and supported.

### Cons

*   **Overkill for simple CSV parsing:** For simple CSV parsing, Pandas might be considered an overkill. However, given the possibility of more complex data manipulation in the future, using Pandas from the start is a good investment.

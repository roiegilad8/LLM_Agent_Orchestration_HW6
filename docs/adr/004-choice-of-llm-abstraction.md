# ADR-004: Choice of LLM Abstraction

## Status

Accepted

## Context

The project needs to interact with different Large Language Models (LLMs). To make the code modular and extensible, an abstraction layer is needed to hide the implementation details of each LLM API.

## Decision

We have decided to create a **custom abstraction layer** for interacting with LLMs. This layer consists of a `BaseEvaluator` abstract class and concrete implementations for each prompt engineering technique. The `OpenAIClient` class is an example of a client that can be used with this abstraction layer.

## Consequences

### Pros

*   **Flexibility:** A custom abstraction layer gives us full control over the design and implementation. We can easily add support for new LLMs by creating new clients that implement the same interface.
*   **Decoupling:** The abstraction layer decouples the core logic of the application from the specific implementation of each LLM client.

### Cons

*   **More effort:** Creating a custom abstraction layer requires more effort than using an existing library like LangChain or LiteLLM. However, for the scope of this project, a simple custom abstraction layer is sufficient and provides more learning opportunities.

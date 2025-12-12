# ADR-007: Decision to use manual evaluation

## Status

Accepted

## Context

The project requires evaluating the generated prompts against different LLMs. The initial plan was to use the OpenAI API to get the responses and then evaluate them. However, the user did not have a valid OpenAI API key.

## Decision

We have decided to switch to a **manual evaluation** workflow. The application will generate the prompt files, and the user will manually run these prompts in the LLM of their choice. The user will then provide the responses in a structured format, and the application will analyze the results.

## Consequences

### Pros

*   **No API key required:** This approach does not require any API keys, which makes the tool more accessible.
*   **Flexibility:** The user can use any LLM they want, including web-based interfaces that do not provide an API.

### Cons

*   **Manual effort:** This approach requires manual effort from the user to run the prompts and provide the responses.
*   **Error-prone:** The manual process of copying and pasting prompts and responses can be error-prone.
*   **Less reproducible:** The manual evaluation process is less reproducible than an automated one.

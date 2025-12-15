# Contributing Guide

## Code of Conduct
Be respectful, inclusive, and collaborative. We follow the Contributor Covenant.

---

## Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/LLM_Agent_Orchestration_HW6.git
cd LLM_Agent_Orchestration_HW6
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

### 4. Install pre-commit hooks
```bash
pre-commit install
```

---

## Code Style & Conventions

### Formatting
- **Line Length:** 100 characters max
- **Formatter:** Black (auto-formats on commit)
- **Import Order:** isort (auto-sorts on commit)

### Naming Conventions
- **Variables/Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** prefix with `_` (e.g., `_private_var`)

### Docstrings
Use Google-style docstrings:
```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description of what the function does.
    
    Longer description if needed. Explain the purpose,
    parameters, and return value.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
    pass
```

### Type Hints
Use type hints for all function signatures:
```python
def process_data(data: list[str], count: int) -> dict[str, int]:
    """Process data and return counts."""
    return {}
```

### Comments
- Use `#` for inline comments
- Keep comments concise and meaningful
- Avoid obvious comments: `x = 1  # set x to 1` ❌
- Explain *why*, not *what*: `# Account for timezone offset in UTC` ✅

---

## Git Workflow

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation
- `test/description` - Tests only
- `refactor/description` - Code cleanup

### Commit Messages
Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style changes (formatting, semicolons, etc)
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Build, dependencies, etc
- `ci:` CI/CD changes

**Examples:**
```
feat(cost-analysis): add cost breakdown by technique
fix(grading): handle edge case in accuracy calculation
docs: update CONTRIBUTING.md with code style guide
test(compare): add unit tests for grading logic
```

### Commit Size
- Keep commits small and focused (1 change per commit)
- Don't mix features and bug fixes
- Write clear, descriptive commit messages

### Pull Request Process
1. Create feature branch from `main`
2. Make commits with clear messages
3. Push to your fork
4. Open PR with:
   - Clear title (`feat:` or `fix:` prefix)
   - Description of changes
   - Reference related issues
5. Pass all checks (linting, tests, coverage)
6. Request review
7. Merge after approval

---

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_grading.py::test_accuracy_calculation
```

### Writing Tests
- Use `pytest` framework
- Prefix test files with `test_`
- Prefix test functions with `test_`
- Use descriptive names: `test_accuracy_calculation_with_perfect_scores` ✅

```python
def test_accuracy_calculation():
    """Test accuracy is calculated correctly."""
    from src.grader import calculate_accuracy
    
    results = ['A', 'B', 'C']
    expected = ['A', 'B', 'D']
    
    accuracy = calculate_accuracy(results, expected)
    assert accuracy == 2/3
```

---

## Quality Checks

### Pre-commit Hooks
Automatically run on `git commit`:
- **Black** - Code formatting
- **isort** - Import sorting
- **ruff** - Linting
- **trailing-whitespace** - Remove trailing spaces
- **end-of-file-fixer** - Add newlines to EOF
- **check-yaml** - Validate YAML files
- **mypy** - Type checking (light)

If hooks fail, fix the issues and commit again.

### Manual Checks
```bash
# Format code
black .

# Sort imports
isort .

# Lint
ruff check .

# Type checking
mypy src/
```

### CI/CD Pipeline
Every push runs:
- Linting (ruff, black, isort)
- Type checking (mypy)
- Tests (pytest)
- Coverage report
- Build check

All checks must pass before merging.

---

## Documentation

### README.md
- High-level project overview
- Quick start instructions
- Key features
- Links to detailed docs

### Docstrings
- All public functions and classes
- Clear parameter and return descriptions
- Examples for complex functions

### Comments
- Explain *why*, not *what*
- Keep up-to-date with code changes
- Remove commented-out code

### Changelog
Update `CHANGELOG.md` with each release:
```
## [1.0.0] - 2024-12-15

### Added
- Cost analysis module
- Prompt engineering experiments
- CI/CD pipeline

### Fixed
- Token counting bug in analysis

### Changed
- Updated documentation
```

---

## Project Structure

```
LLM_Agent_Orchestration_HW6/
├── src/                          # Source code
│   ├── grader.py                # Grading logic
│   ├── analyzer.py              # Analysis and metrics
│   └── utils.py                 # Utilities
├── tests/                        # Test files
│   ├── test_grader.py
│   └── test_analyzer.py
├── results/                      # Results (gitignored)
│   ├── GPT/
│   ├── Grok/
│   ├── Perplexity/
│   └── RESULTS.md
├── outputs/                      # Generated outputs
│   ├── *.csv                    # Analysis files
│   └── *.png                    # Visualizations
├── .github/workflows/            # CI/CD pipelines
├── .pre-commit-config.yaml      # Pre-commit hooks
├── pyproject.toml               # Linting & formatting config
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Dev dependencies
└── README.md                    # Project documentation
```

---

## Performance & Scalability

### Token Optimization
- Use Baseline for simple queries
- Use Few-Shot for pattern matching
- Use CoT for reasoning tasks
- Use ReAct only for complex multi-step problems

### Cost Optimization
- Perplexity: Best cost-to-performance (~$0.03 per 100 Qs)
- GPT-4o: Best reasoning but highest cost (~$0.18)
- Grok-2: Middle ground (~$0.20)

---

## Questions?

- Check existing issues/discussions
- Open a new GitHub issue
- Reference the documentation
- Ask in comments on pull requests

Thank you for contributing! 🚀

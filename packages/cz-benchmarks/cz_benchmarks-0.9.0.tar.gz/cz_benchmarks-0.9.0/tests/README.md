# Test Suite Documentation

This document describes the test structure and patterns used in the CZ Benchmarks test suite.

## Directory Structure

```
tests/
├── datasets/         # Tests for dataset handling and loading
├── metrics/          # Tests for evaluation metrics
├── models/          # Tests for model implementations
├── tasks/           # Tests for different benchmark tasks
└── utils.py         # Common test utilities
```

## Test Patterns

### 1. Test Organization

- Tests are organized by component (datasets, metrics, models, tasks)
- Each component has its own directory with a `conftest.py` for shared fixtures
- Test files follow the naming convention `test_*.py`

### 2. Fixtures

Fixtures are defined in `conftest.py` files and follow these patterns:

```python
@pytest.fixture
def fixture_name():
    """Docstring explaining the fixture's purpose."""
    # Setup code
    yield value  # or return value
    # Cleanup code (if needed)
```

Common fixture patterns:
- Registry fixtures (e.g., `dummy_metric_registry`)
- Data fixtures (e.g., `sample_data`)
- Function fixtures (e.g., `dummy_metric_function`)

### 3. Test Structure

Tests follow these patterns:

1. **Setup**: Use fixtures for common setup
2. **Test Case**: Clear, focused test cases with descriptive names
3. **Assertions**: Use pytest's assertion system
4. **Error Handling**: Test both success and failure cases

Example:
```python
def test_feature_name_behavior(fixture1, fixture2):
    """Docstring explaining what this test verifies."""
    # Arrange
    input_data = fixture1
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

### 4. Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear, descriptive test names
3. **Documentation**: Include docstrings explaining test purpose
4. **Error Cases**: Test both success and failure scenarios
5. **Fixtures**: Use fixtures for reusable setup code
6. **Assertions**: Use specific assertions (e.g., `assert result == expected`)

## Adding New Tests

### 1. For a New Component

1. Create a new directory in `tests/` if needed
2. Create a `conftest.py` with shared fixtures
3. Create test files following `test_*.py` pattern

### 2. For an Existing Component

1. Add new test functions to the appropriate test file
2. Add new fixtures to `conftest.py` if needed
3. Follow the existing patterns in that component

### 3. Test File Template

```python
import pytest
from czbenchmarks.component import Feature

def test_feature_behavior(fixture1, fixture2):
    """Test description."""
    # Arrange
    input_data = fixture1
    
    # Act
    result = Feature.process(input_data)
    
    # Assert
    assert result == expected_value

def test_feature_error_handling(fixture1):
    """Test error handling."""
    with pytest.raises(ExpectedError):
        Feature.process(invalid_input)
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/metrics/test_metrics.py

# Run tests with coverage
pytest --cov=czbenchmarks
```

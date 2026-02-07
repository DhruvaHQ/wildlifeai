# Testing Guide for WildlifeAI

## Current Test Coverage

**Overall Coverage: 67%**

| Module | Coverage | Lines | Missing |
|--------|----------|-------|---------|
| `__init__.py` | 100% | 3 | 0 |
| `models.py` | 100% | 14 | 0 |
| `pipeline.py` | 83% | 59 | 10 |
| `utils.py` | 71% | 70 | 20 |
| `cli.py` | 0% | 26 | 26 |
| **TOTAL** | **67%** | **172** | **56** |

## Running Tests

### Quick Test Run
```bash
poetry run pytest
```

### Verbose Output
```bash
poetry run pytest -v
```

### With Coverage
```bash
poetry run pytest --cov=src/wildlifeai --cov-report=term-missing
```

### HTML Coverage Report
```bash
poetry run pytest --cov=src/wildlifeai --cov-report=html
# Open htmlcov/index.html in browser
```

### Run Specific Tests
```bash
# Single file
poetry run pytest tests/test_utils.py

# Single class
poetry run pytest tests/test_utils.py::TestExtractExif

# Single test
poetry run pytest tests/test_utils.py::TestExtractExif::test_extract_exif_with_no_exif
```

## Test Structure

```
tests/
├── __init__.py
├── test_utils.py       # Tests for image processing utilities
├── test_models.py      # Tests for ML model interface
└── test_pipeline.py    # Integration tests for pipeline
```

## Writing Tests

### Example Test
```python
def test_extract_exif_with_no_exif():
    """Test EXIF extraction from image without EXIF data"""
    img = Image.new('RGB', (100, 100), color='red')
    exif = extract_exif(img)
    
    assert isinstance(exif, dict)
```

### Using Fixtures
```python
@pytest.fixture
def temp_image_folder(tmp_path):
    """Create temporary folder with test images"""
    image_dir = tmp_path / "test_images"
    image_dir.mkdir()
    
    img = Image.new('RGB', (100, 100), color='blue')
    img.save(image_dir / "test1.jpg")
    
    return image_dir
```

## Continuous Integration

Tests run automatically on:
- Every push to `main` branch
- Every pull request
- Multiple Python versions (3.10, 3.11, 3.12)
- Multiple OS (Ubuntu, Windows, macOS)

See: [.github/workflows/tests.yml](.github/workflows/tests.yml)

## Coverage Goals

- **Current**: 67%
- **Target**: 80%
- **Minimum**: 60%

### Areas Needing Coverage

1. **CLI Module (0%)** - Highest priority
   - Test command-line argument parsing
   - Test config file loading
   - Test error messages

2. **Pipeline Module (83%)** - Good, needs minor additions
   - Test edge cases
   - Test model loading with actual path

3. **Utils Module (71%)** - Needs improvement
   - Test more error scenarios
   - Test EXIF extraction with real metadata
   - Test different image formats

## Test Best Practices

1. **Descriptive Names**: Use clear, descriptive test names
2. **One Assertion**: Focus on one thing per test
3. **AAA Pattern**: Arrange, Act, Assert
4. **Use Fixtures**: Reuse common test setup
5. **Test Errors**: Test both success and failure cases
6. **Mock External**: Mock external dependencies (files, network)

## Running Linters

### Black (formatting)
```bash
poetry run black src/ tests/
```

### Flake8 (linting)
```bash
poetry run flake8 src/ tests/
```

## Contributing Tests

When adding new features:
1. Write tests first (TDD approach)
2. Ensure tests pass: `poetry run pytest`
3. Check coverage: `poetry run pytest --cov`
4. Aim for >80% coverage on new code
5. Run linters before committing

## Test Maintenance

- Review tests monthly
- Update tests when requirements change
- Remove obsolete tests
- Keep test data minimal
- Document complex test setups

---

Last updated: February 7, 2026

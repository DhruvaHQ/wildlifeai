# Contributing to WildlifeAI

Thank you for your interest in contributing to WildlifeAI! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YourUsername/wildlifeai.git
   cd wildlifeai
   ```

2. **Install dependencies**
   ```bash
   poetry install --with dev
   ```

3. **Run tests to verify setup**
   ```bash
   poetry run pytest
   ```

## Development Workflow

### Code Style

We use Black for code formatting and Flake8 for linting.

**Format your code:**
```bash
poetry run black src/ tests/
```

**Check for linting issues:**
```bash
poetry run flake8 src/ tests/
```

### Running Tests

**Run all tests:**
```bash
poetry run pytest
```

**Run specific test file:**
```bash
poetry run pytest tests/test_utils.py
```

**Run with coverage:**
```bash
poetry run pytest --cov=src/wildlifeai --cov-report=html
```

View coverage report in `htmlcov/index.html`

### Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add type hints where appropriate
   - Follow existing code style

3. **Add tests**
   - Write tests for new functionality
   - Ensure all tests pass
   - Aim for good code coverage

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure CI passes

## Areas for Contribution

### High Priority
- 🤖 **ML Model Integration** - Integrate actual species classification models
- 📸 **Enhanced EXIF Support** - Add GPS, orientation, and advanced metadata
- 🧪 **Test Coverage** - Expand test suite
- 📚 **Documentation** - Improve docstrings and add examples

### Medium Priority
- ⚡ **Performance** - Optimize image processing pipeline
- 🔌 **Plugins** - Create plugin system for custom processors
- 📊 **Batch Processing** - Efficient multi-file processing
- 🌐 **API** - REST API for remote processing

### Ideas Welcome
- Cloud integration (AWS, GCP, Azure)
- Real-time camera trap monitoring
- Species database integration
- Visualization dashboards
- Mobile app support

## Code Guidelines

### Python Style
- Follow PEP 8
- Use type hints for function signatures
- Write comprehensive docstrings (Google style)
- Keep functions focused and small

### Documentation
- Update README.md for user-facing changes
- Add docstrings to all public functions/classes
- Include usage examples where helpful

### Testing
- Write unit tests for utilities and models
- Write integration tests for pipelines
- Test error cases and edge conditions
- Use fixtures for common test data

### Commit Messages
- Use clear, descriptive messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issues when applicable
- Examples:
  - `Add support for GPS metadata extraction`
  - `Fix path handling on Windows (#123)`
  - `Update documentation for CLI usage`

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Tag maintainers for urgent issues

Thank you for contributing to wildlife conservation through technology! 🦁🌍

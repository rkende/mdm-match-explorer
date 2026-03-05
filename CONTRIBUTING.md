# Contributing to IBM MDM Match Decision Explorer

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 🌟 Ways to Contribute

- **Report bugs** - Found an issue? Let us know!
- **Suggest features** - Have ideas for improvements?
- **Improve documentation** - Help make docs clearer
- **Submit code** - Fix bugs or add features
- **Share feedback** - Tell us about your experience

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- IBM MDM (Match 360) access for testing
- Familiarity with Streamlit and REST APIs

### Development Setup

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub
   # Then clone your fork
   git clone https://github.com/YOUR_USERNAME/mdm-match-explorer.git
   cd mdm-match-explorer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Production dependencies
   pip install -r requirements.txt
   
   # Development dependencies
   pip install -r requirements-dev.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

5. **Run Tests**
   ```bash
   pytest tests/
   ```

6. **Start Development Server**
   ```bash
   streamlit run src/app.py
   ```

## 📝 Development Workflow

### 1. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 2. Make Your Changes

Follow these guidelines:

#### Code Style

- **Python**: Follow PEP 8
- **Line length**: Max 100 characters
- **Imports**: Group stdlib, third-party, local
- **Type hints**: Use for function signatures
- **Docstrings**: Use Google style

Example:
```python
from typing import Optional, Dict, Any

def compare_entities(
    entity1: Dict[str, Any],
    entity2: Dict[str, Any],
    crn: str,
    debug: bool = False
) -> Optional[Dict[str, Any]]:
    """Compare two entities using MDM API.
    
    Args:
        entity1: First entity data
        entity2: Second entity data
        crn: Cloud Resource Name
        debug: Enable debug output
        
    Returns:
        Match result dictionary or None if error
        
    Raises:
        ValueError: If entity data is invalid
        ConnectionError: If API is unreachable
    """
    pass
```

#### Code Organization

- Keep functions focused and small (<50 lines)
- Use meaningful variable names
- Add comments for complex logic
- Extract magic numbers to constants
- Use Pydantic models for data validation

#### UI Components

- Keep Streamlit components modular
- Use session state appropriately
- Provide clear user feedback
- Handle errors gracefully
- Add loading indicators for slow operations

### 3. Write Tests

Add tests for new functionality:

```python
# tests/test_mdm_client.py
import pytest
from src.mdm.client import MDMClient

def test_compare_entities_success():
    """Test successful entity comparison."""
    client = MDMClient(
        base_url="https://test.example.com",
        api_token="test_token"
    )
    
    result = client.compare_entities(
        entity1={"legal_name": {"given_name": "John"}},
        entity2={"legal_name": {"given_name": "John"}},
        crn="test_crn"
    )
    
    assert result is not None
    assert "similarity" in result

def test_compare_entities_invalid_data():
    """Test comparison with invalid data."""
    client = MDMClient(
        base_url="https://test.example.com",
        api_token="test_token"
    )
    
    with pytest.raises(ValueError):
        client.compare_entities(
            entity1={},  # Invalid: empty
            entity2={},
            crn="test_crn"
        )
```

Run tests:
```bash
# All tests
pytest

# Specific test file
pytest tests/test_mdm_client.py

# With coverage
pytest --cov=src tests/

# Verbose output
pytest -v
```

### 4. Update Documentation

If your changes affect usage:

- Update README.md
- Update QUICKSTART.md if setup changes
- Add docstrings to new functions
- Update IMPLEMENTATION_PLAN.md for architecture changes
- Add examples for new features

### 5. Commit Your Changes

Write clear commit messages:

```bash
# Good commit messages
git commit -m "feat: Add support for organization entities"
git commit -m "fix: Correct timestamp format in API requests"
git commit -m "docs: Update installation instructions"
git commit -m "refactor: Extract token management to separate class"

# Bad commit messages (avoid these)
git commit -m "Update code"
git commit -m "Fix bug"
git commit -m "Changes"
```

Commit message format:
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

### 6. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR on GitHub
# Fill in the PR template
```

## 🔍 Code Review Process

### What We Look For

1. **Functionality**
   - Does it work as intended?
   - Are edge cases handled?
   - Is error handling appropriate?

2. **Code Quality**
   - Is it readable and maintainable?
   - Are there code smells?
   - Is it well-organized?

3. **Testing**
   - Are there adequate tests?
   - Do tests pass?
   - Is coverage maintained?

4. **Documentation**
   - Are changes documented?
   - Are docstrings clear?
   - Is README updated if needed?

5. **Performance**
   - Are there performance issues?
   - Is caching used appropriately?
   - Are API calls optimized?

### Review Timeline

- Initial review: Within 2-3 business days
- Follow-up reviews: Within 1-2 business days
- Merge: After approval and CI passes

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try latest version
3. Verify it's reproducible
4. Gather relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.11.5]
- App version: [e.g., 1.0.0]
- MDM version: [e.g., Match 360 v2.0]

**Screenshots**
If applicable

**Additional Context**
Any other relevant information

**Logs**
```
Paste relevant logs here
```
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this needed? What problem does it solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Mockups, examples, references
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_mdm_client.py
│   ├── test_auth.py
│   └── test_models.py
├── integration/            # Integration tests
│   └── test_api_flow.py
└── fixtures/               # Test data
    └── sample_entities.json
```

### Writing Good Tests

```python
# Good test
def test_token_refresh_before_expiry():
    """Test that token refreshes 5 minutes before expiry."""
    manager = TokenManager(api_key="test_key")
    manager.token_expiry = datetime.now() + timedelta(minutes=4)
    
    token = manager.get_token()
    
    assert token is not None
    assert manager.token_expiry > datetime.now() + timedelta(minutes=55)

# Bad test (too vague)
def test_token():
    manager = TokenManager(api_key="test_key")
    assert manager.get_token()
```

### Test Coverage

Aim for:
- Overall: >80%
- Critical paths: 100%
- New features: >90%

Check coverage:
```bash
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html
```

## 📚 Documentation Standards

### Code Documentation

```python
def compare_entities(
    entity1: Dict[str, Any],
    entity2: Dict[str, Any],
    crn: str,
    record_number1: Optional[str] = None,
    record_number2: Optional[str] = None,
    debug: bool = False
) -> Optional[Dict[str, Any]]:
    """Compare two person entities using IBM MDM API.
    
    This function sends a comparison request to the MDM API and returns
    the match decision with confidence scores and field-level analysis.
    
    Args:
        entity1: First entity data dictionary containing person attributes
        entity2: Second entity data dictionary containing person attributes
        crn: Cloud Resource Name identifying the MDM instance
        record_number1: Optional record number for first entity (for existing records)
        record_number2: Optional record number for second entity (for existing records)
        debug: If True, includes detailed debug information in response
        
    Returns:
        Dictionary containing:
            - similarity: Match probability (0.0 to 1.0)
            - match_decision: Boolean indicating if entities match
            - field_scores: Dictionary of individual field match scores
            - debug_info: Optional debug details if debug=True
        Returns None if comparison fails.
        
    Raises:
        ValueError: If entity data is invalid or missing required fields
        ConnectionError: If unable to connect to MDM API
        AuthenticationError: If API credentials are invalid
        
    Example:
        >>> client = MDMClient(base_url="...", api_token="...")
        >>> result = client.compare_entities(
        ...     entity1={"legal_name": {"given_name": "John"}},
        ...     entity2={"legal_name": {"given_name": "Jon"}},
        ...     crn="crn:v1:..."
        ... )
        >>> print(result["similarity"])
        0.85
    """
    pass
```

### README Updates

When adding features, update:
- Features section
- Usage examples
- Configuration options
- Troubleshooting section

## 🔒 Security Guidelines

### Sensitive Data

- Never commit credentials
- Use environment variables
- Add sensitive files to `.gitignore`
- Clear credentials from logs

### Code Security

- Validate all user inputs
- Sanitize data before API calls
- Use HTTPS for all API requests
- Handle errors without exposing internals
- Keep dependencies updated

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead:
1. Email security@example.com
2. Include detailed description
3. Provide steps to reproduce
4. Suggest a fix if possible

## 📋 Pull Request Checklist

Before submitting:

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] CI/CD checks pass
- [ ] Self-review completed

## 🎯 Development Tips

### Debugging

```python
# Enable debug mode
import streamlit as st
st.set_option('client.showErrorDetails', True)

# Add debug prints
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Entity data: {entity}")
```

### Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Streamlit Development

```bash
# Auto-reload on changes
streamlit run src/app.py --server.runOnSave true

# Custom port
streamlit run src/app.py --server.port 8502

# Disable CORS
streamlit run src/app.py --server.enableCORS false
```

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person
- Assume good intentions

### Communication

- Use clear, professional language
- Be patient with questions
- Share knowledge generously
- Acknowledge contributions
- Celebrate successes

## 📞 Getting Help

- **Questions**: Create a discussion
- **Bugs**: Create an issue
- **Features**: Create a feature request
- **Security**: Email security@example.com
- **General**: Join our community chat

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉

---

**Questions?** Open a discussion or reach out to the maintainers.
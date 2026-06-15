# Contributing Guidelines

We welcome contributions to the Network Test Automation Framework!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch
4. Make your changes
5. Commit with descriptive messages
6. Push to your fork
7. Create a Pull Request

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python

- Follow PEP 8
- Use Black for formatting
- Use Pylint for linting
- Type hints required

### JavaScript

- Use ESLint configuration
- Use Prettier for formatting
- Follow React best practices

## Testing

All code must include tests:

```bash
# Backend tests
pytest tests/ -v --cov=app

# Frontend tests
npm test
```

## Pull Request Process

1. Update README.md if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Request review from maintainers
5. Address review comments
6. Merge when approved

## Reporting Issues

When reporting issues, include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error logs if applicable

## Feature Requests

Feature requests should include:

- Use case
- Proposed solution
- Alternative approaches
- Impact assessment

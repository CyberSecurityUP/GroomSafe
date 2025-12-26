# Contributing to GROOMSAFE

Thank you for your interest in contributing to GROOMSAFE! This project focuses on child safety research and investigator protection, so all contributions must adhere to strict ethical guidelines.

## Code of Conduct

### Ethical Requirements

All contributors must:

- ✅ Maintain the highest ethical standards
- ✅ Prioritize child safety and investigator wellbeing
- ✅ Preserve explainability and transparency
- ✅ Respect privacy and data protection principles
- ✅ Follow responsible disclosure practices
- ✅ Consider legal and compliance implications

All contributors must NOT:

- ❌ Introduce features that process explicit content
- ❌ Remove safety guardrails or ethical constraints
- ❌ Bypass human oversight requirements
- ❌ Compromise investigator protection features
- ❌ Reduce explainability or auditability
- ❌ Introduce surveillance capabilities beyond stated scope

## How to Contribute

### Reporting Issues

When reporting issues:

1. Use the GitHub issue tracker
2. Provide clear, detailed descriptions
3. Include steps to reproduce (when applicable)
4. Specify your environment (Python version, OS, etc.)
5. **Never include real conversation data or sensitive information**

### Suggesting Enhancements

Enhancement suggestions should:

1. Align with project ethical principles
2. Include clear use cases and benefits
3. Consider impact on explainability
4. Preserve investigator safety features
5. Be documented with examples

### Pull Requests

#### Before Submitting

1. **Read the project documentation** thoroughly
2. **Discuss major changes** in an issue first
3. **Test your changes** comprehensively
4. **Update documentation** as needed
5. **Follow coding standards** (see below)

#### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes following coding standards
4. Add/update tests for new functionality
5. Ensure all tests pass
6. Update documentation (README, docstrings, etc.)
7. Commit with clear, descriptive messages
8. Push to your fork
9. Submit a pull request

#### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No real data or sensitive information included
- [ ] Ethical guidelines maintained
- [ ] Explainability preserved
- [ ] Audit logging maintained for new features

## Coding Standards

### Python Style

- Follow **PEP 8** style guidelines
- Use **type hints** for function signatures
- Maximum line length: **88 characters** (Black formatter)
- Use **descriptive variable names**

### Documentation

- All modules must have docstrings
- All public functions must have docstrings
- Include type hints in function signatures
- Document parameters and return values
- Provide usage examples for complex features

Example:
```python
def assess_risk(conversation: Conversation) -> RiskAssessment:
    """
    Assess behavioral risk in a conversation

    Args:
        conversation: Conversation object with message sequence

    Returns:
        RiskAssessment with score, stage, and explanation

    Example:
        >>> conversation = load_conversation("example.json")
        >>> assessment = assess_risk(conversation)
        >>> print(assessment.grooming_risk_score)
        65.3
    """
    pass
```

### Testing

- Write unit tests for new functions
- Maintain test coverage above 80%
- Use pytest framework
- Test edge cases and error conditions
- Never use real data in tests (synthetic only)

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Detailed explanation (if needed)

Fixes #issue_number
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

Examples:
```
feat(humanshield): add exposure time tracking

Add detailed tracking of analyst exposure time to enable
better break enforcement and wellbeing monitoring.

Fixes #123
```

## Development Setup

### Local Development

```bash
# Clone repository
git clone https://github.com/your-username/groomsafe.git
cd groomsafe

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Generate synthetic test data
cd groomsafe
python3 data/synthetic/generate_synthetic_data.py

# Run tests
pytest

# Run code formatting
black groomsafe/

# Run linting
flake8 groomsafe/
```

### Testing Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=groomsafe --cov-report=html

# Run specific test file
pytest tests/test_feature_extraction.py

# Run example usage
python3 groomsafe/examples/example_usage.py
```

## Priority Areas

We especially welcome contributions in:

### High Priority

1. **Additional Behavioral Features**: New non-explicit behavioral signals
2. **Enhanced Explainability**: Improved explanation generation
3. **Bias Detection**: Tools to identify and mitigate algorithmic bias
4. **Multi-language Support**: Extend to non-English conversations
5. **Visualization Tools**: Safe, analyst-friendly visualizations

### Medium Priority

1. **Performance Optimization**: Faster feature extraction
2. **Additional Tests**: Expanded test coverage
3. **Documentation Improvements**: Clearer guides and examples
4. **API Enhancements**: New endpoints or improved schemas

### Research Contributions

1. **Validation Studies**: Testing on appropriate datasets
2. **Benchmark Development**: Standard evaluation metrics
3. **Literature Integration**: Incorporating latest research
4. **Ethical Framework**: Enhanced ethical guidelines

## Review Process

All contributions will be reviewed for:

1. **Technical Quality**: Code correctness and efficiency
2. **Ethical Compliance**: Adherence to project principles
3. **Documentation**: Clarity and completeness
4. **Testing**: Adequate test coverage
5. **Safety**: No security vulnerabilities introduced
6. **Explainability**: Maintained transparency

Reviewers may request changes before approval.

## Questions?

If you have questions:

1. Check existing documentation
2. Search closed issues
3. Open a new issue with your question
4. Tag with `question` label

## Recognition

All contributors will be recognized in:

- Project README
- Release notes
- Academic publications (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see LICENSE file).

## Thank You!

Your contributions help protect children and support investigators. Thank you for being part of this important work!

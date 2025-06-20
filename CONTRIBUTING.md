# Contributing to AI DJ Streamer 🎵

Thank you for your interest in contributing to AI DJ Streamer! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository
- Click the "Fork" button on the GitHub repository page
- Clone your forked repository to your local machine

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write clean, well-documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_main.py -v

# Run linting
pip install flake8 black
flake8 .
black --check .
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

### 6. Push and Create a Pull Request
```bash
git push origin feature/your-feature-name
```

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Confluent Cloud account (for Kafka testing)

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `kafka_config.py` with your Confluent credentials
4. Run the application: `python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8002)"`

## 🎯 Areas for Contribution

### High Priority
- [ ] Add more sophisticated sentiment analysis models
- [ ] Implement user authentication and personalization
- [ ] Add support for multiple music streaming services
- [ ] Create mobile app version
- [ ] Add real-time chat integration (Twitch, YouTube, etc.)

### Medium Priority
- [ ] Improve error handling and logging
- [ ] Add more music genres and tracks
- [ ] Implement caching for better performance
- [ ] Add unit tests for all components
- [ ] Create deployment guides for cloud platforms

### Low Priority
- [ ] Add dark/light theme toggle
- [ ] Implement music playlist export
- [ ] Add social sharing features
- [ ] Create browser extension

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Add comments for complex logic
- Use meaningful variable names

### CSS
- Use BEM methodology for class naming
- Keep styles modular and reusable
- Use CSS custom properties for theming
- Ensure responsive design

## 🧪 Testing Guidelines

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_main.py
```

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Include examples in docstrings
- Document complex algorithms
- Keep README.md updated

### API Documentation
- Document all API endpoints
- Include request/response examples
- Add error codes and messages
- Keep OpenAPI spec updated

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

## 💡 Feature Requests

When requesting features, please include:
- Clear description of the feature
- Use cases and benefits
- Implementation suggestions (if any)
- Priority level

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-dj-streamer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-dj-streamer/discussions)
- **Email**: your.email@example.com

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI DJ Streamer! 🎵 
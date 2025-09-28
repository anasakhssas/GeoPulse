# Contributing to GeoPulse

Thank you for your interest in contributing to GeoPulse! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/geopulse.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`

## 🛠️ Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### Quick Start
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/geopulse.git
cd geopulse

# Start the application
docker-compose -f docker-compose.simple-no-db.yml up -d

# Or run locally
python run_local.py
```

## 📝 Making Changes

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issues when applicable: "Fix #123: Description"

Example:
```
Add country filter functionality to city dashboard

- Implement dropdown filter for country selection
- Update city statistics to respect country filter
- Add tests for filtering logic
```

## 🧪 Testing

### Testing Your Changes
1. Test with the provided sample CSV files
2. Add new CSV files to `data/input/` and verify auto-refresh
3. Check both dashboard pages work correctly
4. Ensure Docker containers start without errors

### Adding Tests
- Add test cases for new functionality
- Update existing tests when modifying features
- Test with various CSV formats and edge cases

## 📊 CSV Data Format

When adding test data or examples, follow this format:
```csv
name,country,city,date
John Doe,United States,New York,2024-01-15
Jane Smith,United Kingdom,London,2024-01-16
```

Required columns: `name`, `country`, `city`, `date`

## 🎯 Types of Contributions

### 🐛 Bug Reports
- Use the issue template
- Include steps to reproduce
- Provide error messages and logs
- Specify your environment (OS, Docker version, etc.)

### ✨ Feature Requests
- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider backwards compatibility

### 💻 Code Contributions
- Dashboard improvements
- Data processing enhancements
- Docker configuration optimizations
- Documentation updates
- Performance improvements

## 📋 Pull Request Process

1. **Create an issue** first to discuss major changes
2. **Fork** the repository and create a feature branch
3. **Make your changes** following the coding standards
4. **Test thoroughly** with various CSV files
5. **Update documentation** if needed
6. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/GIFs for UI changes
   - Test results

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added test cases
- [ ] Tested with sample CSV files
- [ ] Dashboard displays correctly
- [ ] Docker containers work

## Screenshots
(If applicable)

## Related Issues
Fixes #123
```

## 🎨 UI/UX Guidelines

### Dashboard Design
- Keep the interface clean and intuitive
- Use consistent color schemes
- Ensure responsive design
- Make charts interactive and informative

### Data Visualization
- Use appropriate chart types for data
- Include meaningful tooltips
- Ensure accessibility (color-blind friendly)
- Provide clear legends and labels

## 🔍 Code Review Guidelines

### For Contributors
- Keep changes focused and atomic
- Write clear commit messages
- Respond to feedback promptly
- Be open to suggestions

### For Reviewers
- Be constructive and helpful
- Check functionality and performance
- Verify documentation updates
- Test the changes locally

## 📚 Documentation

### When to Update Documentation
- Adding new features
- Changing existing functionality
- Updating installation/setup process
- Adding new CSV format support

### Documentation Style
- Use clear, simple language
- Include code examples
- Add screenshots for UI features
- Keep README.md updated

## ❓ Questions?

- Create an issue for questions about contributing
- Check existing issues and pull requests first
- Be respectful and patient

## 🏆 Recognition

Contributors will be:
- Added to the project's contributors list
- Mentioned in release notes for significant contributions
- Recognized in the project documentation

Thank you for contributing to GeoPulse! 🌍📊
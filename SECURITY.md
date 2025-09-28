# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in GeoPulse, please report it privately by emailing the project maintainers. Please do not create public issues for security vulnerabilities.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

- GeoPulse handles CSV data input - ensure your CSV files don't contain sensitive information
- The dashboard runs on localhost:8501 by default - consider network access controls for production
- Docker containers run with standard permissions - review for production deployments
- No authentication is built-in - add authentication for production use
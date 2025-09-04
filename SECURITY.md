# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it privately via:
- GitHub Issues (mark as security vulnerability)
- Do NOT create public issues for security vulnerabilities

## Security Best Practices

### For Contributors

1. **Never commit credentials:**
   - No passwords, tokens, or API keys in code
   - Use environment variables for sensitive data
   - Check `.env.example` for required variables

2. **Sensitive files to avoid:**
   - `*.key`, `*.pem`, `*.p12` files
   - Database files with real data
   - Cookie/session files
   - Configuration files with secrets

3. **Before committing:**
   ```bash
   # Check for potential secrets
   git diff --cached | grep -i -E "(password|secret|token|key)"
   ```

### For Users

1. **Environment Variables:**
   ```bash
   export INSTAGRAM_USERNAME="your_username"
   export INSTAGRAM_PASSWORD="your_password"
   ```

2. **Never share:**
   - Your Instagram credentials
   - Generated cookie files
   - Cache databases with personal data

## Security Features

- ✅ Credentials via environment variables only
- ✅ Comprehensive `.gitignore` for sensitive files
- ✅ No hardcoded secrets in codebase
- ✅ Secure token handling for GitHub integration

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.4.x   | ✅ Yes             |
| < 1.4   | ❌ No              |


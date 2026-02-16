# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability in VishwaGuru, we appreciate your help in disclosing it to us responsibly.

### How to Report

**Please DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security issues by emailing: **[Your contact email here]**

### What to Include

Please include the following information in your report:

- **Description of the vulnerability**: Clear and detailed explanation
- **Steps to reproduce**: Step-by-step instructions to reproduce the issue
- **Potential impact**: What could an attacker achieve?
- **Affected versions**: Which versions are vulnerable?
- **Suggested fix** (if available): Proposed solution or mitigation

### Response Timeline

- **Initial Response**: We aim to acknowledge your report within **48 hours**
- **Status Update**: We will provide a status update within **7 days**
- **Fix Timeline**: We aim to release a fix within **30 days** for critical issues

### Responsible Disclosure

We kindly ask that you:
- Give us reasonable time to address the issue before public disclosure
- Do not exploit the vulnerability beyond what is necessary to demonstrate it
- Do not access or modify other users' data

We greatly appreciate your efforts to keep VishwaGuru secure!

---

## 🛡️ Security Best Practices for Deployment

When deploying VishwaGuru in production, please follow these security guidelines:

### **1. Environment Variables**
- ✅ **Never commit API keys or secrets** to the repository
- ✅ Use environment variables for all sensitive configuration
- ✅ Rotate API keys regularly
- ✅ Use different keys for development and production

### **2. Database Security**
- ✅ Use strong database passwords (minimum 16 characters, mixed case, numbers, symbols)
- ✅ Enable SSL/TLS for database connections (`?sslmode=require` in PostgreSQL)
- ✅ Restrict database access to application servers only
- ✅ Regularly backup your database

### **3. API Security**
- ✅ Implement rate limiting on all API endpoints (see middleware in backend)
- ✅ Validate and sanitize all user inputs
- ✅ Use parameterized queries (SQLAlchemy ORM does this automatically)
- ✅ Enable CORS only for trusted domains in production

### **4. HTTPS/TLS**
- ✅ Always use HTTPS in production (Netlify and Render provide this automatically)
- ✅ Enforce HTTPS redirects
- ✅ Use HSTS headers
- ✅ Keep TLS certificates up to date

### **5. Dependencies**
- ✅ Keep all dependencies updated regularly
- ✅ Run `npm audit` and `pip-audit` regularly
- ✅ Use Dependabot for automated dependency updates
- ✅ Review dependency changes before updating

### **6. Authentication & Authorization**
- ✅ Use strong password requirements if implementing user accounts
- ✅ Implement proper session management
- ✅ Use secure, httpOnly cookies
- ✅ Implement proper access controls

### **7. Telegram Bot Security**
- ✅ Keep bot token secret and never expose it
- ✅ Validate all incoming webhook requests
- ✅ Implement rate limiting for bot commands
- ✅ Sanitize all user-provided content before processing

### **8. AI/Gemini API Security**
- ✅ Never expose your Gemini API key
- ✅ Implement request rate limiting
- ✅ Validate and sanitize inputs before sending to AI
- ✅ Monitor API usage for anomalies

### **9. File Upload Security** (if implementing)
- ✅ Validate file types and sizes
- ✅ Scan uploads for malware
- ✅ Store uploads outside the web root
- ✅ Use random filenames

### **10. Monitoring & Logging**
- ✅ Enable security monitoring and alerts
- ✅ Log all authentication attempts
- ✅ Monitor for unusual activity patterns
- ✅ Never log sensitive data (passwords, API keys, tokens)

---

## 🔐 Security Checklist for Production

Before deploying to production, ensure:

- [ ] All environment variables are properly set
- [ ] API keys are production keys, not development keys
- [ ] Database uses strong password and SSL
- [ ] HTTPS is enforced
- [ ] CORS is configured for specific domains only
- [ ] Rate limiting is enabled
- [ ] Dependencies are up to date
- [ ] Security headers are configured
- [ ] Monitoring and logging are enabled
- [ ] Backup strategy is in place

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [React Security Best Practices](https://react.dev/learn/security)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

## 🙏 Acknowledgments

We would like to thank all security researchers who responsibly disclose vulnerabilities to us.

---

**Last Updated**: February 2026  
**Contact**: [Your contact email]

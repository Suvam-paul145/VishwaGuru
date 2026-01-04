# ECWoC26 - Elite Coders Winter of Code 2026

Welcome to VishwaGuru's participation in ECWoC26! 🎉

## About ECWoC26

Elite Coders Winter of Code (ECWoC26) is a program designed to foster open-source contributions and help developers build real-world skills through challenging technical problems.

## About VishwaGuru

VishwaGuru is an open-source platform empowering India's youth to engage with democracy. It uses AI to simplify contacting representatives, filing grievances, and organizing community action.

**Key Features:**
- 🤖 AI-Powered Action Plans using Google Gemini
- 📱 Issue Reporting via Web and Telegram Bot
- 🗺️ Find My MLA/Representative feature
- 🔍 Computer Vision for issue detection (potholes, garbage, flooding, etc.)
- 🌐 Modern Stack: React + FastAPI + PostgreSQL

## Complex Technical Challenges

We've curated **10 highly complex technical challenges** perfect for ECWoC26 participants. These challenges span multiple domains and technologies:

### Challenge Categories

1. **Real-time Systems** - WebSocket, Redis Pub/Sub, Event-Driven Architecture
2. **Internationalization** - Multi-language support, Translation pipelines, i18n
3. **Machine Learning** - Computer Vision, Multi-model Ensembles, NLP
4. **Blockchain** - Web3, Smart Contracts, Decentralized Storage
5. **Data Science** - Clustering Algorithms, Similarity Search, Analytics
6. **Progressive Web Apps** - Offline-first, Service Workers, Background Sync
7. **Data Visualization** - Advanced Dashboards, Interactive Charts
8. **AI/ML Systems** - Smart Routing, Classification, Pattern Recognition
9. **Security** - Rate Limiting, Abuse Prevention, API Security
10. **Quality Assurance** - E2E Testing, Visual Regression, CI/CD

## Documentation

- **[ECWOC26_COMPLEX_ISSUES.md](./ECWOC26_COMPLEX_ISSUES.md)** - Detailed description of all 10 complex issues
- **[ECWOC26_ISSUE_TEMPLATES.md](./ECWOC26_ISSUE_TEMPLATES.md)** - Ready-to-use GitHub issue templates
- **[create_ecwoc26_issues.sh](./create_ecwoc26_issues.sh)** - Helper script for issue creation

## How to Participate

### 1. Choose an Issue

Browse the [Issues](https://github.com/RohanExploit/VishwaGuru/issues?q=is%3Aissue+is%3Aopen+label%3AECWoC26) labeled with **ECWoC26**.

Each issue includes:
- 🎯 Clear objectives
- 📋 Detailed requirements
- ✅ Acceptance criteria
- 🎓 Required skills
- ⏱️ Estimated time
- 📚 Resources

### 2. Express Interest

Comment on the issue you want to work on:
```
Hi! I'm interested in working on this issue as part of ECWoC26. 

My relevant experience:
- [Your relevant skills/projects]

My approach:
- [Brief outline of your proposed solution]

Expected timeline: [Your estimate]
```

Wait for maintainer approval before starting work.

### 3. Set Up Development Environment

```bash
# Clone the repository
git clone https://github.com/RohanExploit/VishwaGuru.git
cd VishwaGuru

# Backend setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Create .env file
cp .env.example .env
# Add your API keys (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN)
```

For detailed instructions, see [README.md](./README.md).

### 4. Development Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... code ...

# Test your changes
# Run backend tests
pytest backend/

# Run frontend tests
cd frontend && npm test

# Commit with meaningful messages
git add .
git commit -m "feat: Add WebSocket notification system"

# Push to your fork
git push origin feature/your-feature-name
```

### 5. Submit Pull Request

1. Push your changes to your fork
2. Open a Pull Request to the main repository
3. Reference the issue: "Closes #XX" or "Fixes #XX"
4. Fill out the PR template completely
5. Respond to code review feedback promptly

## Contribution Guidelines

### Code Quality Standards

- ✅ Write clean, readable, well-documented code
- ✅ Follow existing code style and conventions
- ✅ Add comprehensive tests for new features
- ✅ Update documentation as needed
- ✅ Ensure no security vulnerabilities
- ✅ Performance: No significant degradation
- ✅ Accessibility: WCAG 2.1 AA compliance where applicable

### Best Practices

1. **Communication**
   - Ask questions early if unclear
   - Provide regular updates on progress
   - Be responsive to feedback

2. **Testing**
   - Write unit tests for backend changes
   - Write integration tests for complex features
   - Manual testing on multiple devices/browsers
   - Test edge cases and error scenarios

3. **Documentation**
   - Update README if adding new features
   - Add docstrings to functions and classes
   - Include inline comments for complex logic
   - Update API documentation

4. **Security**
   - Never commit secrets or API keys
   - Validate all user inputs
   - Follow OWASP guidelines
   - Report security issues privately

5. **Performance**
   - Optimize database queries
   - Minimize API calls
   - Use caching where appropriate
   - Profile and benchmark critical paths

## Technical Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL (production), SQLite (development)
- **ORM:** SQLAlchemy
- **AI:** Google Gemini API
- **ML:** YOLOv8, HuggingFace Transformers
- **Bot:** python-telegram-bot

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **State:** React Hooks
- **Routing:** React Router

### DevOps
- **Frontend Hosting:** Netlify
- **Backend Hosting:** Render
- **Database:** Neon PostgreSQL
- **CI/CD:** GitHub Actions

## Resources

### General
- [VishwaGuru Architecture](./ARCHITECTURE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [UI Guide](./UI_GUIDE.md)

### Learning Resources

**Backend (Python/FastAPI)**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Python Best Practices](https://docs.python-guide.org/)

**Frontend (React)**
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)

**Machine Learning**
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [Google Gemini API](https://ai.google.dev/docs)

**Web3/Blockchain** (for blockchain issue)
- [Ethereum Documentation](https://ethereum.org/en/developers/docs/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Web3.py Guide](https://web3py.readthedocs.io/)

**Testing**
- [Playwright Documentation](https://playwright.dev/)
- [Cypress Documentation](https://docs.cypress.io/)
- [pytest Documentation](https://docs.pytest.org/)

## Getting Help

### Communication Channels

1. **GitHub Issues**: Best for technical discussions
2. **Pull Request Comments**: For code review discussions
3. **GitHub Discussions**: For general questions (if enabled)

### Questions to Ask

When stuck, provide:
- What you're trying to achieve
- What you've tried so far
- Error messages or unexpected behavior
- Relevant code snippets
- Your development environment

## Recognition

Contributors who successfully complete ECWoC26 challenges will be:
- ✨ Credited in the project README
- 🏆 Recognized in ECWoC26 program
- 📝 Given strong recommendation letters (for significant contributions)
- 🌟 Potential to become project maintainers

## Tips for Success

### For First-Time Contributors

1. **Start Small**: Familiarize yourself with the codebase first
2. **Read Existing Code**: Understand patterns and conventions
3. **Ask Questions**: No question is too small
4. **Be Patient**: Complex issues take time
5. **Communicate**: Keep maintainers updated

### For Complex Issues

1. **Break It Down**: Divide into smaller, manageable tasks
2. **Research First**: Understand the problem domain thoroughly
3. **Prototype**: Build a proof-of-concept first
4. **Iterate**: Get feedback early and often
5. **Document**: Keep track of decisions and trade-offs

### Time Management

- Most complex issues: 2-4 weeks
- Plan for 10-20 hours per week
- Set milestones and track progress
- Buffer time for code review and revisions

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All participants must:

- ✅ Be respectful and professional
- ✅ Welcome newcomers and diverse perspectives  
- ✅ Give and receive constructive feedback gracefully
- ✅ Focus on what's best for the community
- ❌ No harassment, discrimination, or trolling

Report any Code of Conduct violations to the maintainers.

## License

VishwaGuru is licensed under the **AGPL-3.0 License**. By contributing, you agree that your contributions will be licensed under the same license.

## Contact

- **Repository:** https://github.com/RohanExploit/VishwaGuru
- **Issues:** https://github.com/RohanExploit/VishwaGuru/issues
- **Maintainer:** @RohanExploit

---

## Quick Start Checklist

- [ ] Read this README completely
- [ ] Review [ECWOC26_COMPLEX_ISSUES.md](./ECWOC26_COMPLEX_ISSUES.md)
- [ ] Browse available issues labeled **ECWoC26**
- [ ] Set up development environment
- [ ] Choose an issue and comment your interest
- [ ] Wait for maintainer approval
- [ ] Create feature branch and start coding
- [ ] Write tests for your changes
- [ ] Update documentation
- [ ] Submit pull request
- [ ] Respond to code review
- [ ] Celebrate your contribution! 🎉

---

**Welcome to VishwaGuru! Let's build something amazing together! 🚀**

*Last updated: January 2026*

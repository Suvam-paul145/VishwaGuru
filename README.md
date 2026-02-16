# 🌍 VishwaGuru

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/Ewocs/VishwaGuru?style=social)
![GitHub forks](https://img.shields.io/github/forks/Ewocs/VishwaGuru?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Ewocs/VishwaGuru?style=social)

![GitHub issues](https://img.shields.io/github/issues/Ewocs/VishwaGuru)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Ewocs/VishwaGuru)
![GitHub last commit](https://img.shields.io/github/last-commit/Ewocs/VishwaGuru)
![GitHub code size](https://img.shields.io/github/languages/code-size/Ewocs/VishwaGuru)
![GitHub contributors](https://img.shields.io/github/contributors/Ewocs/VishwaGuru)

</div>

**VishwaGuru is an AI-powered platform designed to help users analyze civic issues and generate actionable solutions using modern web technologies and AI models.**


## ✨ Features

- 🤖 **AI-generated action plans**: Using Google Gemini to create WhatsApp messages, email drafts, and X (Twitter) posts.
- ⚡ **FastAPI-powered backend**: High-performance asynchronous API.
- 🎨 **Modern React + Vite frontend**: Responsive and user-friendly interface.
- 📱 **Telegram bot integration**: Report issues directly from your favorite messaging app.
- 🗄️ **SQLite (dev) & PostgreSQL (prod)**: Flexible database options for development and production.
- ☁️ **Cloud Native**: Designed for deployment on Netlify, Render, and Neon.
- 📍 **Spatial Deduplication**: Automatically detects nearby issues to prevent duplicates.
- 🔍 **Unified Detection**: AI-powered detection for potholes, garbage, vandalism, and more.
- 🏛️ **MLA Lookup**: Find your Maharashtra representative by pincode and file grievances.

---

## 🛠️ Project Setup (Local)

### 📥 Clone the Repository
```bash
git clone https://github.com/Ewocs/VishwaGuru.git
cd VishwaGuru
```

---

## ⚙️ Backend Setup

### Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 🔐 Environment Configuration
```bash
cp .env.example .env
```

Set the following in your `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_api_key
DATABASE_URL=sqlite:///./data/issues.db
FRONTEND_URL=http://localhost:5173
```

---

## 🎨 Frontend Setup
```bash
cd frontend
npm install
```

---

## 🏃‍♂️ Running Locally

| Service | Command | URL |
|------|--------|-----|
| Backend | PYTHONPATH=. python -m uvicorn backend.main:app --reload | http://localhost:8000 |
| Frontend | cd frontend && npm run dev | http://localhost:5173 |

---

## 🛠️ Tech Stack

- **Frontend**: React 18+, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (Dev), PostgreSQL (Prod via Neon)
- **AI/ML**: Google Gemini Pro, Hugging Face Inference API (CLIP), Ultralytics (YOLO)
- **Bot**: python-telegram-bot

---

## 🏗️ Architecture

VishwaGuru follows a modern client-server architecture:

1.  **Frontend (Netlify)**: A React application that communicates with the backend via REST APIs.
2.  **Backend (Render)**: A FastAPI server that handles logic, AI integrations, and database operations.
3.  **Database (Neon)**: A serverless PostgreSQL database for persistent storage.
4.  **AI Services**: Integrates Google Gemini for text generation and Hugging Face/Local ML for image analysis.

---

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed system design
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Step-by-step deployment instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guidelines for contributors
- [backend/README.md](backend/README.md) - Backend-specific details

---

## 📄 License

GNU Affero General Public License v3.0 (AGPL-3.0)

<div align="center">

![VishwaGuru Banner](https://img.shields.io/badge/VishwaGuru-Civic%20Engagement-blue?style=for-the-badge&logo=github)
![License](https://img.shields.io/badge/License-AGPL--3.0-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-18+-61dafb?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)

**Empowering India's youth to engage with democracy through AI-powered civic action** 🚀

</div>

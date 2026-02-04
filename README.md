# 🌍 VishwaGuru

<div align="center">

![VishwaGuru Banner](https://img.shields.io/badge/VishwaGuru-Civic%20Engagement-blue?style=for-the-badge&logo=github)
![License](https://img.shields.io/badge/License-AGPL--3.0-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-19+-61dafb?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi)

**Empowering India's youth to engage with democracy through AI-powered civic action** 🚀

[✨ Features](#-key-features) • [🛠️ Tech Stack](#-tech-stack) • [🏗️ Architecture](#-architecture) • [🏃 Local Setup](#-local-development-setup) • [☁️ Deployment](#-deployment-guide)

</div>

---

## 📖 About VishwaGuru

VishwaGuru is an open-source platform that **transforms civic engagement** in India. Using cutting-edge AI, it simplifies contacting representatives, filing grievances, and organizing community actions. Our mission is to make democracy accessible to every Indian citizen through technology.

---

## 🌟 Key Features

<table>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/🤖-AI--Powered-blue?style=for-the-badge" />
<br>
<strong>AI Action Plans</strong>
<br>
Generates personalized WhatsApp messages, emails, and tweets using Google Gemini API to effectively raise civic issues.
</td>
<td align="center">
<img src="https://img.shields.io/badge/📱-Multi--Platform-green?style=for-the-badge" />
<br>
<strong>Omnichannel Reporting</strong>
<br>
Report issues via a modern web interface or a seamless Telegram bot integration.
</td>
<td align="center">
<img src="https://img.shields.io/badge/⚡-Smart--Detection-orange?style=for-the-badge" />
<br>
<strong>Auto-Detection</strong>
<br>
Automatically detects issue categories (potholes, garbage, etc.) from uploaded images using computer vision.
</td>
</tr>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/📍-Spatial--Awareness-purple?style=for-the-badge" />
<br>
<strong>Location Intelligence</strong>
<br>
Identifies local representatives based on GPS coordinates and prevents duplicate reports with spatial deduplication.
</td>
<td align="center">
<img src="https://img.shields.io/badge/🌐-Local--Languages-red?style=for-the-badge" />
<br>
<strong>India-Centric</strong>
<br>
Built for Indian languages and governance systems, supporting English, Hindi, and Marathi.
</td>
<td align="center">
<img src="https://img.shields.io/badge/🔒-Secure--&-Scalable-yellow?style=for-the-badge" />
<br>
<strong>Production Ready</strong>
<br>
FastAPI backend, React frontend, and robust PostgreSQL database support.
</td>
</tr>
</table>

---

## ⚡ Performance Optimizations

VishwaGuru is built for speed and efficiency:

-   **Frontend Route Preloading**: Critical views like the Dashboard and Reporting forms are preloaded in the background, ensuring near-instant navigation.
-   **Image Upload Optimization**: Server-side image processing avoids redundant decoding, reducing CPU usage and latency by ~4x for large uploads.
-   **Spatial Indexing**: Efficient geospatial queries (O(k)) using bounding boxes ensure fast location-based searches.
-   **Caching**: aggressive caching strategies for recent issues and static assets.

---

## 🛠️ Tech Stack

### **Frontend**
- **Framework**: React 19 + Vite
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Maps**: Leaflet / React-Leaflet
- **PWA**: Vite PWA Plugin

### **Backend**
- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite (Dev) / PostgreSQL (Prod)
- **ORM**: SQLAlchemy
- **AI/ML**: Google Gemini API, Hugging Face, YOLO (Object Detection)
- **Async**: Uvicorn, Asyncio

### **Infrastructure**
- **Frontend Hosting**: Netlify
- **Backend Hosting**: Render
- **Database**: Neon (Serverless PostgreSQL)

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User] -->|Web/Mobile| Frontend[React Frontend]
    User -->|Chat| Bot[Telegram Bot]

    subgraph "VishwaGuru Cloud"
        Frontend -->|REST API| Backend[FastAPI Backend]
        Bot -->|Webhook| Backend

        Backend -->|Query| DB[(PostgreSQL/SQLite)]
        Backend -->|Inference| AI[AI Services]
    end

    AI -->|GenAI| Gemini[Google Gemini]
    AI -->|Vision| HF[Hugging Face / Local ML]
```

---

## 🏃 Local Development Setup

Follow these steps to run VishwaGuru on your local machine.

### **Prerequisites**
- Node.js (v18+) & npm
- Python (v3.12+)
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/Ewocs/VishwaGuru.git
cd VishwaGuru
```

### **2. Backend Setup**

1.  **Create a Virtual Environment**:
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your keys:
    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    GEMINI_API_KEY=your_google_gemini_api_key
    # Default uses SQLite, perfect for local dev
    DATABASE_URL=sqlite:///./data/issues.db
    ```

4.  **Run the Backend**:
    ```bash
    # Run from the project root
    PYTHONPATH=. python -m uvicorn backend.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    API Documentation: `http://localhost:8000/docs`.

### **3. Frontend Setup**

1.  **Navigate to Frontend Directory**:
    ```bash
    cd frontend
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```

3.  **Configure Environment**:
    Create a `.env` file in `frontend/`:
    ```bash
    cp .env.example .env
    ```
    Set the API URL:
    ```env
    VITE_API_URL=http://localhost:8000
    ```

4.  **Run the Frontend**:
    ```bash
    npm run dev
    ```
    The application will be running at `http://localhost:5173`.

---

## ☁️ Deployment Guide

VishwaGuru is optimized for a modern serverless stack.

| Component | Service | Tier |
|-----------|---------|------|
| **Frontend** | Netlify | Free |
| **Backend** | Render | Free |
| **Database** | Neon | Free |

### **Quick Deployment Overview**

1.  **Database (Neon)**:
    *   Create a Postgres project on [Neon](https://neon.tech).
    *   Get the connection string (e.g., `postgres://user:pass@host/db?sslmode=require`).

2.  **Backend (Render)**:
    *   Create a Web Service connected to your repo.
    *   **Build Command**: `pip install -r backend/requirements-render.txt`
    *   **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
    *   **Env Vars**: Set `DATABASE_URL` (from Neon), `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, and `FRONTEND_URL` (your Netlify URL).

3.  **Frontend (Netlify)**:
    *   Create a new site connected to your repo.
    *   **Base Directory**: `frontend`
    *   **Build Command**: `npm run build`
    *   **Publish Directory**: `frontend/dist`
    *   **Env Vars**: Set `VITE_API_URL` to your Render backend URL (e.g., `https://vishwaguru-backend.onrender.com`).

👉 **[Read the Full Deployment Guide](DEPLOYMENT_GUIDE.md)** for detailed, step-by-step instructions.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ for India 🇮🇳
</div>

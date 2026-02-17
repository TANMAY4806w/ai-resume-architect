# 📄 AI Resume Architect

**Intelligent ATS Optimization & AI-Powered Resume Rewrite Engine**

[![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini AI](https://img.shields.io/badge/Powered_by-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?logo=render&logoColor=white)](https://ai-resume-architect-qmrx.onrender.com/)

🌐 **Live Demo:** [ai-resume-architect-qmrx.onrender.com](https://ai-resume-architect-qmrx.onrender.com/)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **ATS Scoring** | Keyword-based & AI-powered ATS compatibility analysis |
| 🤖 **AI Optimization** | Gemini AI rewrites and enhances resume content with missing keywords |
| 📄 **Multi-Template PDF** | Generate professional resumes using LaTeX templates (Modern, Professional, Two-Column) |
| 📝 **DOCX Export** | Download optimized resumes in Word format |
| 💬 **Career Coach** | Interactive AI chat for personalized career advice |
| 📂 **Dual Input** | Upload PDF/DOCX or fill in details manually |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- LaTeX distribution (TeX Live / MiKTeX) for PDF generation
- [Google Gemini API Key](https://aistudio.google.com/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/TANMAY4806w/ai-resume-architect.git
cd ai-resume-architect

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## 🏗️ Project Structure

```
ai-resume-architect/
├── app.py                  # Main Streamlit application
├── modules/
│   ├── ui.py               # UI components & layout
│   ├── parser.py           # PDF/DOCX text extraction
│   ├── enhancer.py         # AI-powered resume enhancement
│   ├── scorer.py           # ATS scoring engine
│   ├── generator.py        # PDF (LaTeX) & DOCX generation
│   ├── converter.py        # Data format conversion
│   ├── chat.py             # AI Career Coach chatbot
│   └── prompts.py          # AI prompt templates
├── assets/
│   ├── style.css           # Premium UI styling
│   └── templates/          # LaTeX resume templates
├── Dockerfile              # Docker containerization
├── render.yaml             # Render deployment config
└── requirements.txt        # Python dependencies
```

## 🐳 Docker Deployment

```bash
docker build -t ai-resume-architect .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key ai-resume-architect
```

## ☁️ Deploy on Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Select **Docker** as the environment
5. Add environment variable: `GEMINI_API_KEY` = your key
6. Deploy! 🚀

## 🛠️ Tech Stack

- **Frontend:** Streamlit + Custom CSS
- **AI Engine:** Google Gemini (Flash)
- **PDF Generation:** LaTeX (pdflatex) + Jinja2 templating
- **DOCX Generation:** python-docx
- **Parsing:** pdfplumber, python-docx

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<p align="center">Built with ❤️ using Streamlit & Google Gemini AI</p>

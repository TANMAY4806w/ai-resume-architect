# AI-Powered Resume Builder & ATS Optimization Agent
## System Flow & Approach Documentation

---

### 🏗️ Architecture Overview

```
                ┌──────────────────┐
                │   User Input     │
                │  (PDF/DOCX/Form) │
                └────────┬─────────┘
                         │
                ┌────────▼─────────┐
                │  Resume Parser   │
                │  (pdfplumber /   │
                │  python-docx)    │
                └────────┬─────────┘
                         │ raw text
                ┌────────▼─────────┐
                │  ATS Scorer      │──── Initial Score
                │  (Keyword Match  │     + Missing Keywords
                │  + Gemini AI)    │
                └────────┬─────────┘
                         │ missing keywords
                ┌────────▼─────────┐
                │  AI Enhancer     │
                │  (Google Gemini) │──── Enhanced JSON
                │  Smart Keyword   │     with keywords_added
                │  Injection       │     & keywords_skipped
                └────────┬─────────┘
                         │ structured data
             ┌───────────┼───────────┐
             │           │           │
     ┌───────▼──┐  ┌─────▼────┐ ┌───▼──────┐
     │ LaTeX    │  │  DOCX    │ │ Re-Score │
     │ Template │  │ Generator│ │ (ATS v2) │
     │ Engine   │  │          │ │          │
     └───────┬──┘  └─────┬────┘ └───┬──────┘
             │           │          │
     ┌───────▼──┐  ┌─────▼────┐    │
     │  PDF     │  │  Word    │    │
     │  Output  │  │  Output  │    │
     └──────────┘  └──────────┘    │
                                   │
                    ┌──────────────▼──────────┐
                    │  Results Dashboard      │
                    │  • Score Before/After    │
                    │  • Keywords Analysis     │
                    │  • Document Downloads    │
                    │  • AI Career Coach Chat  │
                    └─────────────────────────┘
```

---

### 📋 System Flow (Step-by-Step)

#### Step 1: Input
- **Option A:** User uploads an existing resume (PDF or Word)
  - `pdfplumber` extracts text from PDFs
  - `python-docx` extracts text from DOCX files
- **Option B:** User fills in a manual entry form with:
  - Personal Information, Education, Work Experience, Projects, Skills

#### Step 2: ATS Scoring (Initial)
- Extracts keywords from both resume and job description
- Removes stopwords and noise
- Calculates keyword overlap percentage as the ATS score
- Gemini AI provides context-aware scoring for semantic matching
- Returns: **Initial ATS Score** + **List of Missing Keywords**

#### Step 3: AI-Based Enhancement
- Google Gemini AI receives:
  - Original resume text
  - Target job description
  - List of missing keywords
- AI intelligently:
  - Rewrites content for impact and clarity
  - Naturally injects missing keywords where contextually appropriate
  - Improves grammar, phrasing, and professional tone
  - Generates quantifiable achievement bullets
  - Tracks which keywords were added vs. skipped (with reasons)

#### Step 4: Template Selection
- 3 pre-integrated LaTeX templates:
  - **Modern Blue** — Clean, contemporary design
  - **Classic Professional** — Traditional corporate format
  - **Compact Two-Column** — Space-efficient layout
- All templates are ATS-optimized for readability

#### Step 5: Resume Generation
- **PDF:** LaTeX template engine (Jinja2 + pdflatex) generates professional PDFs
- **Word (DOCX):** python-docx generates an editable Word document
- Displays the final optimized ATS score

---

### 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend / UI | Streamlit + Custom CSS (Glassmorphism) |
| AI Engine | Google Gemini (Flash) API |
| PDF Generation | LaTeX (pdflatex) + Jinja2 Templating |
| DOCX Generation | python-docx |
| Resume Parsing | pdfplumber, python-docx |
| Deployment | Render (Docker) |

---

### ✨ Bonus Features Implemented

1. **Score Improvement Tracker** — Displays before & after ATS scores with improvement delta
2. **Feedback Chat** — AI Career Coach chatbot powered by Gemini for personalized advice
3. **Keyword Analysis** — Visual breakdown of added vs. missing keywords with styled tags
4. **Multiple Export Formats** — Both PDF and editable Word output
5. **Premium UI** — Glassmorphism design, animated gradients, responsive layout

---

### 📂 Project Structure

```
ai-resume-architect/
├── app.py                  # Main Streamlit application entry point
├── modules/
│   ├── ui.py               # UI components, header, sidebar, forms, results
│   ├── parser.py           # PDF/DOCX text extraction
│   ├── enhancer.py         # Gemini AI resume enhancement
│   ├── scorer.py           # ATS scoring engine (keyword + AI)
│   ├── generator.py        # PDF (LaTeX) & DOCX generation
│   ├── converter.py        # Data format conversion utilities
│   ├── chat.py             # AI Career Coach chatbot
│   └── prompts.py          # Centralized AI prompt templates
├── assets/
│   ├── style.css           # Premium CSS design system
│   └── templates/          # LaTeX resume templates (3 variants)
├── tests/                  # Unit tests
├── Dockerfile              # Docker containerization
├── render.yaml             # Render deployment config
└── requirements.txt        # Python dependencies
```

---

### 🚀 How to Run

```bash
git clone https://github.com/TANMAY4806w/ai-resume-architect.git
cd ai-resume-architect
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
streamlit run app.py
```

---

**GitHub:** https://github.com/TANMAY4806w/ai-resume-architect

**Developed by:** Tanmay

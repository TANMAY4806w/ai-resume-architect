import streamlit as st
from streamlit_option_menu import option_menu
import base64

def load_css():
    """Loads custom CSS if available."""
    try:
        with open("assets/style.css", "r") as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def setup_page():
    """Configures page settings."""
    st.set_page_config(page_title="ResumeAI — AI Resume Architect", page_icon="📄", layout="wide")
    load_css()
    
def get_template_map():
    """Returns available templates mapped to filenames."""
    return {
        "Modern Blue": "modern",
        "Classic Professional": "professional",
        "Compact Two-Column": "twocolumn"
    }

# ─── HERO HEADER ───────────────────────────────────────────────
def display_header():
    """Displays an animated hero header with badges."""
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">📄 AI Resume Architect</h1>
        <p class="hero-tagline">Intelligent ATS Optimization & AI-Powered Rewrite Engine</p>
        <div class="hero-badges">
            <span class="hero-badge">🎯 ATS Optimization</span>
            <span class="hero-badge">🤖 AI-Powered</span>
            <span class="hero-badge">📑 Multi-Template</span>
            <span class="hero-badge">💬 Career Coach</span>
        </div>
        <div class="hero-divider"></div>
    </div>
    """, unsafe_allow_html=True)

# ─── INPUT METHOD SELECTOR ─────────────────────────────────────
def select_input_method():
    """Input method selection with styled option menu."""
    return option_menu(
        menu_title=None,
        options=["Upload Resume", "Manual Entry"],
        icons=["cloud-upload-fill", "pencil-square"],
        orientation="horizontal",
        styles={
            "container": {"padding": "6px", "background": "transparent"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0px 6px",
                "border-radius": "12px",
                "font-weight": "600",
                "transition": "all 0.3s ease",
            },
            "nav-link-selected": {
                "border-radius": "12px",
                "font-weight": "700",
            },
        }
    )

# ─── UPLOAD FORM ───────────────────────────────────────────────
def render_upload_form():
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📂</span>
        <h3>Upload Document</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    return st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

# ─── MANUAL ENTRY FORM ────────────────────────────────────────
def render_manual_form():
    """Renders the detailed manual entry form with premium styling."""

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">✍️</span>
        <h3>Candidate Details</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    st.caption("Fill in your professional details below to generate an optimized resume.")
    
    # ─── 1. Personal Info ───
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.expander("👤 Personal Information", expanded=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name", placeholder="e.g. John Doe")
        role = c2.text_input("Target Role", placeholder="e.g. Software Engineer")
        
        c3, c4 = st.columns(2)
        email = c3.text_input("Email", placeholder="john@example.com")
        phone = c4.text_input("Phone", placeholder="+1 (555) 123-4567")
        
        c5, c6 = st.columns(2)
        linkedin = c5.text_input("LinkedIn URL", placeholder="linkedin.com/in/johndoe")
        github = c6.text_input("GitHub / Portfolio URL", placeholder="github.com/johndoe")
    st.markdown('</div><br>', unsafe_allow_html=True)

    # ─── 2. Education (Dynamic) ───
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c_h1, c_h2 = st.columns([0.85, 0.15])
    with c_h1: 
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🎓</span>
            <h3>Education</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if 'edu_count' not in st.session_state: st.session_state.edu_count = 1
    def add_edu(): st.session_state.edu_count += 1
    def remove_edu(): st.session_state.edu_count = max(1, st.session_state.edu_count - 1)
    
    with c_h2: 
        st.button("➕ Add", key="add_edu_btn", on_click=add_edu)

    edu_items = []
    for i in range(st.session_state.edu_count):
        st.markdown(f'<div class="entry-card">', unsafe_allow_html=True)
        c0_1, c0_2 = st.columns([0.9, 0.1])
        c0_1.markdown(f"**Education #{i+1}**")
        
        if st.session_state.edu_count > 1 and i == st.session_state.edu_count - 1:
            if c0_2.button("✖️", key="rem_edu_btn", on_click=remove_edu, help="Remove this entry"): 
                st.rerun()

        c1, c2 = st.columns(2)
        inst = c1.text_input("Institution", key=f"edu_inst_{i}", placeholder="e.g. MIT")
        deg = c2.text_input("Degree", key=f"edu_deg_{i}", placeholder="e.g. B.S. Computer Science")
        c3, c4 = st.columns(2)
        year = c3.text_input("Year", key=f"edu_year_{i}", placeholder="e.g. 2020 - 2024")
        score = c4.text_input("GPA / Score", key=f"edu_score_{i}", placeholder="e.g. 3.8/4.0")
        
        if inst:
            edu_items.append(f"{deg} from {inst} ({year}) | Score: {score}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div><br>', unsafe_allow_html=True)

    # ─── 3. Experience (Dynamic) ───
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c_h1, c_h2 = st.columns([0.85, 0.15])
    with c_h1: 
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">💼</span>
            <h3>Work Experience</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if 'exp_count' not in st.session_state: st.session_state.exp_count = 1
    def add_exp(): st.session_state.exp_count += 1
    def remove_exp(): st.session_state.exp_count = max(1, st.session_state.exp_count - 1)
    
    with c_h2: 
        st.button("➕ Add", key="add_exp_btn", on_click=add_exp)

    exp_items = []
    for i in range(st.session_state.exp_count):
        st.markdown(f'<div class="entry-card">', unsafe_allow_html=True)
        c0_1, c0_2 = st.columns([0.9, 0.1])
        c0_1.markdown(f"**Role #{i+1}**")
        
        if st.session_state.exp_count > 1 and i == st.session_state.exp_count - 1:
            if c0_2.button("✖️", key="rem_exp_btn", on_click=remove_exp, help="Remove this entry"):
                st.rerun()

        c1, c2 = st.columns(2)
        role_title = c1.text_input("Job Title", key=f"exp_role_{i}", placeholder="e.g. Software Engineer")
        company = c2.text_input("Company", key=f"exp_comp_{i}", placeholder="e.g. Google")
        duration = st.text_input("Duration", key=f"exp_dur_{i}", placeholder="e.g. Jan 2023 – Present")
        desc = st.text_area("Key Responsibilities & Achievements", key=f"exp_desc_{i}", height=100,
                            placeholder="Describe your key contributions, metrics, and impact...")
        
        if role_title:
            exp_items.append(f"Role: {role_title} at {company} ({duration})\nDetails: {desc}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div><br>', unsafe_allow_html=True)

    # ─── 4. Projects (Dynamic) ───
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c_h1, c_h2 = st.columns([0.85, 0.15])
    with c_h1: 
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🚀</span>
            <h3>Projects</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if 'proj_count' not in st.session_state: st.session_state.proj_count = 1
    def add_proj(): st.session_state.proj_count += 1
    def remove_proj(): st.session_state.proj_count = max(1, st.session_state.proj_count - 1)
    
    with c_h2: 
        st.button("➕ Add", key="add_proj_btn", on_click=add_proj)

    proj_items = []
    for i in range(st.session_state.proj_count):
        st.markdown(f'<div class="entry-card">', unsafe_allow_html=True)
        c0_1, c0_2 = st.columns([0.9, 0.1])
        c0_1.markdown(f"**Project #{i+1}**")
        
        if st.session_state.proj_count > 1 and i == st.session_state.proj_count - 1:
            if c0_2.button("✖️", key="rem_proj_btn", on_click=remove_proj, help="Remove this entry"):
                st.rerun()

        c1, c2 = st.columns(2)
        p_name = c1.text_input("Project Name", key=f"proj_name_{i}", placeholder="e.g. AI Chatbot")
        p_tech = c2.text_input("Tech Stack", key=f"proj_tech_{i}", placeholder="e.g. Python, React, AWS")
        p_link = st.text_input("Link", key=f"proj_link_{i}", placeholder="e.g. github.com/user/project")
        p_desc = st.text_area("Description", key=f"proj_desc_{i}", height=80,
                              placeholder="What does it do? What was your role?")
        
        if p_name:
            proj_items.append(f"Project: {p_name} ({p_tech})\nLink: {p_link}\nDetails: {p_desc}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div><br>', unsafe_allow_html=True)

    # ─── 5. Skills ───
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🛠️</span>
        <h3>Skills</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    langs = c1.text_area("Programming Languages", placeholder="e.g. Python, JavaScript, Java")
    libs = c2.text_area("Libraries / Frameworks", placeholder="e.g. React, TensorFlow, FastAPI")
    c3, c4 = st.columns(2)
    tools = c3.text_area("Tools / Platforms", placeholder="e.g. Docker, AWS, Git")
    soft = c4.text_area("Soft Skills", placeholder="e.g. Leadership, Communication")
    st.markdown('</div>', unsafe_allow_html=True)

    # Construct the raw text
    if name:
        text_parts = [
            f"Name: {name}",
            f"Target Role: {role}",
            f"Email: {email}",
            f"Phone: {phone}",
            f"LinkedIn: {linkedin}",
            f"GitHub: {github}",
            "\nEDUCATION:",
            "\n".join(edu_items),
            "\nEXPERIENCE:",
            "\n\n".join(exp_items),
            "\nPROJECTS:",
            "\n\n".join(proj_items),
            "\nSKILLS:",
            f"Languages: {langs}",
            f"Frameworks: {libs}",
            f"Tools: {tools}",
            f"Soft Skills: {soft}"
        ]
        return "\n".join(text_parts)
    
    return None

# ─── JOB DESCRIPTION INPUT ─────────────────────────────────────
def render_jd_input():
    st.markdown("""
    <div class="section-header" style="margin-top: 10px;">
        <span class="section-icon">🎯</span>
        <h3>Target Job Description</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    return st.text_area(
        "Paste the full job description here...",
        height=200,
        label_visibility="collapsed",
        placeholder="Paste the target job description here. Include all requirements, qualifications, and responsibilities for best ATS keyword matching..."
    )

# ─── SIDEBAR ───────────────────────────────────────────────────
def render_sidebar_settings():
    with st.sidebar:
        # Branded header
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">📄</div>
            <p class="brand-title">ResumeAI</p>
            <p class="brand-version">v2.0 • AI Architect</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="sidebar-accent-line"></div>', unsafe_allow_html=True)
        
        st.markdown("##### ⚙️ Configuration")
        template = st.selectbox(
            "Resume Template",
            list(get_template_map().keys()),
            help="Choose the visual style for your generated resume PDF."
        )
        
        # Template descriptions
        template_info = {
            "Modern Blue": "Clean, contemporary layout with blue accents and clear sections.",
            "Classic Professional": "Traditional format preferred by corporate recruiters.",
            "Compact Two-Column": "Space-efficient design that fits more content per page."
        }
        st.caption(f"ℹ️ {template_info.get(template, '')}")
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About this App"):
            st.markdown("""
            **AI Resume Architect** uses Google Gemini AI to:
            - 🎯 Analyze ATS keyword compatibility
            - 🤖 Rewrite & optimize resume content
            - 📄 Generate professional PDF & DOCX
            - 💬 Provide personalized career coaching
            
            *Built with Streamlit & Gemini AI*
            """)
        
        st.markdown("---")
        
        # Danger-styled reset button
        st.markdown('<div class="sidebar-danger-btn">', unsafe_allow_html=True)
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        return template

# ─── PDF PREVIEW ───────────────────────────────────────────────
def display_pdf_preview(pdf_path):
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📄</span>
        <h3>Document Preview</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf" style="border-radius: 14px; border: 1px solid var(--border-color);"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Preview unavailable: {str(e)}")

# ─── RESULTS DISPLAY ──────────────────────────────────────────
def display_results(score_before, score_after, missing, added, skipped, pdf_path, docx_path, filename_prefix="Resume"):
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📊</span>
        <h3>Optimization Report</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    
    # Score Cards
    improvement = score_after - score_before
    delta_html = f'<div class="score-delta">▲ {improvement:.1f}%</div>' if improvement > 0 else ''
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class="score-card before">
            <div class="score-label">Initial ATS Score</div>
            <div class="score-value">{score_before}<span class="score-suffix">%</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="score-card after">
            <div class="score-label">Optimized ATS Score</div>
            <div class="score-value">{score_after}<span class="score-suffix">%</span></div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class="score-card keywords">
            <div class="score-label">Keywords Added</div>
            <div class="score-value">{len(added)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Keyword Analysis
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔑</span>
        <h3>Keyword Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if added:
        pills_html = ''.join([f'<span class="keyword-pill added">✓ {kw}</span>' for kw in added])
        st.markdown(f"""
        <p style="font-weight: 600; margin-bottom: 6px; color: var(--success-color);">✅ Keywords Successfully Integrated</p>
        <div style="margin-bottom: 16px;">{pills_html}</div>
        """, unsafe_allow_html=True)
        
    if skipped:
        with st.expander("⏭️ Skipped Keywords (Context Mismatch)"):
            for item in skipped:
                if isinstance(item, dict):
                    st.write(f"- **{item.get('keyword')}**: {item.get('reason')}")
                else:
                    st.write(f"- {item}")
                    
    remaining = set(missing) - set(added)
    if remaining:
        with st.expander("⚠️ Outstanding Keywords"):
            pills_html = ''.join([f'<span class="keyword-pill missing">{kw}</span>' for kw in list(remaining)[:15]])
            st.markdown(f'<div>{pills_html}</div>', unsafe_allow_html=True)

    # Downloads
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📥</span>
        <h3>Download Documents</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    if pdf_path:
        with open(pdf_path, "rb") as f:
            c1.download_button("📄 Download PDF Resume", f, f"{filename_prefix}_Optimized.pdf", "application/pdf", use_container_width=True)
            
    if docx_path:
        with open(docx_path, "rb") as f:
            c2.download_button("📝 Download Word Resume", f, f"{filename_prefix}_Optimized.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)

# ─── FOOTER ────────────────────────────────────────────────────
def display_footer():
    """Displays a styled footer."""
    st.markdown("""
    <div class="app-footer">
        <p>Built with ❤️ using <strong>Streamlit</strong> & <strong>Google Gemini AI</strong></p>
        <p>AI Resume Architect — Your intelligent career companion</p>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import os
from dotenv import load_dotenv

import modules.ui as ui
from modules.parser import extract_text_from_pdf, extract_text_from_docx
from modules.enhancer import enhance_resume_content
from modules.converter import convert_resume_data_to_text
from modules.scorer import calculate_ats_score, calculate_ai_score
from modules.generator import generate_resume_pdf, generate_resume_docx

# Load environment variables
load_dotenv()

# Verify API Key
if not os.getenv("GEMINI_API_KEY"):
    st.error("⚠️ **Configuration Error**: `GEMINI_API_KEY` not found.")
    st.info("Please create a `.env` file with your valid API key to proceed.")
    st.stop()

def main():
    ui.setup_page()
    ui.display_header()

    # Sidebar Settings
    selected_template = ui.render_sidebar_settings()

    # Session State Initialization
    if 'resume_data' not in st.session_state: st.session_state.resume_data = None
    if 'ats_score_before' not in st.session_state: st.session_state.ats_score_before = None
    if 'ats_score_after' not in st.session_state: st.session_state.ats_score_after = None
    if 'pdf_path' not in st.session_state: st.session_state.pdf_path = None
    if 'docx_path' not in st.session_state: st.session_state.docx_path = None
    if 'missing_keywords' not in st.session_state: st.session_state.missing_keywords = []

    # Main Interaction Flow
    method = ui.select_input_method()
    raw_text = ""

    # Input Section
    if method == "Upload Resume":
        uploaded_file = ui.render_upload_form()
        if uploaded_file:
            if uploaded_file.name.endswith(".pdf"):
                raw_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                raw_text = extract_text_from_docx(uploaded_file)
    else:
        raw_text = ui.render_manual_form()

    # Job Description Input
    job_desc = ui.render_jd_input()

    st.markdown("<br>", unsafe_allow_html=True)

    # Analysis Action
    if st.button("🚀 Optimize Resume", use_container_width=True):
        if not raw_text:
            st.error("⚠️ Please upload a resume or fill in the manual details first.")
        elif not job_desc:
            st.error("⚠️ Please provide the Target Job Description.")
        else:
            process_resume(raw_text, job_desc, selected_template)

    # Results Display
    if st.session_state.ats_score_before is not None:
        display_results()

    # Footer
    ui.display_footer()

def process_resume(raw_text, job_desc, selected_template):
    with st.status("🚀 Optimizing your profile...", expanded=True) as status:
        
        # Step 1
        st.write("**Step 1/4** — 📊 Analyzing initial ATS compatibility...")
        score_before, missing = calculate_ats_score(raw_text, job_desc)
        st.write(f"   ↳ Initial Score: **{score_before}%**")
        
        # Step 2
        st.write("**Step 2/4** — 🤖 Optimizing content & keywords with AI...")
        ai_data = enhance_resume_content(raw_text, job_desc, missing_keywords=missing)
        
        if "error" in ai_data:
            status.update(label="❌ Optimization Failed", state="error", expanded=True)
            st.error(f"AI Error: {ai_data['error']}")
            st.stop()
        
        # Step 3
        st.write("**Step 3/4** — 📈 Verifying improvements...")
        enhanced_text = convert_resume_data_to_text(ai_data)
        score_after, _ = calculate_ats_score(enhanced_text, job_desc)
        
        # Step 4
        st.write("**Step 4/4** — 📄 Generating professional documents...")
        try:
            template_map = ui.get_template_map()
            fname = template_map.get(selected_template, "modern")
            
            pdf_path = generate_resume_pdf(ai_data, template_name=fname)
            docx_path = generate_resume_docx(ai_data)
            
            # Update Session State
            st.session_state.ats_score_before = score_before
            st.session_state.ats_score_after = score_after
            st.session_state.missing_keywords = missing
            st.session_state.keywords_added = ai_data.get('keywords_added', [])
            st.session_state.keywords_skipped = ai_data.get('keywords_skipped', [])
            st.session_state.pdf_path = pdf_path
            st.session_state.docx_path = docx_path
            st.session_state.resume_data = ai_data
            
            status.update(label="✅ Optimization Complete!", state="complete", expanded=False)
            st.success("🎉 Resume optimized successfully! Scroll down to see results.")
            st.rerun()

        except Exception as e:
            status.update(label="❌ Generation Failed", state="error", expanded=True)
            st.error(f"Document generation error: {str(e)}")

def display_results():
    # 1. Preview
    if st.session_state.pdf_path:
        ui.display_pdf_preview(st.session_state.pdf_path)
    
    # 2. Metrics & Files
    candidate_name = st.session_state.resume_data.get('name', 'Candidate').replace(" ", "_")
    ui.display_results(
        st.session_state.ats_score_before,
        st.session_state.ats_score_after,
        st.session_state.missing_keywords,
        st.session_state.keywords_added,
        st.session_state.keywords_skipped,
        st.session_state.pdf_path,
        st.session_state.docx_path,
        filename_prefix=candidate_name
    )
    
    with st.expander("🔍 View Raw Analysis Data"):
        st.json(st.session_state.resume_data)

    # 3. AI Chat
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💬</span>
        <h3>Career Coach Assistant</h3>
    </div>
    <div class="section-accent-line"></div>
    """, unsafe_allow_html=True)
    
    from modules.chat import FeedbackChat
    
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = FeedbackChat()
    
    context = st.session_state.resume_data if st.session_state.resume_data else "No resume processed yet."
    st.session_state.chat_session.render_chat_ui(str(context), "Career advice based on the optimization.")

if __name__ == "__main__":
    main()
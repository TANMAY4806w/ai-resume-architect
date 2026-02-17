import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)

class FeedbackChat:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def get_chat_history(self):
        """Retrieves or initializes chat history from session state."""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        return st.session_state.chat_history

    def add_message(self, role, content):
        """Adds a message to the chat history."""
        self.get_chat_history().append({"role": role, "content": content})

    def generate_response(self, user_query, resume_text, job_desc):
        """
        Generates a response from the AI based on the user's query and context.
        """
        # Build context
        context = f"""
        You are an expert AI Recruiter and Resume Coach. 
        You are helping a candidate improve their resume for a specific job.
        
        CONTEXT:
        RESUME CONTENT:
        {resume_text}
        
        TARGET JOB DESCRIPTION:
        {job_desc}
        
        USER QUERY:
        {user_query}
        
        INSTRUCTIONS:
        - Provide specific, actionable advice.
        - Be encouraging but honest.
        - Keep answers concise and relevant to the resume/JD provided.
        - If the user asks about the ATS score, explain how to improve it based on the missing keywords (if you can infer them).
        """
        
        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"

    def render_chat_ui(self, resume_text, job_desc):
        """
        Renders the chat interface in Streamlit.
        """
        st.markdown("### 💬 Chat with AI Recruiter")
        st.caption("Ask questions about your resume, or get specific improvement tips.")

        # Initialize chat history if not present
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I've analyzed your resume against the job description. Ask me anything! e.g., 'How can I improve my summary?' or 'What keywords am I missing?'"}
            ]

        # Display chat messages
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.generate_response(prompt, resume_text, job_desc)
                    st.markdown(response)
            
            # Add AI message
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

        # Download Button
        if len(st.session_state.chat_history) > 1:
            st.markdown("---")
            col1, col2 = st.columns([0.8, 0.2])
            with col2:
                if st.button("📥 Download Chat PDF"):
                    from modules.generator import generate_chat_pdf
                    pdf_path = generate_chat_pdf(st.session_state.chat_history)
                    if pdf_path:
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="Please click here to download",
                                data=f,
                                file_name="Career_Coach_Chat.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.error("Failed to generate PDF. Check if LaTeX is installed.")

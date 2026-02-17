import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(uploaded_file):
    """
    Extract text and hyperlinks from PDF using pdfplumber.
    """
    try:
        text = ""
        urls = []
        
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                
                if page.annots:
                    for annot in page.annots:
                        uri = annot.get('uri')
                        if uri:
                            urls.append(uri)
                            
        # Find URLs in text
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        found_urls = re.findall(url_pattern, text)
        urls.extend(found_urls)
        
        if urls:
            unique_urls = list(set(urls))
            text += "\n\nExtracted Links:\n"
            for url in unique_urls:
                if 'github.com' in url:
                    text += f"GitHub: {url}\n"
                elif 'linkedin.com' in url:
                    text += f"LinkedIn: {url}\n"
                else:
                    text += f"Link: {url}\n"
        
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(uploaded_file):
    """
    Extract text and hyperlinks from DOCX.
    """
    try:
        doc = Document(uploaded_file)
        text = ""
        urls = []
        
        for para in doc.paragraphs:
            text += para.text + "\n"
            for run in para.runs:
                if run.element.rPr is not None:
                    for child in run.element.rPr:
                        if 'hyperlink' in child.tag.lower():
                            try:
                                url = child.get('r:id')
                                if url:
                                    urls.append(url)
                            except:
                                pass
        
        if urls:
            text += "\n\nExtracted Links:\n" + "\n".join(set(urls))
        
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

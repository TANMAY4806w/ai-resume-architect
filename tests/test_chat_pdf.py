import sys
import os
import unittest
 
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from modules.generator import generate_chat_pdf
 
class TestChatPDF(unittest.TestCase):
    def test_generate_pdf(self):
        # Mock chat history
        history = [
            {"role": "user", "content": "How can I improve my resume?"},
            {"role": "assistant", "content": "You should add more keywords like Python and Docker."}
        ]
        
        # Generate PDF
        pdf_path = generate_chat_pdf(history)
        
        # Verify
        self.assertIsNotNone(pdf_path)
        self.assertTrue(os.path.exists(pdf_path))
        print(f"PDF generated successfully at: {pdf_path}")
        
if __name__ == '__main__':
    unittest.main()

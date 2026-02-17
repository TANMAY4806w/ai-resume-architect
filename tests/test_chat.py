import sys
import os
 
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
import unittest
from unittest.mock import MagicMock, patch
from modules.chat import FeedbackChat
 
class TestFeedbackChat(unittest.TestCase):
    @patch('modules.chat.genai.GenerativeModel')
    @patch('modules.chat.st')
    def test_generate_response(self, mock_st, mock_model_class):
        # Setup mock
        mock_model_instance = mock_model_class.return_value
        mock_response = MagicMock()
        mock_response.text = "This is a mocked response."
        mock_model_instance.generate_content.return_value = mock_response
        
        # Initialize
        chat = FeedbackChat()
        
        # Test
        response = chat.generate_response("How is my resume?", "Resume Content", "Job Description")
        
        # Verify
        self.assertEqual(response, "This is a mocked response.")
        mock_model_instance.generate_content.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()

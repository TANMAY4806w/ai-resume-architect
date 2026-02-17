import unittest
from unittest.mock import MagicMock, patch
from modules.parser import extract_text_from_pdf

class TestParser(unittest.TestCase):

    @patch('modules.parser.pdfplumber.open')
    def test_extract_text_from_pdf_success(self, mock_pdf_open):
        # Mock the pdf object and pages
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Sample Resume Text"
        mock_page.annots = [{'uri': 'https://linkedin.com/in/test'}]
        
        mock_pdf.pages = [mock_page]
        # Context manager mock
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf
        
        # Test file object (mocked)
        mock_file = MagicMock()
        
        result = extract_text_from_pdf(mock_file)
        
        self.assertIn("Sample Resume Text", result)
        self.assertIn("LinkedIn: https://linkedin.com/in/test", result)

    @patch('modules.parser.pdfplumber.open')
    def test_extract_text_from_pdf_empty(self, mock_pdf_open):
        mock_pdf = MagicMock()
        mock_pdf.pages = []
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf
        
        result = extract_text_from_pdf(MagicMock())
        
        self.assertEqual(result, "")

    def test_extract_text_from_pdf_error(self):
        # Test error handling without mocking pdfplumber to trigger exception
        # Passing a string instead of file object should trigger an error in open()
        result = extract_text_from_pdf("invalid_file_path")
        self.assertTrue(result.startswith("Error reading PDF"))

if __name__ == '__main__':
    unittest.main()

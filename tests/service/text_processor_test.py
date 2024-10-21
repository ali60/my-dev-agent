import unittest
from unittest.mock import patch, Mock
from service.text_processor import TextProcessor

class TestTextProcessor(unittest.TestCase):
    @patch('models.model_manager.ModelManager')
    def setUp(self, mock_model_manager):
        self.mock_model_manager = mock_model_manager.return_value
        self.text_processor = TextProcessor(self.mock_model_manager)

    def test_summarize_text(self):
        input_text = "This is a test text."
        expected_summary = "Test text summary"
        self.mock_model_manager.invoke_model.return_value = expected_summary
        result = self.text_processor.summarize_text(input_text)
        self.assertEqual(result, expected_summary)
        self.mock_model_manager.invoke_model.assert_called_once_with(f"Summarize the following text: \n{input_text}")

    def test_generate_response(self):
        input_text = "This is a test text."
        expected_response = "Test response"
        self.mock_model_manager.invoke_model.return_value = expected_response
        result = self.text_processor.generate_response(input_text)
        self.assertEqual(result, expected_response)
        self.mock_model_manager.invoke_model.assert_called_once_with(f"Generate a critical response for this text: \n{input_text}")

    def test_reword_response(self):
        input_text = "This is a test text."
        expected_reword = "Test reword"
        self.mock_model_manager.invoke_model.return_value = expected_reword
        result = self.text_processor.reword_response(input_text)
        self.assertEqual(result, expected_reword)
        self.mock_model_manager.invoke_model.assert_called_once_with(f"Reword this text: \n{input_text}")

    def test_rewrite_code(self):
        input_text = "def my_function():\n  pass"
        expected_rewrite = "Improved code"
        self.mock_model_manager.invoke_model.return_value = expected_rewrite
        result = self.text_processor.rewrite_code(input_text)
        self.assertEqual(result, expected_rewrite)
        self.mock_model_manager.invoke_model.assert_called_once_with(f"Enhance this code: \n{input_text}")

    def test_unit_test_code(self):
        input_text = "def my_function():\n  pass"
        expected_unit_test = "Unit test code"
        self.mock_model_manager.invoke_model.return_value = expected_unit_test
        result = self.text_processor.unit_test_code(input_text)
        self.assertEqual(result, expected_unit_test)
        self.mock_model_manager.invoke_model.assert_called_once_with(f"Write unit test for this code, use unittest, use given/then/when: \n{input_text}")

if __name__ == '__main__':
    unittest.main()
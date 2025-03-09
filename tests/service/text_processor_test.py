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
        self.mock_model_manager.invoke_model.assert_called_once()
        # Check that the prompt contains the input text
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_text, call_args)
        self.assertIn("summarize", call_args.lower())

    def test_critical_response(self):
        input_text = "This is a test text."
        expected_response = "Critical analysis"
        self.mock_model_manager.invoke_model.return_value = expected_response
        
        result = self.text_processor.critical_response(input_text)
        
        self.assertEqual(result, expected_response)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_text, call_args)
        self.assertIn("critical analysis", call_args.lower())

    def test_generate_response(self):
        input_text = "This is a test text."
        expected_response = "Generated response"
        self.mock_model_manager.invoke_model.return_value = expected_response
        
        result = self.text_processor.generate_response(input_text)
        
        self.assertEqual(result, expected_response)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_text, call_args)
        self.assertIn("response", call_args.lower())

    def test_rewrite_code(self):
        input_code = "def my_function():\n  pass"
        expected_rewrite = "Improved code"
        self.mock_model_manager.invoke_model.return_value = expected_rewrite
        
        result = self.text_processor.rewrite_code(input_code)
        
        self.assertEqual(result, expected_rewrite)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_code, call_args)
        self.assertIn("rewrite", call_args.lower())

    def test_generate_unit_test(self):
        input_code = "def my_function():\n  pass"
        expected_unit_test = "Unit test code"
        self.mock_model_manager.invoke_model.return_value = expected_unit_test
        
        result = self.text_processor.generate_unit_test(input_code)
        
        self.assertEqual(result, expected_unit_test)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_code, call_args)
        self.assertIn("unit test", call_args.lower())

    def test_list_typos(self):
        input_text = "This has a typo."
        expected_result = "Typo list"
        self.mock_model_manager.invoke_model.return_value = expected_result
        
        result = self.text_processor.list_typos(input_text)
        
        self.assertEqual(result, expected_result)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_text, call_args)
        self.assertIn("typos", call_args.lower())

    def test_code_review(self):
        input_code = "def my_function():\n  pass"
        expected_review = "Code review result"
        self.mock_model_manager.invoke_model.return_value = expected_review
        
        result = self.text_processor.code_review(input_code)
        
        self.assertEqual(result, expected_review)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_code, call_args)
        self.assertIn("code review", call_args.lower())

    def test_sec_review(self):
        input_code = "def my_function():\n  pass"
        expected_review = "Security review result"
        self.mock_model_manager.invoke_model.return_value = expected_review
        
        result = self.text_processor.sec_review(input_code)
        
        self.assertEqual(result, expected_review)
        self.mock_model_manager.invoke_model.assert_called_once()
        call_args = self.mock_model_manager.invoke_model.call_args[0][0]
        self.assertIn(input_code, call_args)
        self.assertIn("security review", call_args.lower())

    def test_null(self):
        input_text = "Just pass this through"
        expected_result = "Passed through"
        self.mock_model_manager.invoke_model.return_value = expected_result
        
        result = self.text_processor.null(input_text)
        
        self.assertEqual(result, expected_result)
        self.mock_model_manager.invoke_model.assert_called_once_with(input_text)


if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, Mock
import os
from configuration.config import config
from dotenv import load_dotenv
from models.gpt_models import ChatGPTModelInvoker

class TestChatGPTModelInvoker(unittest.TestCase):
    
    @patch('models.gpt_models.openai.ChatCompletion.create')  # Patch the correct path
    def setUp(self, mock_create):
        self.mock_create = mock_create
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = "test_api_key"
        # Setup the configuration here if needed, or use a fixture
        config = {
            "openai": {
                "modelId": "test_model",
                "max_tokens": 1000
            }
        }
        self.model_invoker = ChatGPTModelInvoker()

    def test_invoke_handles_exceptions(self):
        self.mock_create.side_effect = Exception("Test error")
        response = self.model_invoker.invoke("Hello")
        self.assertIsNone(response)

    def test_process_response_extracts_content(self):
        response = {"choices": [{"message": {"content": "Hello"}}]}
        processed_response = self.model_invoker.process_response(response)
        self.assertEqual(processed_response, "Hello")

    def test_process_response_handles_invalid_response(self):
        response = None
        processed_response = self.model_invoker.process_response(response)
        self.assertEqual(processed_response, "No valid response received.")

if __name__ == '__main__':
    unittest.main()

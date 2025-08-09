import unittest
from unittest.mock import patch, Mock
import boto3

from models.bedrock_models import ClaudeInvoker, LlamaInvoker, TitanInvoker
from models.gpt_models import ChatGPTModelInvoker
from models.model_manager import ModelManager

class TestModelManager(unittest.TestCase):
    @patch('models.model_manager.boto3.Session')
    def setUp(self, mock_session):
        self.mock_bedrock_runtime = Mock()
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.client.return_value = self.mock_bedrock_runtime
        
        self.config = {
            "region": "us-east-1",
            "default_model": "claude",
            "claude": {
                "modelId": "claude-3-sonnet",
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 1.0,
                "stop_sequences": []
            }
        }
        self.model_manager = ModelManager(self.config)

    def test_init_sets_attributes(self):
        self.assertEqual(self.model_manager.bedrock_runtime, self.mock_bedrock_runtime)
        self.assertEqual(self.model_manager.default_model, "claude")
        self.assertEqual(self.model_manager.max_tokens, 1000)
        self.assertEqual(self.model_manager.temperature, 0.7)

    def test_invoke_model_calls_correct_model(self):
        with patch.object(self.model_manager.models["claude"], "invoke") as mock_invoke:
            self.model_manager.invoke_model("Hello")
            mock_invoke.assert_called_once_with("Hello", {
                "prompt": "Hello",
                "max_tokens": 1000,
                "temperature": 0.7
            })

    def test_invoke_model_handles_default_model(self):
        self.model_manager.default_model = "nonexistent"
        with patch.object(self.model_manager.models["llama"], "invoke") as mock_invoke:
            self.model_manager.invoke_model("Hello")
            mock_invoke.assert_called_once_with("Hello", {
                "prompt": "Hello",
                "max_tokens": 1000,
                "temperature": 0.7
            })

    def test_invoke_model_processes_response(self):
        with patch.object(self.model_manager.models["claude"], "invoke") as mock_invoke:
            mock_invoke.return_value = {"response": "Hello"}
            with patch.object(self.model_manager.models["claude"], "process_response") as mock_process_response:
                self.model_manager.invoke_model("Hello")
                mock_process_response.assert_called_once_with({"response": "Hello"})


if __name__ == '__main__':
    unittest.main()
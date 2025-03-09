import unittest
from unittest.mock import patch, Mock
import boto3

from models.bedrock_models import ClaudeInvoker, LlamaInvoker, AmazonInvoker
from models.gpt_models import ChatGPTModelInvoker
from models.model_manager import ModelManager

class TestModelManager(unittest.TestCase):
    @patch('boto3.Session')
    def setUp(self, mock_boto3_session):
        self.mock_session = Mock()
        self.mock_bedrock_runtime = Mock()
        mock_boto3_session.return_value = self.mock_session
        self.mock_session.client.return_value = self.mock_bedrock_runtime
        
        self.config = {
            "profile": "test-profile",
            "region": "us-west-2",
            "default_model": "claude",
            "claude": {
                "max_tokens": 1000,
                "temperature": 0.7
            }
        }
        self.model_manager = ModelManager(self.config)

    def test_init_sets_attributes(self):
        self.assertEqual(self.model_manager.bedrock_runtime, self.mock_bedrock_runtime)
        self.assertEqual(self.model_manager.default_model, "claude")
        self.assertEqual(self.model_manager.max_tokens, 1000)
        self.assertEqual(self.model_manager.temperature, 0.7)
        
        # Verify session was created with correct parameters
        self.mock_session.client.assert_called_once()
        call_args = self.mock_session.client.call_args
        self.assertEqual(call_args[0][0], "bedrock-runtime")

    def test_invoke_model_calls_correct_model(self):
        with patch.object(self.model_manager.models["claude"], "invoke") as mock_invoke:
            mock_invoke.return_value = {"response": "Hello"}
            with patch.object(self.model_manager.models["claude"], "process_response") as mock_process:
                mock_process.return_value = "Processed response"
                
                result = self.model_manager.invoke_model("Hello")
                
                mock_invoke.assert_called_once_with("Hello", {
                    "prompt": "Hello",
                    "max_tokens": 1000,
                    "temperature": 0.7
                })
                mock_process.assert_called_once_with({"response": "Hello"})
                self.assertEqual(result, "Processed response")

    def test_invoke_model_handles_default_model(self):
        self.model_manager.default_model = "nonexistent"
        with patch.object(self.model_manager.models["llama"], "invoke") as mock_invoke:
            mock_invoke.return_value = {"response": "Hello"}
            with patch.object(self.model_manager.models["llama"], "process_response") as mock_process:
                mock_process.return_value = "Processed response"
                
                result = self.model_manager.invoke_model("Hello")
                
                mock_invoke.assert_called_once_with("Hello", {
                    "prompt": "Hello",
                    "max_tokens": 1000,
                    "temperature": 0.7
                })
                mock_process.assert_called_once_with({"response": "Hello"})
                self.assertEqual(result, "Processed response")

    def test_invoke_model_handles_none_response(self):
        with patch.object(self.model_manager.models["claude"], "invoke") as mock_invoke:
            mock_invoke.return_value = None
            
            result = self.model_manager.invoke_model("Hello")
            
            mock_invoke.assert_called_once()
            self.assertEqual(result, "Error while invoking the model")


if __name__ == '__main__':
    unittest.main()
import json
import unittest
from unittest.mock import patch, Mock, MagicMock
from models.bedrock_models import ClaudeInvoker, LlamaInvoker, AmazonInvoker
from botocore.exceptions import ClientError
from configuration.config import config

class TestInvoker(unittest.TestCase):
    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_claude(self, mock_make_api_call):
        bedrock_client = Mock()
        # Mocking the response body as a file-like object with a read() method
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            'content': [{'text': 'test completion'}]
        })
        bedrock_client.invoke_model.return_value = {'body': mock_response}

        invoker = ClaudeInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)
        
        self.assertEqual(response['content'][0]['text'], 'test completion')
        # Verify the request body structure
        call_args = bedrock_client.invoke_model.call_args[1]
        self.assertEqual(call_args['modelId'], config['claude']['modelId'])
        
        # Parse the body JSON to verify its structure
        body = json.loads(call_args['body'])
        self.assertEqual(body['anthropic_version'], "bedrock-2023-05-31")
        self.assertEqual(body['max_tokens'], config['claude']['max_tokens'])
        self.assertEqual(body['temperature'], config['claude']['temperature'])
        self.assertEqual(body['messages'][0]['content'][0]['text'], prompt)

    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_llama(self, mock_make_api_call):
        bedrock_client = Mock()
        # Mocking the response body as a file-like object with a read() method
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({'generation': 'test generation'})
        bedrock_client.invoke_model.return_value = {'body': mock_response}

        invoker = LlamaInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)

        self.assertEqual(response['generation'], 'test generation')
        # Verify the request body structure
        call_args = bedrock_client.invoke_model.call_args[1]
        self.assertEqual(call_args['modelId'], config['llama']['modelId'])
        
        # Parse the body JSON to verify its structure
        body = json.loads(call_args['body'])
        self.assertEqual(body['prompt'], prompt)
        self.assertEqual(body['max_gen_len'], config['llama']['max_tokens'])
        self.assertEqual(body['temperature'], config['llama']['temperature'])

    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_amazon(self, mock_make_api_call):
        bedrock_client = Mock()
        # Mocking the response body as a file-like object with a read() method
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({'results': [{'outputText': 'test output'}]})
        bedrock_client.invoke_model.return_value = {'body': mock_response}

        invoker = AmazonInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)

        self.assertEqual(response['results'][0]['outputText'], 'test output')
        # Verify the request body structure
        call_args = bedrock_client.invoke_model.call_args[1]
        self.assertEqual(call_args['modelId'], config['titan']['modelId'])
        
        # Parse the body JSON to verify its structure
        body = json.loads(call_args['body'])
        self.assertEqual(body['inputText'], prompt)
        self.assertEqual(body['textGenerationConfig']['maxTokenCount'], config['titan']['max_tokens'])
        self.assertEqual(body['textGenerationConfig']['temperature'], config['titan']['temperature'])

    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_error(self, mock_make_api_call):
        bedrock_client = Mock()
        error_response = {'Error': {'Code': '500', 'Message': 'Internal Server Error'}}
        bedrock_client.invoke_model.side_effect = ClientError(error_response, 'invoke_model')
        invoker = ClaudeInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)
        
        self.assertIsNone(response)
        # Verify the model ID
        call_args = bedrock_client.invoke_model.call_args[1]
        self.assertEqual(call_args['modelId'], config['claude']['modelId'])

    @patch('service.utils.clipboard_utils.ClipboardUtils.copy_to_clipboard')
    def test_handle_code_blocks(self, mock_copy):
        mock_copy.return_value = True
        bedrock_client = Mock()
        invoker = ClaudeInvoker(bedrock_client)
        
        # Test with code block
        text = "Here is some code:\n```python\ndef hello():\n    print('Hello')\n```\nEnd of code."
        result = invoker._handle_code_blocks(text)
        
        # Verify the text is returned unchanged
        self.assertEqual(result, text)
        # Verify copy_to_clipboard was called with the code block content
        mock_copy.assert_called_once_with("def hello():\n    print('Hello')")

    def test_process_response_claude(self):
        bedrock_client = Mock()
        invoker = ClaudeInvoker(bedrock_client)
        
        # Mock _handle_code_blocks to return unchanged text
        with patch.object(invoker, '_handle_code_blocks', return_value="Processed text"):
            response = {'content': [{'text': 'Test text'}]}
            result = invoker.process_response(response)
            
            self.assertEqual(result, "Processed text")
            invoker._handle_code_blocks.assert_called_once_with("Test text")

    def test_process_response_llama(self):
        bedrock_client = Mock()
        invoker = LlamaInvoker(bedrock_client)
        
        # Mock _handle_code_blocks to return unchanged text
        with patch.object(invoker, '_handle_code_blocks', return_value="Processed text"):
            response = {'generation': 'Test text'}
            result = invoker.process_response(response)
            
            self.assertEqual(result, "Processed text")
            invoker._handle_code_blocks.assert_called_once_with("Test text")

    def test_process_response_amazon(self):
        bedrock_client = Mock()
        invoker = AmazonInvoker(bedrock_client)
        
        # Mock _handle_code_blocks to return unchanged text
        with patch.object(invoker, '_handle_code_blocks', return_value="Processed text"):
            response = {'results': [{'outputText': 'Test text'}]}
            result = invoker.process_response(response)
            
            self.assertEqual(result, "Processed text")
            invoker._handle_code_blocks.assert_called_once_with("Test text")


if __name__ == '__main__':
    unittest.main()
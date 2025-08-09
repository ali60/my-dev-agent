import json
import unittest
from unittest.mock import patch, Mock, MagicMock
from models.bedrock_models import ClaudeInvoker, LlamaInvoker, TitanInvoker
from botocore.exceptions import ClientError
from configuration.config import config

class TestInvoker(unittest.TestCase):
    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_claude(self, mock_make_api_call):
        bedrock_client = Mock()
        # Mock the new Converse API response
        mock_response = {
            'output': {
                'message': {
                    'content': [
                        {
                            'text': 'test completion'
                        }
                    ]
                }
            }
        }
        bedrock_client.converse.return_value = mock_response

        invoker = ClaudeInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)
        
        self.assertEqual(response, mock_response)
        # Verify the Converse API was called with correct parameters
        bedrock_client.converse.assert_called_once_with(
            modelId=config['claude']['modelId'],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": config['claude']['max_tokens'],
                "temperature": config['claude']['temperature'],
                "topP": config['claude']['top_p'],
                "stopSequences": config['claude']['stop_sequences']
            }
        )

    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_llama(self, mock_make_api_call):
        bedrock_client = Mock()
        # Mocking the response body as a file-like object with a read() method
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({'generation': '[INST]test generation[/INST]'})
        bedrock_client.invoke_model.return_value = {'body': mock_response}

        invoker = LlamaInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)

        self.assertEqual(response, {'generation': '[INST]test generation[/INST]'})
        # Adjusting to use actual model configuration
        bedrock_client.invoke_model.assert_called_once_with(
            modelId=config['llama']['modelId'],
            body=json.dumps({
                "prompt": config['llama']['prompt_format'].format(prompt=prompt),
                "max_gen_len": config['llama']['max_tokens'],
                "temperature": config['llama']['temperature'],
                "top_p": config['llama']['top_p']
            })
        )

    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_titan(self, mock_make_api_call):
        bedrock_client = Mock()
        # Mocking the response body as a file-like object with a read() method
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({'results': [{'outputText': 'test output'}]})
        bedrock_client.invoke_model.return_value = {'body': mock_response}

        invoker = TitanInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)

        self.assertEqual(response, {'results': [{'outputText': 'test output'}]})
        # Adjusting to use actual model configuration
        bedrock_client.invoke_model.assert_called_once_with(
            modelId=config['titan']['modelId'],
            body=json.dumps({
                "inputText": config['titan']['prompt_format'].format(prompt=prompt),
                "textGenerationConfig": {
                    "maxTokenCount": config['titan']['max_tokens'],
                    "temperature": config['titan']['temperature'],
                    "topP": config['titan']['top_p']
                }
            })
        )

    @patch('botocore.client.BaseClient._make_api_call')
    def test_invoke_error(self, mock_make_api_call):
        bedrock_client = Mock()
        error_response = {'Error': {'Code': '500', 'Message': 'Internal Server Error'}}
        bedrock_client.converse.side_effect = ClientError(error_response, 'converse')
        invoker = ClaudeInvoker(bedrock_client)
        prompt = 'test prompt'
        response = invoker.invoke(prompt)
        
        self.assertIsNone(response)
        # Verify the Converse API was called with correct parameters
        bedrock_client.converse.assert_called_once_with(
            modelId=config['claude']['modelId'],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": config['claude']['max_tokens'],
                "temperature": config['claude']['temperature'],
                "topP": config['claude']['top_p'],
                "stopSequences": config['claude']['stop_sequences']
            }
        )

if __name__ == '__main__':
    unittest.main()

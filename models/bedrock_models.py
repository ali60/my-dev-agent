import json
from models.model_invoker import ModelInvoker
from botocore.exceptions import ClientError
from configuration.config import config


class ClaudeInvoker(ModelInvoker):
    def __init__(self, bedrock_client):
        model_config = config['claude']
        super().__init__(model_config["modelId"])
        self.bedrock_client = bedrock_client
        self.prompt_format = model_config["prompt_format"]
        self.max_tokens = model_config["max_tokens"]
        self.temperature = model_config["temperature"]
        self.top_p = model_config["top_p"]
        self.stop_sequences = model_config["stop_sequences"]

    def invoke(self, prompt, payload=None):
        try:
            # Use Bedrock Converse API for Claude 3 models
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": self.max_tokens,
                    "temperature": self.temperature,
                    "topP": self.top_p,
                    "stopSequences": self.stop_sequences
                }
            )
            return response
        except ClientError as e:
            print(f"Error: {e}")
            return None

    def invoke_stream(self, prompt, payload=None):
        """Invoke Claude model with streaming using Bedrock Converse API"""
        try:
            # Use Bedrock Converse Stream API for Claude 3 models
            response = self.bedrock_client.converse_stream(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": self.max_tokens,
                    "temperature": self.temperature,
                    "topP": self.top_p,
                    "stopSequences": self.stop_sequences
                }
            )
            return response
        except ClientError as e:
            print(f"Error: {e}")
            return None

    def process_stream_response(self, stream_response):
        """Process streaming response from Bedrock Converse Stream API"""
        if not stream_response:
            return
            
        try:
            for event in stream_response['stream']:
                if 'contentBlockDelta' in event:
                    delta = event['contentBlockDelta']['delta']
                    if 'text' in delta:
                        yield delta['text']
                elif 'messageStop' in event:
                    break
        except Exception as e:
            print(f"Error processing stream: {e}")
            return

    def process_response(self, response):
        if response and 'output' in response and 'message' in response['output']:
            content = response['output']['message']['content']
            if content and len(content) > 0:
                return content[0]['text'].strip()
        return "Error processing response"


class LlamaInvoker(ModelInvoker):
    def __init__(self, bedrock_client):
        model_config = config['llama']
        super().__init__(model_config["modelId"])
        self.bedrock_client = bedrock_client
        self.prompt_format = model_config["prompt_format"]
        self.max_tokens = model_config["max_tokens"]
        self.temperature = model_config["temperature"]
        self.top_p = model_config["top_p"]

    def invoke(self, prompt, payload=None):
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(
                    {
                        "prompt": self.prompt_format.format(prompt=prompt),
                        "max_gen_len": self.max_tokens,
                        "temperature": self.temperature,
                        "top_p": self.top_p,
                    }
                ),
            )
            response_body = json.loads(response["body"].read())
            return response_body
        except ClientError as e:
            print(f"Error: {e}")
            return None

    def process_response(self, response):
        return (
            response["generation"].replace("[INST]", "").replace("[/INST]", "").strip()
        )


class TitanInvoker(ModelInvoker):
    def __init__(self, bedrock_client):
        model_config = config['titan']
        super().__init__(model_config["modelId"])
        self.bedrock_client = bedrock_client
        self.prompt_format = model_config["prompt_format"]
        self.max_tokens = model_config["max_tokens"]
        self.temperature = model_config["temperature"]
        self.top_p = model_config["top_p"]

    def invoke(self, prompt, payload=None):
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(
                    {
                        "inputText": self.prompt_format.format(prompt=prompt),
                        "textGenerationConfig": {
                            "maxTokenCount": self.max_tokens,
                            "temperature": self.temperature,
                            "topP": self.top_p,
                        },
                    }
                ),
            )
            response_body = json.loads(response["body"].read())
            return response_body
        except ClientError as e:
            print(f"Error: {e}")
            return None

    def process_response(self, response):

        return response["results"][0]["outputText"].strip()

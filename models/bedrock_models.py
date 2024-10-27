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
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(
                    {
                        "prompt": self.prompt_format.format(prompt=prompt),
                        "max_tokens_to_sample": self.max_tokens,
                        "temperature": self.temperature,
                        "top_p": self.top_p,
                        "stop_sequences": self.stop_sequences,
                    }
                ),
            )
            response_body = json.loads(response["body"].read())
            return response_body
        except ClientError as e:
            print(f"Error: {e}")
            return None

    def process_response(self, response):
        return response["completion"].strip()


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

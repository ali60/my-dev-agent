import boto3
from botocore.config import Config
from models.bedrock_models import ClaudeInvoker, LlamaInvoker, TitanInvoker
from models.gpt_models import ChatGPTModelInvoker

class ModelManager:
    def __init__(self, config):
        # Configure retries for throttling
        boto3_config = Config(
            retries={
                'max_attempts': 6,
                'mode': 'standard'
            }
        )
        
        # Create bedrock-runtime client with retry config
        self.bedrock_runtime = boto3.client("bedrock-runtime", config=boto3_config, region_name=config["region"])

        self.models = {
            "claude": ClaudeInvoker(self.bedrock_runtime),
            "llama": LlamaInvoker(self.bedrock_runtime),
            "titan": TitanInvoker(self.bedrock_runtime),
            "openai": ChatGPTModelInvoker(),
        }
        self.default_model = config["default_model"]
        model_md = config[self.default_model]
        self.max_tokens = model_md["max_tokens"]
        self.temperature = model_md["temperature"]

    def invoke_model(self, prompt):
        model = self.models.get(self.default_model, self.models["llama"])
        payload = {
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        print("invoke model")
        response = model.invoke(prompt, payload)
        print("got response")
        if response is None:
            return "Error while invoking the model"
        return model.process_response(response)

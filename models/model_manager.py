import boto3
from models.bedrock_models import ClaudeInvoker, LlamaInvoker, TitanInvoker
from models.gpt_models import ChatGPTModelInvoker

class ModelManager:
    def __init__(self, config):
        self.bedrock_runtime = boto3.client("bedrock-runtime")
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
        response = model.invoke(prompt, payload)
        return model.process_response(response)

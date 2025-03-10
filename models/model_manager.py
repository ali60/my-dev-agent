import boto3
from botocore.config import Config
from models.bedrock_models import ClaudeInvoker, LlamaInvoker, AmazonInvoker
from models.gpt_models import ChatGPTModelInvoker
from service.utils.spinner import spinning_cursor


class ModelManager:
    def __init__(self, config):
        # Configure retries for throttling
        boto3_config = Config(retries={"max_attempts": 6, "mode": "standard"})

        # Create bedrock-runtime client with retry config
        session = boto3.Session(
            profile_name=config["profile"], region_name=config["region"]
        )

        self.bedrock_runtime = session.client("bedrock-runtime", config=boto3_config)

        self.models = {
            "claude": ClaudeInvoker(self.bedrock_runtime),
            "llama": LlamaInvoker(self.bedrock_runtime),
            "titan": AmazonInvoker(self.bedrock_runtime),
            "nova": AmazonInvoker(self.bedrock_runtime),
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
        
        # Use the spinning cursor while waiting for the model response
        with spinning_cursor(f"Invoking {self.default_model} model", spinner_type="moon"):
            response = model.invoke(prompt, payload)
            
        if response is None:
            return "Error while invoking the model"
        return model.process_response(response)

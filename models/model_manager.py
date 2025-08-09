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
        
        # Create boto3 session with the specified AWS profile (if provided)
        profile_name = config.get("profile")
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
        else:
            session = boto3.Session()  # Use default profile/credentials
        
        # Create bedrock-runtime client with retry config and profile
        self.bedrock_runtime = session.client("bedrock-runtime", config=boto3_config, region_name=config["region"])

        self.models = {
            "claude": ClaudeInvoker(self.bedrock_runtime),
            "llama": LlamaInvoker(self.bedrock_runtime),
            "titan": TitanInvoker(self.bedrock_runtime),
            "openai": ChatGPTModelInvoker(),
        }
        self.default_model = config["default_model"]
        
        # Get model configuration, fallback to claude if not found
        if self.default_model in config:
            model_md = config[self.default_model]
        else:
            print(f"Warning: Model '{self.default_model}' not found in config, using claude as fallback")
            model_md = config.get("claude", {"max_tokens": 1000, "temperature": 0.7})
            
        self.max_tokens = model_md.get("max_tokens", 1000)
        self.temperature = model_md.get("temperature", 0.7)

    def is_streaming_supported(self, model_name):
        """Check if streaming is supported for the given model"""
        # Claude 3 models and OpenAI models support streaming
        streaming_models = ["claude", "openai"]
        return model_name in streaming_models

    def invoke_model_stream(self, prompt):
        """Invoke model with streaming response using Bedrock Converse API"""
        model = self.models.get(self.default_model, self.models["llama"])
        
        # Check if the model supports streaming
        if hasattr(model, 'invoke_stream'):
            payload = {
                "prompt": prompt,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
            print("invoke model stream")
            try:
                stream_response = model.invoke_stream(prompt, payload)
                if stream_response and hasattr(model, 'process_stream_response'):
                    return model.process_stream_response(stream_response)
                else:
                    return iter([])  # Return empty iterator if no response
            except Exception as e:
                print(f"Streaming error: {e}")
                return iter([])  # Return empty iterator on error
        else:
            # Fallback to regular invoke if streaming not supported
            print("streaming not supported, falling back to regular invoke")
            try:
                response = self.invoke_model(prompt)
                return iter([response])  # Return single response as iterator
            except Exception as e:
                print(f"Fallback error: {e}")
                return iter([])  # Return empty iterator on error

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

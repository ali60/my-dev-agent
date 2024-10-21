from models.model_invoker import ModelInvoker
import openai
import os
from configuration.config import config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ChatGPTModelInvoker(ModelInvoker):
    def __init__(self):
        model_config = config["openai"]
        self.model_id = model_config["modelId"]
        self.max_tokens = model_config["max_tokens"]
        super().__init__(model_id=self.model_id)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def invoke(self, prompt, payload=None):
        try:
            response = openai.ChatCompletion.create(
                model=self.model_id,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
            )
            return response
        except Exception as e:
            print(f"Error invoking OpenAI model {self.model_id}: {e}")
            return None

    def process_response(self, response):
        if response and "choices" in response:
            return response["choices"][0]["message"]["content"].strip()
        return "No valid response received."

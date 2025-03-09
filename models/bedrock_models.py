# models/bedrock_models.py
import json
import re
from rich import print as rprint
from service.utils.clipboard_utils import ClipboardUtils
from botocore.exceptions import ClientError
from configuration.config import config


class BaseInvoker:
    def __init__(self, bedrock_client, model_config):
        self.bedrock_client = bedrock_client
        self.model_id = model_config["modelId"]

    def _invoke_with_profile(self, body):
        """Helper method to invoke model"""
        try:
            kwargs = {"modelId": self.model_id, "body": json.dumps(body)}
            return self.bedrock_client.invoke_model(**kwargs)
        except ClientError as e:
            print(f"Error invoking model: {e}")
            raise

    def _handle_code_blocks(self, text):
        """Extract and handle code blocks from response text"""
        try:
            # Extract code blocks
            code_blocks = re.findall(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)

            if code_blocks:
                # Copy the first code block to clipboard
                code = code_blocks[0].strip()
                if ClipboardUtils.copy_to_clipboard(code):
                    rprint("[bold green]Code block copied to clipboard![/bold green]")

                    # If there are multiple code blocks, show a message
                    if len(code_blocks) > 1:
                        rprint(
                            "[yellow]Multiple code blocks found. First block copied to clipboard.[/yellow]"
                        )
                        rprint("[yellow]Available code blocks:[/yellow]")
                        for i, block in enumerate(code_blocks, 1):
                            preview = block[:60] + "..." if len(block) > 60 else block
                            rprint(f"[cyan]Block {i}:[/cyan] {preview}")
                else:
                    rprint(
                        "[bold yellow]Warning: Could not copy code to clipboard[/bold yellow]"
                    )

            return text

        except Exception as e:
            rprint(f"[bold red]Error handling code blocks: {e}[/bold red]")
            return text


class ClaudeInvoker(BaseInvoker):
    def __init__(self, bedrock_client):
        model_config = config["claude"]
        super().__init__(bedrock_client, model_config)
        self.max_tokens = model_config["max_tokens"]
        self.temperature = model_config["temperature"]
        self.top_p = model_config["top_p"]
        self.stop_sequences = model_config["stop_sequences"]
        self.anthropic_version = "bedrock-2023-05-31"

    def invoke(self, prompt, payload=None):
        try:
            request_body = {
                "anthropic_version": self.anthropic_version,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "stop_sequences": self.stop_sequences,
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
            }

            response = self._invoke_with_profile(request_body)
            return json.loads(response["body"].read())

        except Exception as e:
            print(f"Error: {e}")
            return None

    def process_response(self, response):
        try:
            if not response or "content" not in response:
                raise ValueError(f"Invalid response format: {response}")

            text = response["content"][0]["text"].strip()
            return self._handle_code_blocks(text)

        except Exception as e:
            print(f"Error processing Claude response: {e}")
            print(f"Response content: {response}")
            raise


class LlamaInvoker(BaseInvoker):
    def __init__(self, bedrock_client):
        model_config = config["llama"]
        super().__init__(bedrock_client, model_config)
        self.max_tokens = model_config["max_tokens"]
        self.temperature = model_config["temperature"]
        self.top_p = model_config["top_p"]

    def invoke(self, prompt, payload=None):
        try:
            request_body = {
                "prompt": prompt,
                "max_gen_len": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            }

            response = self._invoke_with_profile(request_body)
            return json.loads(response["body"].read())

        except Exception as e:
            print(f"Error: {e}")
            return None

    def process_response(self, response):
        try:
            if not response or "generation" not in response:
                raise ValueError(f"Invalid response format: {response}")

            text = response["generation"].strip()
            return self._handle_code_blocks(text)

        except Exception as e:
            print(f"Error processing Llama response: {e}")
            print(f"Response content: {response}")
            raise


class AmazonInvoker(BaseInvoker):
    def __init__(self, bedrock_client):
        model_config = config["titan"]
        super().__init__(bedrock_client, model_config)
        self.max_tokens = model_config["max_tokens"]
        self.temperature = model_config["temperature"]
        self.top_p = model_config["top_p"]

    def invoke(self, prompt, payload=None):
        try:
            request_body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": self.max_tokens,
                    "temperature": self.temperature,
                    "topP": self.top_p,
                },
            }

            response = self._invoke_with_profile(request_body)
            return json.loads(response["body"].read())

        except Exception as e:
            print(f"Error: {e}")
            return None

    def process_response(self, response):
        try:
            if not response or "results" not in response or not response["results"]:
                raise ValueError(f"Invalid response format: {response}")

            text = response["results"][0]["outputText"].strip()
            return self._handle_code_blocks(text)

        except Exception as e:
            print(f"Error processing Titan response: {e}")
            print(f"Response content: {response}")
            raise

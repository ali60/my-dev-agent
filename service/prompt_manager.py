# service/prompt_manager.py
import subprocess
from service.text_processor import TextProcessor
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print as rprint
import pyperclip
import time

# service/prompt_manager.py
from service.utils.clipboard_utils import ClipboardUtils


class PromptManager:
    def __init__(self, config, model_manager):
        self.config = config
        self.model_manager = model_manager
        self.text_processor = TextProcessor(model_manager)
        self.console = Console()
        self.command_map = {
            "s": ("summarize", self.text_processor.summarize_text),
            "c": ("critical response", self.text_processor.critical_response),
            "r": ("response", self.text_processor.generate_response),
            "rc": ("rewrite_code", self.text_processor.rewrite_code),
            "uc": ("generate unit test", self.text_processor.generate_unit_test),
            "lt": ("list typos", self.text_processor.list_typos),
            "cr": ("code review", self.text_processor.code_review),
            "sr": ("security review", self.text_processor.sec_review),
            "n": ("null", self.text_processor.null),
        }

    def get_command_options(self):
        """Generate command options string from command_map"""
        options = []
        for key, value in self.command_map.items():
            description, _ = value
            options.append(f"[cyan]{key}[/cyan]:[yellow]{description}[/yellow]")
        return "[" + ", ".join(options) + "]"

    def display_markdown(self, text):
        """Display text with Markdown formatting"""
        try:
            markdown = Markdown(text)
            self.console.print(Panel(markdown, border_style="blue"))
        except Exception as e:
            rprint(f"[bold red]Error rendering markdown: {e}[/bold red]")
            print(text)

    def get_selected_text(self):
        """Get text from clipboard after user selects it"""
        rprint(
            "[bold yellow]Please select the text you want to process...[/bold yellow]"
        )

        # Store initial clipboard content
        return ClipboardUtils.paste_from_clipboard()

    def run(self):
        rprint(
            "[bold green]Press 's' to capture and summarize the selected text, or 'q' to quit.[/bold green]"
        )
        while True:
            command_options = self.get_command_options()
            rprint(command_options)

            user_input = input()
            if user_input.lower() == "q":
                rprint("[bold red]Exiting...[/bold red]")
                break

            text = (
                self.get_selected_text()
            )  # Using get_selected_text instead of get_clipboard_text
            if not text:
                rprint("[bold red]No text selected.[/bold red]")
                continue

            try:
                response = self.process_input(user_input, text)
                if response:
                    self.display_markdown(response)
                else:
                    rprint(
                        "[bold red]Failed to generate a summary or response.[/bold red]"
                    )
            except Exception as e:
                rprint(f"[bold red]Error while processing input: {e}[/bold red]")
                raise e

    def process_input(self, user_input, text):
        if user_input in self.command_map:
            _, command_func = self.command_map[user_input]
            return command_func(text)
        else:
            rprint("[bold red]Invalid choice. Please try again.[/bold red]")
            return None

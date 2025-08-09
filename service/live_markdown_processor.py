# service/live_markdown_processor.py
from rich import print as rprint
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
import time
import re


class LiveMarkdownProcessor:
    """Text processor that renders markdown in real-time during streaming"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.console = Console()

    def _stream_with_live_markdown(self, prompt, title="AI Response"):
        """Stream response with live markdown rendering"""
        rprint(f"\n[bold blue]🤖 {title}[/bold blue]")
        
        # Check if streaming is supported
        default_model = self.model_manager.default_model
        if not self.model_manager.is_streaming_supported(default_model):
            rprint(f"[yellow]⚠️  Streaming not supported for {default_model}, using regular response...[/yellow]")
            response = self.model_manager.invoke_model(prompt)
            self._display_final_markdown(response)
            return response
        
        # Stream with live markdown updates and scroll control
        response_chunks = []
        accumulated_text = ""
        
        try:
            # Create console with specific settings to control scrolling
            console = Console(force_terminal=True, legacy_windows=False)
            
            with Live(console=console, refresh_per_second=10, screen=True) as live:
                live.update(Panel(Text("🔄 Starting stream...", style="dim"), title=title, border_style="blue"))
                
                for chunk in self.model_manager.invoke_model_stream(prompt):
                    response_chunks.append(chunk)
                    accumulated_text += chunk
                    
                    try:
                        markdown = Markdown(accumulated_text)
                        live.update(Panel(markdown, title=f"{title} (streaming...)", border_style="blue"))
                    except Exception:
                        live.update(Panel(Text(accumulated_text), title=f"{title} (streaming...)", border_style="blue"))
                    
                    time.sleep(0.01)
                
                # Final update with completed status
                try:
                    markdown = Markdown(accumulated_text)
                    live.update(Panel(markdown, title=f"{title} ✅ Complete", border_style="green"))
                except Exception:
                    live.update(Panel(Text(accumulated_text), title=f"{title} ✅ Complete", border_style="green"))
            
            rprint(f"[green]✅ Response complete! ({len(response_chunks)} chunks, {len(accumulated_text)} characters)[/green]\n")
            return accumulated_text
            
        except Exception as e:
            rprint(f"\n[red]❌ Streaming error: {e}[/red]")
            rprint("[yellow]Falling back to regular response...[/yellow]")
            response = self.model_manager.invoke_model(prompt)
            self._display_final_markdown(response)
            return response

    def _display_final_markdown(self, text):
        """Display final markdown rendering"""
        try:
            markdown = Markdown(text)
            self.console.print(Panel(markdown, border_style="blue"))
        except Exception as e:
            rprint(f"[bold red]Error rendering markdown: {e}[/bold red]")
            print(text)

    def summarize_text(self, text):
        prompt = (
            "Please summarize the following text and format your response in markdown:\n\n"
            f"{text}\n\n"
            "Use markdown formatting including:\n"
            "- Headers for main points\n"
            "- Bullet points for key details\n"
            "- Bold/italic for emphasis where appropriate"
        )
        return self._stream_with_live_markdown(prompt, "📝 Text Summary")

    def critical_response(self, text):
        prompt = (
            "Please provide a critical analysis of the following text using markdown formatting:\n\n"
            f"{text}\n\n"
            "Include:\n"
            "- Main arguments\n"
            "- Supporting evidence\n"
            "- Potential counterarguments\n"
            "- Your evaluation"
        )
        return self._stream_with_live_markdown(prompt, "🔍 Critical Analysis")

    def generate_response(self, text):
        prompt = (
            "Please generate a detailed response to the following text using markdown formatting:\n\n"
            f"{text}"
        )
        return self._stream_with_live_markdown(prompt, "💭 AI Response")

    def rewrite_code(self, text):
        prompt = (
            "Please rewrite and improve the following code. Format your response in markdown:\n\n"
            f"```\n{text}\n```\n\n"
            "Include:\n"
            "- Improved code in a code block\n"
            "- Explanation of changes\n"
            "- Best practices applied"
        )
        return self._stream_with_live_markdown(prompt, "🔧 Code Rewrite")

    def generate_unit_test(self, text):
        prompt = (
            "Please generate unit tests for the following code using markdown formatting:\n\n"
            f"```\n{text}\n```\n\n"
            "Include:\n"
            "- Complete unit test code\n"
            "- Test cases for different scenarios\n"
            "- Explanation of test strategy"
        )
        return self._stream_with_live_markdown(prompt, "🧪 Unit Tests")

    def list_typos(self, text):
        prompt = (
            "Please identify and list any typos or grammatical errors in the following text:\n\n"
            f"{text}\n\n"
            "Format your response in markdown with:\n"
            "- List of errors found\n"
            "- Suggested corrections\n"
            "- Corrected version if needed"
        )
        return self._stream_with_live_markdown(prompt, "📝 Typo Check")

    def code_review(self, text):
        prompt = (
            "Please perform a comprehensive code review of the following code:\n\n"
            f"```\n{text}\n```\n\n"
            "Include in your markdown response:\n"
            "- Code quality assessment\n"
            "- Security considerations\n"
            "- Performance improvements\n"
            "- Best practices recommendations\n"
            "- Potential bugs or issues"
        )
        return self._stream_with_live_markdown(prompt, "👀 Code Review")

    def sec_review(self, text):
        prompt = (
            "Please perform a security review of the following code or text:\n\n"
            f"```\n{text}\n```\n\n"
            "Focus on:\n"
            "- Security vulnerabilities\n"
            "- Potential attack vectors\n"
            "- Security best practices\n"
            "- Recommendations for improvement\n"
            "Format your response in markdown."
        )
        return self._stream_with_live_markdown(prompt, "🔒 Security Review")

    def null(self, text):
        """Null operation - just return the text"""
        rprint("[dim]Null operation - returning original text[/dim]")
        return text

    def reword(self, text):
        prompt = (
            "Please reword and improve the following text while maintaining its meaning:\n\n"
            f"{text}\n\n"
            "Make it:\n"
            "- More clear and concise\n"
            "- Better structured\n"
            "- More engaging\n"
            "Format your response in markdown."
        )
        return self._stream_with_live_markdown(prompt, "✏️ Text Rewrite")

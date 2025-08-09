#!/usr/bin/env python3
"""
AI Agent with free text input and command support.

This version supports both free text conversation and command invocation using
backslash commands like \\s, \\lt, etc. It renders markdown in real-time as responses stream.
"""

from models.model_manager import ModelManager
from service.live_markdown_processor import LiveMarkdownProcessor
from service.utils.clipboard_utils import ClipboardUtils
from rich.console import Console
from rich import print as rprint
from configuration.config import config
import re
import time


class ChatAIAgent:
    """AI Agent with free text input and command support"""
    
    def __init__(self, config, model_manager):
        self.config = config
        self.model_manager = model_manager
        self.text_processor = LiveMarkdownProcessor(model_manager)
        self.console = Console()
        
        # Conversation context for follow-up questions
        self.conversation_history = []
        self.max_history_length = 10  # Keep last 10 exchanges
        
        self.command_map = {
            "\\s": ("summarize", self.text_processor.summarize_text),
            "\\c": ("critical response", self.text_processor.critical_response),
            "\\r": ("response", self.text_processor.generate_response),
            "\\rc": ("rewrite_code", self.text_processor.rewrite_code),
            "\\uc": ("generate unit test", self.text_processor.generate_unit_test),
            "\\lt": ("list typos", self.text_processor.list_typos),
            "\\cr": ("code review", self.text_processor.code_review),
            "\\sr": ("security review", self.text_processor.sec_review),
            "\\n": ("null", self.text_processor.null),
            "\\rw": ("reword", self.text_processor.reword),
            "\\f": ("follow-up", self.handle_followup_question),
        }
        self.categories = {
            "📝 Text": ["\\s", "\\rw", "\\lt"],
            "💻 Code": ["\\rc", "\\uc", "\\cr", "\\sr"], 
            "💬 Chat": ["\\r", "\\c", "\\f"],
            "🔧 Utils": ["\\n"]
        }

    def add_to_conversation_history(self, user_input, ai_response):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            "user": user_input,
            "assistant": ai_response,
            "timestamp": time.time()
        })
        
        # Keep only the last N exchanges to prevent memory bloat
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def get_conversation_context(self):
        """Get formatted conversation context for follow-up questions"""
        if not self.conversation_history:
            return ""
        
        context_parts = ["Previous conversation context:"]
        for i, exchange in enumerate(self.conversation_history[-3:], 1):  # Last 3 exchanges
            context_parts.append(f"\nExchange {i}:")
            context_parts.append(f"User: {exchange['user'][:200]}{'...' if len(exchange['user']) > 200 else ''}")
            context_parts.append(f"Assistant: {exchange['assistant'][:300]}{'...' if len(exchange['assistant']) > 300 else ''}")
        
        return "\n".join(context_parts)
    
    def handle_followup_question(self, question):
        """Handle follow-up questions with conversation context"""
        if not self.conversation_history:
            rprint("[yellow]⚠️  No previous conversation to follow up on. Starting fresh conversation...[/yellow]")
            return self.text_processor.generate_response(question)
        
        # Build context-aware prompt
        context = self.get_conversation_context()
        contextual_prompt = f"""{context}

Current follow-up question: {question}

Please answer the follow-up question considering the previous conversation context. Reference relevant parts of our previous discussion when helpful."""
        
        return self.text_processor._stream_with_live_markdown(contextual_prompt, "🔄 Follow-up Response")
    
    def show_conversation_status(self):
        """Show current conversation status"""
        if self.conversation_history:
            rprint(f"[dim]💭 Conversation history: {len(self.conversation_history)} exchanges • Use \\f for follow-up questions[/dim]")
        else:
            rprint(f"[dim]💭 New conversation • All responses will be saved for follow-up context[/dim]")

    def show_smart_help(self):
        """Smart contextual help display with progressive disclosure"""
        from rich.panel import Panel
        from rich.columns import Columns
        
        # Quick start commands (most common)
        quick_commands = ["\\s", "\\r", "\\cr", "\\rw", "\\f"]
        
        help_content = []
        help_content.append("[bold green]⚡ Quick Commands:[/bold green]")
        
        for cmd in quick_commands:
            if cmd in self.command_map:
                desc = self.command_map[cmd][0]
                help_content.append(f"  [cyan]{cmd:<4}[/cyan] {desc}")
        
        help_content.append("")
        help_content.append("[dim]💡 Tips:[/dim]")
        help_content.append("[dim]  • Type naturally for conversation[/dim]")
        help_content.append("[dim]  • Use \\<cmd> for specific functions[/dim]")
        help_content.append("[dim]  • Type 'help' for all commands[/dim]")
        
        panel = Panel(
            "\n".join(help_content),
            title="[bold blue]🤖 AI Agent Help[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        
        rprint(panel)
    
    def show_full_command_reference(self):
        """Complete command reference in categorized format"""
        from rich.panel import Panel
        from rich.columns import Columns
        
        panels = []
        
        for category, cmd_list in self.categories.items():
            content = []
            for cmd in cmd_list:
                if cmd in self.command_map:
                    desc = self.command_map[cmd][0]
                    content.append(f"[cyan]{cmd:<4}[/cyan] {desc}")
            
            if content:
                panel = Panel(
                    "\n".join(content),
                    title=f"[bold]{category}[/bold]",
                    border_style="dim",
                    padding=(0, 1)
                )
                panels.append(panel)
        
        rprint(Columns(panels, equal=True, expand=True))
    
    def show_contextual_suggestions(self, user_input):
        """Show relevant commands based on user input"""
        from rich.panel import Panel
        
        keywords = {
            "code": ["\\rc", "\\uc", "\\cr"],
            "text": ["\\s", "\\rw", "\\lt"],
            "review": ["\\cr", "\\sr", "\\c"],
            "fix": ["\\rc", "\\lt"],
            "write": ["\\rw", "\\rc"],
            "check": ["\\lt", "\\cr", "\\sr"],
            "test": ["\\uc", "\\cr"]
        }
        
        suggestions = set()
        user_lower = user_input.lower()
        
        for keyword, cmds in keywords.items():
            if keyword in user_lower:
                suggestions.update(cmds)
        
        if suggestions:
            content = []
            content.append(f"[dim]Based on '{user_input[:30]}...'[/dim]")
            content.append("")
            content.append("[bold green]💡 Suggested commands:[/bold green]")
            
            for cmd in list(suggestions)[:3]:
                if cmd in self.command_map:
                    desc = self.command_map[cmd][0]
                    content.append(f"  [cyan]{cmd}[/cyan] {desc}")
            
            panel = Panel(
                "\n".join(content),
                title="[bold yellow]🔍 Smart Suggestions[/bold yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
            rprint(panel)
    
    def show_autocomplete_preview(self, partial_input):
        """Show autocomplete suggestions for partial commands"""
        from rich.panel import Panel
        
        if not partial_input.startswith("\\"):
            return
            
        matches = [cmd for cmd in self.command_map.keys() 
                  if cmd.startswith(partial_input)]
        
        if len(matches) > 1:  # Only show if multiple matches
            content = []
            for cmd in matches[:5]:
                desc = self.command_map[cmd][0]
                # Highlight matching part
                highlighted = f"[bold cyan]{partial_input}[/bold cyan][cyan]{cmd[len(partial_input):]}[/cyan]"
                content.append(f"{highlighted} [dim]→[/dim] {desc}")
            
            panel = Panel(
                "\n".join(content),
                title="[bold green]⚡ Autocomplete[/bold green]",
                border_style="green",
                padding=(0, 1)
            )
            rprint(panel)

    def parse_input(self, user_input):
        """Parse user input to detect commands and extract text"""
        user_input = user_input.strip()
        
        # Sort commands by length (longest first) to handle multi-character commands correctly
        sorted_commands = sorted(self.command_map.keys(), key=len, reverse=True)
        
        # Check if input starts with a command
        for cmd in sorted_commands:
            if user_input.startswith(cmd):
                # Extract text after command (if any)
                remaining_text = user_input[len(cmd):].strip()
                return cmd, remaining_text
        
        # No command found, treat as free text
        return None, user_input

    def get_multiline_input(self):
        """Handle multiline input using paste mode"""
        rprint("[bold yellow]📋 Paste Mode Activated[/bold yellow]")
        rprint("[dim]Paste your multiline content, then press Ctrl+D (Unix/Mac) or Ctrl+Z+Enter (Windows)[/dim]")
        rprint("[dim]Or type your content line by line, then Ctrl+D when finished[/dim]")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            # Ctrl+D pressed - normal end of input
            pass
        except KeyboardInterrupt:
            rprint("\n[yellow]⏸️  Multiline input cancelled[/yellow]")
            return None
        
        if lines:
            content = "\n".join(lines)
            rprint(f"[green]✅ Captured {len(lines)} lines ({len(content)} characters)[/green]")
            return content
        else:
            rprint("[yellow]⚠️  No content entered[/yellow]")
            return None

    def handle_special_input_modes(self, user_input):
        """Handle special input modes like paste mode"""
        # Check for paste mode trigger
        if user_input.lower() in ['paste', 'multiline', 'ml']:
            return self.get_multiline_input()
        
        # Check for triple quotes trigger  
        if user_input.endswith("'''"):
            command_part = user_input[:-3].strip()
            rprint("[dim]📝 Multiline mode - type ''' on its own line to end[/dim]")
            lines = []
            while True:
                try:
                    line = input("... ")
                    if line.strip() == "'''":
                        break
                    lines.append(line)
                except KeyboardInterrupt:
                    rprint("\n[yellow]⏸️  Multiline input cancelled[/yellow]")
                    return None
            
            if lines:
                multiline_content = "\n".join(lines)
                return f"{command_part} {multiline_content}".strip()
        
        return user_input

    def get_text_for_processing(self, command, remaining_text):
        """Get text for processing based on command and remaining text"""
        if remaining_text:
            # Use the text provided after the command
            return remaining_text
        elif command:
            # Command without text, try to get from clipboard
            rprint("[bold yellow]Getting text from clipboard...[/bold yellow]")
            rprint("[dim]💡 Tip: You can also use 'paste' mode for multiline input[/dim]")
            clipboard_text = ClipboardUtils.paste_from_clipboard()
            if not clipboard_text:
                rprint("[bold red]❌ No text in clipboard.[/bold red]")
                rprint("[yellow]💡 Try: `\\s paste` for multiline input or `\\s '''` for triple-quote mode[/yellow]")
                return None
            return clipboard_text
        else:
            # Free text, return as is
            return remaining_text

    def show_streaming_info(self):
        """Show information about streaming capabilities"""
        default_model = self.model_manager.default_model
        streaming_supported = self.model_manager.is_streaming_supported(default_model)
        
        rprint(f"\n[bold blue]🚀 AI Agent with Free Text & Commands[/bold blue]")
        rprint(f"[dim]Current model: {default_model}[/dim]")
        
        if streaming_supported:
            rprint(f"[green]✅ Live markdown streaming enabled for {default_model}[/green]")
            rprint("[dim]You'll see formatted responses appear in real-time![/dim]")
        else:
            rprint(f"[yellow]⚠️  Streaming not supported for {default_model}[/yellow]")
            rprint("[dim]Using traditional response mode with final markdown rendering[/dim]")

    def run(self):
        """Main interaction loop with smart UI"""
        self.show_streaming_info()
        self.show_smart_help()
        
        while True:
            self.show_conversation_status()
            rprint(f"\n[dim]💬 Chat naturally or use commands (\\s, \\cr, \\f, etc.) • 'q' to quit • 'help' for all commands[/dim]")
            rprint(f"[dim]📝 For multiline: 'paste', '\\s '''', or '\\s paste'[/dim]")
            user_input = input("\n> ").strip()
            
            if user_input.lower() == "q":
                rprint("[bold red]👋 Exiting...[/bold red]")
                break
            
            if user_input.lower() == "help":
                rprint("\n[bold blue]📖 Complete Command Reference:[/bold blue]")
                self.show_full_command_reference()
                continue
                
            if user_input.lower() == "clear":
                self.conversation_history = []
                rprint("[green]✅ Conversation history cleared[/green]")
                continue
            
            if not user_input:
                continue
            
            # Handle special input modes (paste, multiline, triple quotes)
            processed_input = self.handle_special_input_modes(user_input)
            if processed_input is None:
                continue  # Input was cancelled
            elif processed_input != user_input:
                user_input = processed_input  # Input was modified (multiline mode)
                
            # Show autocomplete preview for partial commands
            if user_input.startswith("\\") and len(user_input) > 1:
                self.show_autocomplete_preview(user_input)
                
            try:
                command, remaining_text = self.parse_input(user_input)
                ai_response = None
                
                if command:
                    # Process command
                    text_to_process = self.get_text_for_processing(command, remaining_text)
                    if text_to_process:
                        rprint(f"\n[dim]🔧 Processing with command: {command}[/dim]")
                        _, command_func = self.command_map[command]
                        ai_response = command_func(text_to_process)
                else:
                    # Free text conversation - show contextual suggestions if helpful
                    if len(remaining_text) > 10:  # Only for substantial input
                        self.show_contextual_suggestions(remaining_text)
                    
                    rprint(f"\n[dim]💬 Free conversation[/dim]")
                    ai_response = self.text_processor.generate_response(remaining_text)
                
                # Save to conversation history if we got a response
                if ai_response:
                    self.add_to_conversation_history(user_input, ai_response)
                    
            except KeyboardInterrupt:
                rprint("\n[yellow]⏸️  Interrupted. Continue or type 'q' to quit.[/yellow]")
            except Exception as e:
                rprint(f"[bold red]❌ Error while processing input: {e}[/bold red]")
                # Don't raise in interactive mode, just continue


def main():
    """Main function to run the AI agent with free text and command support"""
    try:
        # Initialize model manager
        model_manager = ModelManager(config)
        
        # Create chat AI agent
        agent = ChatAIAgent(config, model_manager=model_manager)
        
        # Show welcome message
        rprint("[bold green]🚀 Welcome to AI Agent with Free Text & Commands![/bold green]")
        rprint("[dim]Type naturally or use commands like \\s, \\lt, etc.[/dim]")
        
        # Run the interactive session
        agent.run()
        
    except KeyboardInterrupt:
        rprint("\n[yellow]👋 Interrupted by user. Exiting...[/yellow]")
    except Exception as e:
        rprint(f"\n[bold red]❌ Error: {e}[/bold red]")
        raise


if __name__ == "__main__":
    main()

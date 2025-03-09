# utils/code_extractor.py
import re
from rich import print as rprint
from service.utils.clipboard_utils import ClipboardUtils

class CodeExtractor:
    @staticmethod
    def extract_and_copy_code(text):
        """
        Extract code blocks from markdown text and copy the first one to clipboard.
        Returns a tuple of (text, extracted_code)
        """
        # Extract code blocks
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
        
        if code_blocks:
            # Get the first code block
            code = code_blocks[0].strip()
            
            # Copy to clipboard using platform-specific method
            if ClipboardUtils.copy_to_clipboard(code):
                rprint("[bold green]Code block copied to clipboard![/bold green]")
            else:
                rprint("[bold yellow]Warning: Could not copy code to clipboard[/bold yellow]")
            
            return text, code
        
        return text, None

    @staticmethod
    def list_code_blocks(text):
        """
        Extract and return all code blocks from markdown text
        """
        return re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)

import unittest
from unittest.mock import patch, Mock, call, MagicMock
from service.prompt_manager import PromptManager
from service.text_processor import TextProcessor


class TestPromptManager(unittest.TestCase):
    @patch('service.prompt_manager.TextProcessor')
    @patch('service.prompt_manager.Console')
    def setUp(self, mock_console, mock_text_processor):
        self.mock_config = {"test_config": "value"}
        self.mock_model_manager = Mock()
        self.mock_text_processor_instance = mock_text_processor.return_value
        self.mock_console_instance = mock_console.return_value
        
        self.prompt_manager = PromptManager(self.mock_config, self.mock_model_manager)
        
        # Replace the text_processor with our mock
        self.prompt_manager.text_processor = self.mock_text_processor_instance
        self.prompt_manager.console = self.mock_console_instance

    def test_init(self):
        # Test that the PromptManager initializes correctly
        self.assertEqual(self.prompt_manager.config, self.mock_config)
        self.assertEqual(self.prompt_manager.model_manager, self.mock_model_manager)
        self.assertEqual(self.prompt_manager.text_processor, self.mock_text_processor_instance)
        self.assertEqual(self.prompt_manager.console, self.mock_console_instance)
        
        # Check that command_map contains expected commands
        self.assertIn("s", self.prompt_manager.command_map)
        self.assertIn("c", self.prompt_manager.command_map)
        self.assertIn("r", self.prompt_manager.command_map)
        self.assertIn("rc", self.prompt_manager.command_map)
        self.assertIn("uc", self.prompt_manager.command_map)

    def test_get_command_options(self):
        # Test that get_command_options returns a string with all commands
        options = self.prompt_manager.get_command_options()
        
        # Check that it's a string and contains expected command keys
        self.assertIsInstance(options, str)
        for key in self.prompt_manager.command_map.keys():
            self.assertIn(key, options)

    @patch('service.prompt_manager.Markdown')
    @patch('service.prompt_manager.Panel')
    def test_display_markdown(self, mock_panel, mock_markdown):
        # Test that display_markdown renders markdown correctly
        test_text = "# Test Markdown"
        mock_markdown_instance = mock_markdown.return_value
        mock_panel_instance = mock_panel.return_value
        
        self.prompt_manager.display_markdown(test_text)
        
        # Check that Markdown was created with the text
        mock_markdown.assert_called_once_with(test_text)
        # Check that Panel was created with the markdown
        mock_panel.assert_called_once_with(mock_markdown_instance, border_style="blue")
        # Check that console.print was called with the panel
        self.mock_console_instance.print.assert_called_once_with(mock_panel_instance)

    @patch('service.prompt_manager.Markdown')
    def test_display_markdown_error(self, mock_markdown):
        # Test error handling in display_markdown
        test_text = "# Test Markdown"
        mock_markdown.side_effect = Exception("Test error")
        
        with patch('service.prompt_manager.rprint') as mock_rprint:
            with patch('builtins.print') as mock_print:
                self.prompt_manager.display_markdown(test_text)
                
                # Check that rprint was called with an error message
                mock_rprint.assert_called_once()
                self.assertIn("Error rendering markdown", str(mock_rprint.call_args))
                # Check that regular print was called with the text
                mock_print.assert_called_once_with(test_text)

    @patch('service.prompt_manager.ClipboardUtils.paste_from_clipboard')
    @patch('service.prompt_manager.rprint')
    def test_get_selected_text(self, mock_rprint, mock_paste):
        # Test that get_selected_text returns clipboard content
        expected_text = "Selected text"
        mock_paste.return_value = expected_text
        
        result = self.prompt_manager.get_selected_text()
        
        # Check that rprint was called with a prompt
        mock_rprint.assert_called_once()
        self.assertIn("select the text", str(mock_rprint.call_args))
        # Check that paste_from_clipboard was called
        mock_paste.assert_called_once()
        # Check that the result is the expected text
        self.assertEqual(result, expected_text)

    def test_process_input_valid(self):
        # Test processing a valid input command
        test_text = "Test text"
        expected_result = "Processed result"
        
        # Set up the mock for summarize_text
        self.mock_text_processor_instance.summarize_text.return_value = expected_result
        
        # Call process_input with 's' command
        result = self.prompt_manager.process_input("s", test_text)
        
        # Check that summarize_text was called with the text
        self.mock_text_processor_instance.summarize_text.assert_called_once_with(test_text)
        # Check that the result is the expected result
        self.assertEqual(result, expected_result)

    def test_process_input_invalid(self):
        # Test processing an invalid input command
        test_text = "Test text"
        
        with patch('service.prompt_manager.rprint') as mock_rprint:
            result = self.prompt_manager.process_input("invalid", test_text)
            
            # Check that rprint was called with an error message
            mock_rprint.assert_called_once()
            self.assertIn("Invalid choice", str(mock_rprint.call_args))
            # Check that the result is None
            self.assertIsNone(result)

    @patch('builtins.input')
    @patch('service.prompt_manager.rprint')
    def test_run_quit(self, mock_rprint, mock_input):
        # Test that run exits when user inputs 'q'
        mock_input.return_value = "q"
        
        self.prompt_manager.run()
        
        # Check that rprint was called with exit message
        exit_call = mock_rprint.call_args_list[-1]
        self.assertIn("Exiting", str(exit_call))

    @patch('builtins.input')
    @patch('service.prompt_manager.rprint')
    def test_run_process_input(self, mock_rprint, mock_input):
        # Test that run processes input correctly
        mock_input.side_effect = ["s", "q"]  # First 's', then 'q' to exit
        
        # Mock get_selected_text and process_input
        with patch.object(self.prompt_manager, 'get_selected_text', return_value="Test text") as mock_get_text:
            with patch.object(self.prompt_manager, 'process_input', return_value="Processed result") as mock_process:
                with patch.object(self.prompt_manager, 'display_markdown') as mock_display:
                    self.prompt_manager.run()
                    
                    # Check that get_selected_text was called
                    mock_get_text.assert_called_once()
                    # Check that process_input was called with 's' and the text
                    mock_process.assert_called_once_with("s", "Test text")
                    # Check that display_markdown was called with the result
                    mock_display.assert_called_once_with("Processed result")

    @patch('builtins.input')
    @patch('service.prompt_manager.rprint')
    def test_run_no_text_selected(self, mock_rprint, mock_input):
        # Test handling when no text is selected
        mock_input.side_effect = ["s", "q"]  # First 's', then 'q' to exit
        
        # Mock get_selected_text to return None (no text selected)
        with patch.object(self.prompt_manager, 'get_selected_text', return_value=None) as mock_get_text:
            self.prompt_manager.run()
            
            # Check that get_selected_text was called
            mock_get_text.assert_called_once()
            # Check that rprint was called with an error message
            no_text_call = [call for call in mock_rprint.call_args_list if "No text selected" in str(call)]
            self.assertTrue(len(no_text_call) > 0)

    @patch('builtins.input')
    @patch('service.prompt_manager.rprint')
    def test_run_process_error(self, mock_rprint, mock_input):
        # Test error handling in run
        mock_input.side_effect = ["s", "q"]  # First 's', then 'q' to exit
        
        # Mock get_selected_text and process_input to raise an exception
        with patch.object(self.prompt_manager, 'get_selected_text', return_value="Test text") as mock_get_text:
            with patch.object(self.prompt_manager, 'process_input', side_effect=Exception("Test error")) as mock_process:
                with self.assertRaises(Exception):
                    self.prompt_manager.run()
                
                # Check that get_selected_text was called
                mock_get_text.assert_called_once()
                # Check that process_input was called
                mock_process.assert_called_once()
                # Check that rprint was called with an error message
                error_call = [call for call in mock_rprint.call_args_list if "Error while processing input" in str(call)]
                self.assertTrue(len(error_call) > 0)


if __name__ == '__main__':
    unittest.main()
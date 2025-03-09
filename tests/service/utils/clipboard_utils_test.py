import unittest
from unittest.mock import patch, Mock, call
import platform
import subprocess
import pyperclip
from service.utils.clipboard_utils import ClipboardUtils


class TestClipboardUtils(unittest.TestCase):
    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_macos(self, mock_popen, mock_platform):
        # Test copy_to_clipboard on macOS
        mock_platform.return_value = "Darwin"
        mock_process = Mock()
        mock_popen.return_value = mock_process
        
        test_text = "Test text"
        result = ClipboardUtils.copy_to_clipboard(test_text)
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that Popen was called with pbcopy
        mock_popen.assert_called_once()
        self.assertEqual(mock_popen.call_args[0][0], "pbcopy")
        # Check that communicate was called with the text
        mock_process.communicate.assert_called_once_with(test_text.encode('utf-8'))
        # Check that the result is True
        self.assertTrue(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_linux(self, mock_popen, mock_platform):
        # Test copy_to_clipboard on Linux
        mock_platform.return_value = "Linux"
        mock_process = Mock()
        mock_popen.return_value = mock_process
        
        test_text = "Test text"
        result = ClipboardUtils.copy_to_clipboard(test_text)
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that Popen was called with xclip
        mock_popen.assert_called_once()
        self.assertEqual(mock_popen.call_args[0][0][0], "xclip")
        # Check that communicate was called with the text
        mock_process.communicate.assert_called_once_with(test_text.encode('utf-8'))
        # Check that the result is True
        self.assertTrue(result)

    @patch('platform.system')
    @patch('pyperclip.copy')
    def test_copy_to_clipboard_windows(self, mock_pyperclip_copy, mock_platform):
        # Test copy_to_clipboard on Windows
        mock_platform.return_value = "Windows"
        
        test_text = "Test text"
        result = ClipboardUtils.copy_to_clipboard(test_text)
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that pyperclip.copy was called with the text
        mock_pyperclip_copy.assert_called_once_with(test_text)
        # Check that the result is True
        self.assertTrue(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    @patch('service.utils.clipboard_utils.rprint')
    def test_copy_to_clipboard_macos_error(self, mock_rprint, mock_popen, mock_platform):
        # Test error handling in copy_to_clipboard on macOS
        mock_platform.return_value = "Darwin"
        mock_popen.side_effect = Exception("Test error")
        
        test_text = "Test text"
        result = ClipboardUtils.copy_to_clipboard(test_text)
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that rprint was called with an error message
        mock_rprint.assert_called_once()
        self.assertIn("Error using pbcopy", str(mock_rprint.call_args))
        # Check that the result is False
        self.assertFalse(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_paste_from_clipboard_macos(self, mock_popen, mock_platform):
        # Test paste_from_clipboard on macOS
        mock_platform.return_value = "Darwin"
        mock_process = Mock()
        mock_process.communicate.return_value = (b"Test text", None)
        mock_popen.return_value = mock_process
        
        result = ClipboardUtils.paste_from_clipboard()
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that Popen was called with pbpaste
        mock_popen.assert_called_once()
        self.assertEqual(mock_popen.call_args[0][0], "pbpaste")
        # Check that communicate was called
        mock_process.communicate.assert_called_once()
        # Check that the result is the decoded text
        self.assertEqual(result, "Test text")

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_paste_from_clipboard_linux(self, mock_popen, mock_platform):
        # Test paste_from_clipboard on Linux
        mock_platform.return_value = "Linux"
        mock_process = Mock()
        mock_process.communicate.return_value = (b"Test text", None)
        mock_popen.return_value = mock_process
        
        result = ClipboardUtils.paste_from_clipboard()
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that Popen was called with xclip
        mock_popen.assert_called_once()
        self.assertEqual(mock_popen.call_args[0][0][0], "xclip")
        # Check that communicate was called
        mock_process.communicate.assert_called_once()
        # Check that the result is the decoded text
        self.assertEqual(result, "Test text")

    @patch('platform.system')
    @patch('pyperclip.paste')
    def test_paste_from_clipboard_windows(self, mock_pyperclip_paste, mock_platform):
        # Test paste_from_clipboard on Windows
        mock_platform.return_value = "Windows"
        mock_pyperclip_paste.return_value = "Test text"
        
        result = ClipboardUtils.paste_from_clipboard()
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that pyperclip.paste was called
        mock_pyperclip_paste.assert_called_once()
        # Check that the result is the text
        self.assertEqual(result, "Test text")

    @patch('platform.system')
    @patch('subprocess.Popen')
    @patch('service.utils.clipboard_utils.rprint')
    def test_paste_from_clipboard_macos_error(self, mock_rprint, mock_popen, mock_platform):
        # Test error handling in paste_from_clipboard on macOS
        mock_platform.return_value = "Darwin"
        mock_popen.side_effect = Exception("Test error")
        
        result = ClipboardUtils.paste_from_clipboard()
        
        # Check that platform.system was called
        mock_platform.assert_called_once()
        # Check that rprint was called with an error message
        mock_rprint.assert_called_once()
        self.assertIn("Error using pbpaste", str(mock_rprint.call_args))
        # Check that the result is None
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
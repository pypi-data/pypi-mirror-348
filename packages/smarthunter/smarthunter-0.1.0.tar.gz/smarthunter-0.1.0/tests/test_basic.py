#!/usr/bin/env python3
"""
Basic tests for smarthunter
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Mock the main function to avoid side effects
class TestSmartHunter(unittest.TestCase):
    def setUp(self):
        # Create a temporary binary file with some test strings
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.test_bin = self.temp_path / "test.bin"
        
        # Create a test binary with some embedded strings
        with open(self.test_bin, 'wb') as f:
            # Write some ASCII strings
            f.write(b"\x00\x00This is a test string\x00\x00")
            f.write(b"\x00Another test\x00")
            # Write a UTF-16 string
            f.write(b"F\x00l\x00a\x00g\x00{\x00t\x00e\x00s\x00t\x00}\x00")
            # Write some junk
            f.write(b"\x01\x02\x03\x04")
            # Write a potential flag
            f.write(b"flag{this_is_a_test_flag}\x00")
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    @patch('webbrowser.open')
    @patch('smarthunter.__main__.cluster')
    def test_hunt_function(self, mock_cluster, mock_browser):
        # Import here to avoid side effects
        from smarthunter.__main__ import hunt
        from argparse import Namespace
        
        # Mock the cluster function to return predictable results
        mock_cluster.return_value = [
            ["flag{this_is_a_test_flag}"],
            ["This is a test string", "Another test"],
            ["Flag{test}"]
        ]
        
        # Create args
        args = Namespace(
            binary=str(self.test_bin),
            out=None,
            json=True,
            no_open=False,
            depth=3
        )
        
        # Run the hunt function
        hunt(self.test_bin, args)
        
        # Check if HTML file was created
        html_file = self.test_bin.parent / f"{self.test_bin.name}_strings.html"
        self.assertTrue(html_file.exists())
        
        # Check if JSON file was created (since json=True)
        json_file = html_file.with_suffix(".json")
        self.assertTrue(json_file.exists())
        
        # Verify browser was opened
        mock_browser.assert_called_once()

if __name__ == "__main__":
    unittest.main() 
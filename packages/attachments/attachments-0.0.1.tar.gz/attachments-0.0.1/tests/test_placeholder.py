# tests/test_placeholder.py

import unittest

# Conditional import for your library's main module
# This structure helps if you run tests from the root directory or within the tests directory.
try:
    from src import attachments
except ImportError:
    # This allows running tests when the package is installed (e.g., in a virtual environment)
    import attachments

class TestAttachments(unittest.TestCase):

    def test_hello_function(self):
        self.assertEqual(attachments.hello(), "Hello from attachments!")

if __name__ == '__main__':
    unittest.main() 
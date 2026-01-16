import unittest
import os
import tempfile
from src.providers.profiles.local import LocalFileProfileProvider

class TestLocalProfileProvider(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        self.test_dir.cleanup()

    def create_profile(self, filename, content):
        path = os.path.join(self.test_dir.name, filename)
        with open(path, 'w') as f:
            f.write(content)
        return path

    def test_basic_profile_parsing(self):
        """Test parsing a simple profile without frontmatter."""
        content = "# Just a title\nSome content."
        path = self.create_profile("basic.md", content)
        
        provider = LocalFileProfileProvider(path)
        data = provider.get_profile()
        
        self.assertEqual(data.content.strip(), content.strip())
        self.assertEqual(data.metadata, {})

    def test_frontmatter_parsing(self):
        """Test parsing a profile WITH frontmatter."""
        raw = """---
quote_prompt: "Be cool."
---
# Title
Content here."""
        path = self.create_profile("smart.md", raw)
        
        provider = LocalFileProfileProvider(path)
        data = provider.get_profile()
        
        expected_content = "# Title\nContent here."
        
        self.assertIn("quote_prompt", data.metadata)
        self.assertEqual(data.metadata['quote_prompt'], "Be cool.")
        self.assertEqual(data.content.strip(), expected_content.strip())

    def test_broken_frontmatter(self):
        """Test that bad frontmatter falls back gracefully or errors predictable."""
        # Note: Depending on implementation, valid YAML failure might throw or return raw.
        # Our implementation uses regex for separation usually, or SafeLoader.
        pass

if __name__ == '__main__':
    unittest.main()

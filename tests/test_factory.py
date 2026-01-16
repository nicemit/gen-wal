import unittest
from src.factory import get_config_from_path

class TestFactoryLogic(unittest.TestCase):
    def setUp(self):
        self.config = {
            'image_provider': 'pollinations:image',
            'pollinations': {
                'text': {'model': 'openai'},
                'image': {'model': 'flux', 'seed': 42}
            },
            'llm': {
                'ollama': {'model': 'llama3'}
            },
            'local_dir': {
                'path': '/tmp/wallpapers'
            }
        }

    def test_get_config_simple(self):
        """Test simple root level access."""
        # hypothetical simple provider
        self.config['simple'] = {'key': 'value'}
        cfg, base = get_config_from_path(self.config, 'simple')
        self.assertEqual(base, 'simple')
        self.assertEqual(cfg, {'key': 'value'})

    def test_get_config_nested(self):
        """Test colon separated access."""
        cfg, base = get_config_from_path(self.config, 'pollinations:image')
        self.assertEqual(base, 'pollinations')
        self.assertEqual(cfg['model'], 'flux')
        self.assertEqual(cfg['seed'], 42)

    def test_get_config_deeply_nested(self):
        """Test retrieving LLM sub-config."""
        cfg, base = get_config_from_path(self.config, 'llm:ollama')
        self.assertEqual(base, 'llm')
        self.assertEqual(cfg['model'], 'llama3')

    def test_missing_config(self):
        """Test missing config returns empty dict but correct base."""
        cfg, base = get_config_from_path(self.config, 'pollinations:audio')
        self.assertEqual(base, 'pollinations')
        self.assertEqual(cfg, {}) # default empty dict on missing key

if __name__ == '__main__':
    unittest.main()

import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(start_dir='.', pattern='test_*.py')
    unittest.TextTestRunner().run(suite)

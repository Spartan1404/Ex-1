import unittest
from client_logic import create_chain, generate_chain_file, DEFAULT_CHARS


class ClientTests(unittest.TestCase):

    def test_create_chain_default(self):
        chain = create_chain()
        self.assertTrue(50 <= len(chain) <= 100)
        self.assertTrue(any(char.isspace() for char in chain))
        self.assertTrue(any(char.isalnum() for char in chain))

    def test_create_chain_custom_length(self):
        chain = create_chain(min_length=30, max_length=30)
        self.assertEqual(len(chain), 30)

    def test_create_chain_custom_chars(self):
        custom_chars = "ABC123"
        chain = create_chain(chars=custom_chars)
        self.assertTrue(all(char in custom_chars or char.isspace() for char in chain))

    def test_create_chain_min_max_spaces(self):
        chain = create_chain(min_spaces=1, max_spaces=1)
        self.assertEqual(chain.count(" "), 1)
        chain = create_chain(min_spaces=3, max_spaces=3)
        self.assertEqual(chain.count(" "), 3)

    def test_generate_chain_file(self):
        chains = generate_chain_file(amount=10, chain_min_length=20, chain_max_length=30, chain_chars=DEFAULT_CHARS, chain_min_spaces=2, chain_max_spaces=3)
        self.assertEqual(len(chains), 10)
        self.assertTrue(all((20 <= len(chain) <= 30) for chain in chains))
        self.assertTrue(all(any(char.isspace() for char in chain) for chain in chains))


if __name__ == '__main__':
    unittest.main()

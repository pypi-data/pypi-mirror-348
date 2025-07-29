import unittest
import sektorsim

class TestClass(unittest.TestCase):

    def test_method(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertEqual(sektorsim.a(3), 4)
        self.assertEqual(sektorsim.b(3), 5)


if __name__ == '__main__':
    unittest.main()

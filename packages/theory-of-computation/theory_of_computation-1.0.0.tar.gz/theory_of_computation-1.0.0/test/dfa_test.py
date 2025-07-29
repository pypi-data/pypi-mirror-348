import unittest
from theory_of_computation.dfa import dfa_substring_101

class TestDFASubstring101(unittest.TestCase):

    def test_dfa(self):
        self.assertEqual(dfa_substring_101("101"), "Accepted") 
        self.assertEqual(dfa_substring_101("0"), "Rejected")
        self.assertEqual(dfa_substring_101("11"), "Rejected")
        self.assertEqual(dfa_substring_101("1010"), "Accepted")
        self.assertEqual(dfa_substring_101("010101"), "Accepted")
        self.assertIsNone(dfa_substring_101("abc"))
        self.assertIsNone(dfa_substring_101("10#01"))
        self.assertEqual(dfa_substring_101("010"), "Rejected")

if __name__ == "__main__":
    unittest.main()
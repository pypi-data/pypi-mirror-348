from theory_of_computation.turing_machine_divisible_by_3 import turing_machine_divisible_by_3
import unittest

class TestDivisibility(unittest.TestCase):
    def test_cases(self):
        self.assertEqual(turing_machine_divisible_by_3("0"), True)
        self.assertEqual(turing_machine_divisible_by_3("11"), True)
        self.assertEqual(turing_machine_divisible_by_3("110"), True)
        self.assertEqual(turing_machine_divisible_by_3("10"), False)

if __name__ == "__main__":
    unittest.main()

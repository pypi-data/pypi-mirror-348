# from colorama import init, Fore, Style
from theory_of_computation.utils import print_invalid , print_accepted, print_rejected


def dfa_substring_101(input_string):
    """
    A DFA that accepts binary strings containing the substring '101'.
    Input:
        input_string: The binary string.

    Returns:
        "Accepted" if the string contains '101', "Rejected" if no.

    """
    for bit in input_string:
        if bit not in ('0', '1'):
            return None  # for invalid input

    current_state = "q0"

    for char in input_string:
        if current_state == "q0":
            if char == '0':
                current_state = "q0"
            elif char == '1':
                current_state = "q1"

        elif current_state == "q1":
            if char == '0':
                current_state = "q2"
            elif char == '1':
                current_state = "q1"

        elif current_state == "q2":
            if char == '0':
                current_state = "q0"
            elif char == '1':
                current_state = "q3"

        elif current_state == "q3":
            if char in ('0', '1'):
                current_state = "q3"

    if current_state == "q3":
        return "Accepted"
    else:
        return "Rejected"

if __name__ == "__main__":
    while True:
        binary_input = input("Enter a binary string (or 'x' to exit): ").strip()
        if binary_input.lower() == 'x':
            break
        result = dfa_substring_101(binary_input)
        if result is None:
            print_invalid()
        elif result == "Accepted":
            print_accepted()
        else:
            print_rejected()
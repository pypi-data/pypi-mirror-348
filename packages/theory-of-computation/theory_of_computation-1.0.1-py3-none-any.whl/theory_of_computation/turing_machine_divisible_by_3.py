from theory_of_computation.utils import print_invalid , print_accepted, print_rejected

def turing_machine_divisible_by_3(binary_input):
    """
    A Turing Machine that recognizes binary numbers divisible by 3.

    Input:
        input_string: The binary string.
    Output:
        True if the binary number is divisible by 3, False if no.
    """
    # States: q0 (start/accept), q1, q2
    # q0: Remainder 0 (accepting state)
    # q1: Remainder 1
    # q2: Remainder 2

    current_state = "q0"

    for bit in binary_input:
        if bit not in ('0', '1'):
            return None  # for invalid input

        if current_state == "q0":
            current_state = "q0" if bit == '0' else "q1"
        elif current_state == "q1":
            current_state = "q2" if bit == '0' else "q0"
        elif current_state == "q2":
            current_state = "q1" if bit == '0' else "q2"

    return current_state == "q0"

if __name__ == "__main__":
    while True:
        binary_input = input("Enter a binary number (or 'x' to exit): ").strip()
        if binary_input.lower() == 'x':
            break
        result = turing_machine_divisible_by_3(binary_input)
        if result is None:
            print_invalid()
        elif result:
            print_accepted()
        else:
            print_rejected()

from colorama import Fore, Style
from colorama import init

# Fore.RED and Fore.GREEN are used to color the output.
init(autoreset=True) # to reset colors after each print
def print_rejected():
    print(Fore.RED + "Rejected")

def print_accepted():
    print(Fore.GREEN + "Accepted")
def print_invalid():
    print(Fore.MAGENTA + "Invalid input: Only 0 and 1 are allowed.")
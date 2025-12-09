import sys
import password_cracker
from user_exception import UserException




def check_arguments():
    if len(sys.argv) < 4:
        raise UserException("Invalid number of arguments, reference readme on https://github.com/MrToxc/ParallelPasswordCracker")
    check_positive_number(sys.argv[1])
    check_positive_number(sys.argv[2])
    check_valid_hash(sys.argv[3])
    for argument in sys.argv[4:]:
        check_character_type(argument)

def check_character_type(character_key):
    if not password_cracker.CHAR_SETS.keys().__contains__(character_key):
        raise UserException(f"Invalid character key: {character_key}")


def check_valid_hash(target_hash):
    if len(target_hash) != len(password_cracker.DEFAULT_HASH):
        raise ValueError("target_hash is invalid")


def check_positive_number(value_str):
    try:
        number = int(value_str)
    except ValueError:
        raise UserException(f"'{value_str}' is not a valid number.")

    if number <= 0:
        raise UserException(f"Number has to be greatest than 0, Number: {number}")


if __name__ == "__main__":

    check_arguments()
    # TODO implement feature where user can specify salt, salt in next line is only for testing reasons
    password_cracker = password_cracker.PasswordCracker(max_chars = int(sys.argv[1]), max_processes = int(sys.argv[2]), target_hash = sys.argv[3], character_types = sys.argv[4:], salt = "ThisIsSalt")
    password_cracker.process_manager()

    result = password_cracker.get_result()
    if len(result) == 0:
        print("Password not found")
    else:
        print(f"Password is: {result}")
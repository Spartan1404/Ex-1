import string
import random

DEFAULT_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits


def create_chain(min_length: int = 50, max_length: int = 100, chars: str = DEFAULT_CHARS, min_spaces: int = 3, max_spaces: int = 5) -> str:
    """
    Generates a string of random characters
    :param min_length: The minimum size of the generated string
    :param max_length: The maximum size of the generated string
    :param chars: Characters to be used to generate the string
    :param min_spaces: Minimum amount of spaces (" ") to be included in the string
    :param max_spaces: Maximum amount of spaces (" ") to be included in the string
    :return: A string of random characters
    """
    length = random.randint(min_length, max_length)
    num_spaces = random.randint(min_spaces, max_spaces)
    chain = [random.choice(chars) for _ in range(length)]

    positions = set()
    while len(positions) != num_spaces:
        a = random.randint(1, length - 2)
        if not {a - 1, a, a + 1} & positions:
            positions.add(a)
    positions = list(positions)

    for p in positions:
        chain[p] = " "
    return ''.join(chain)


def generate_chain_file(amount: int = 1000000,
                        chain_min_length: int = 50,
                        chain_max_length: int = 100,
                        chain_chars: str = DEFAULT_CHARS,
                        chain_min_spaces: int = 3,
                        chain_max_spaces: int = 5,
                        filename: str = 'chains.txt') -> list[str]:
    """
    Create the given amount of random strings and saves them to a file named chains.txt
    :param filename: Name of the file that is going to be created
    :param amount: Amount of strings to be generated
    :param chain_min_length: The minimum size of the generated string
    :param chain_max_length: The maximum size of the generated string
    :param chain_chars: Characters to be used to generate the string
    :param chain_min_spaces: Minimum amount of spaces (" ") to be included in the string
    :param chain_max_spaces: Maximum amount of spaces (" ") to be included in the string
    :return: The list of generated strings
    """
    chain_list = [create_chain(chain_min_length, chain_max_length, chain_chars, chain_min_spaces, chain_max_spaces) for _ in
                  range(amount)]
    with open(filename, 'w') as chains:
        chains.write('\n'.join(chain_list))
    return chain_list

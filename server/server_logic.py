import logging


def calc_ponderation(chain: str, skip_chain: tuple[str] = ('aa', 'AA', 'Aa', 'aA')) -> float:
    """
    Calculates the ponderation metric of a given string by the formula (Number of letters * 1.5 + Number of numbers * 2) / number of spaces.
    :param chain: The main string to be processed
    :param skip_chain: Tuple containing substings. If any substring is found inside the main string the return value will be 1000
    :return: A float value representing the ponderation of the given string
    """
    if not chain:
        return 0
    logger = logging.getLogger('server')
    if any(substring in chain for substring in skip_chain):
        logger.info(f"Double 'a' rule detected on chain: '{chain}'")
        return 1000
    letters = digits = spaces = 0
    for c in chain:
        if c.isalpha():
            letters += 1
        elif c.isdigit():
            digits += 1
        else:
            spaces += 1
    if spaces == 0:
        return 0
    return (letters * 1.5 + digits * 2) / spaces

from typing import Union


def decimal_to_implied_probability(decimal: float) -> float:
    """Converts decimal odds to implied probability

    Args:
        decimal (float): Odds as a decimal

    Returns:
        float: implied probability
    """

    return (1 / decimal) * 100


def american_to_decimal(odds: int) -> float:
    """Converts american odds to decimal odds

    Args:
        odds (int): The American odds given as a whole number

    Returns:
        float: Decimal odds
    """

    if odds < 0:
        return 1 - (100 / odds)
    else:
        return 1 + (odds / 100)


def calc_margin(*args: float) -> float:
    """Calculates difference between odds

    Args:
        *args (float): decimal odds

    Returns:
        float: odds margin
    """

    return sum([decimal_to_implied_probability(i) for i in args])


def calc_margin_american(*args: int) -> float:
    """Calculates difference between odds

    Args:
        *args (int): american odds

    Returns:
        float: odds margin
    """

    return sum([(1 / american_to_decimal(i)) * 100 for i in args])


def find_arbitrage(*args: int, total=100) -> Union[tuple[dict, float], None]:
    """Given a set of American odds, returns the best arbitrage opportunity

    Args:
        *args (int): american odds
        total (int, optional): The total dollar amount available to wager. Defaults to 100.

    Returns:
        Union[tuple[dict, float], None]: A dictionary of the stakes per odds and the profit. If no arbitrage opportunity is found, returns None
    """

    margin = calc_margin_american(*args)
    if margin >= 100:
        return None

    stakes = {}

    for i, odds in enumerate(args):
        prob = decimal_to_implied_probability(american_to_decimal(odds))
        stake = total * prob / margin

        stakes[i] = stake

    profit = (american_to_decimal(args[0]) * stakes[0]) - total

    return stakes, profit

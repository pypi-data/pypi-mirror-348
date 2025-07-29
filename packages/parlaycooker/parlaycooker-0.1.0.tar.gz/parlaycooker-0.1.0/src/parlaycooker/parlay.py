import logging
from functools import reduce
from itertools import product
from operator import mul

from parlaycooker.config import MAX_COMBINATIONS, MAX_PARLAYS_PRINTED
from parlaycooker.model import Bet, Match, Parlay, ParlayGroup

logger = logging.getLogger("parlay")


def check_max_combinations(
    conditions: tuple[str, ...],
    max_combinations: int = MAX_COMBINATIONS,
) -> bool:
    outcomes_per_match = [len(condition) for condition in conditions]
    total_combinations = reduce(mul, outcomes_per_match, 1)

    logger.debug("Total combinations: %d", total_combinations)
    logger.debug("Max combinations: %d", max_combinations)

    if total_combinations > max_combinations:
        logger.warning(
            "Total combinations exceed the maximum limit: %d > %d",
            total_combinations,
            max_combinations,
        )
        print(
            "\033[1;31mWarning: Total combinations: \033[0m\033[1;33m{}\033[0m".format(
                total_combinations
            )
        )
        return False
    else:
        return True


def generate_parlays(
    matches: list[Match],
    conditions: tuple[str, ...],
) -> list[tuple[tuple[float, ...], tuple[str, ...]]]:
    rates = [(match.home, match.draw, match.away) for match in matches]
    filtered_rates = []

    logger.debug(f"Rates: {rates}")
    logger.debug(f"Conditions: {conditions}")

    for match_rates, condition in zip(rates, conditions):
        new_match_rate = []
        if "H" in condition.upper():
            new_match_rate.append(match_rates[0])
        if "D" in condition.upper():
            new_match_rate.append(match_rates[1])
        if "A" in condition.upper():
            new_match_rate.append(match_rates[2])

        new_match_rate = tuple(new_match_rate)
        filtered_rates.append(new_match_rate)

    logger.debug(f"Filtered Rates: {filtered_rates}")

    rate_combinations = product(*filtered_rates)
    outcome_combinations = product(*conditions)

    parlays = []

    for rate_combinations, outcome_combinations in zip(
        rate_combinations, outcome_combinations
    ):
        bets = []
        for i in range(len(matches)):
            match = matches[i]
            rate = rate_combinations[i]
            outcome = outcome_combinations[i]

            bet = Bet(
                match=match,
                rate=rate,
                outcome=outcome,
                probability=1 / rate,
            )
            bets.append(bet)

        parlay = Parlay(
            bets=bets,
            rate=reduce(mul, [bet.rate for bet in bets], 1),
            outcomes=[bet.outcome for bet in bets],
            probability=reduce(mul, [bet.probability for bet in bets], 1),
        )

        parlays.append(parlay)

    logger.debug(f"Generated Parlays: {len(parlays)}")
    parlays.sort(key=lambda x: x.rate, reverse=True)
    return ParlayGroup(parlays=parlays)


def print_parlays(
    parlays: ParlayGroup,
    max_parlays_printed: int = MAX_PARLAYS_PRINTED,
    bet_amount: float = 1.0,
):
    total_bets = len(parlays.parlays)
    total_matches = len(parlays.parlays[0].bets)

    print(
        "\033[1;36mTotal Matches: \033[1;33m",
        total_matches,
        "\033[0m",
        "\033[1;36mTotal Bets: \033[1;33m",
        total_bets,
        "\033[0m",
        "\033[1;36mShowing: \033[1;33m",
        min(MAX_PARLAYS_PRINTED, total_bets),
        "\033[0m",
        "\033[1;36mAmount Per Bet: \033[1;33m",
        f"$ {bet_amount:,.2f}",
        "\033[0m",
        "\033[1;36mTotal Bet: \033[1;33m",
        f"$ {bet_amount * total_bets:,.2f}",
        "\033[0m",
    )

    for parlay in parlays.parlays[:max_parlays_printed]:
        outcomes_str = (
            "\033[1;32m" + "-".join(bet.outcome for bet in parlay.bets) + "\033[0m"
        )
        print(
            f"\033[1;31mParlay Bet - \033[0mOutcomes: {outcomes_str} - "
            f"Rate: \033[1;34m{parlay.rate:8.2f}\033[0m - "
            f"Rate / Total Bets: \033[1;34m{parlay.rate / total_bets:8.2f}\033[0m - "
            f"Probability: \033[1;33m{parlay.probability * 100:8.3f} %\033[0m - "
            f"Earnings: \033[1;35m$ {bet_amount * parlay.rate:,.2f}\033[0m"
        )

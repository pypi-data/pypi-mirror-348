import logging
from time import perf_counter

from parlaycooker.config import MATCHES_FILE, MAX_COMBINATIONS
from parlaycooker.logger import setup_logging
from parlaycooker.parlay import check_max_combinations, generate_parlays, print_parlays
from parlaycooker.read_csv import read_matches_from_csv

setup_logging()
logger = logging.getLogger("parlaycooker")


def main():
    start = perf_counter()

    logger.debug("Starting Parlay Cooker")
    print("\033[1;32mHello from parlaycooker!\033[0m\n")

    try:
        matches, conditions = read_matches_from_csv(MATCHES_FILE)
    except Exception as e:
        print(
            "\033[1;31mError: Could not load matches from file, check the format.\033[0m",
            e,
        )
        return

    if not (matches and conditions):
        print(
            "\033[1;31mError: Could not load matches and conditions from file, check the format.\033[0m"
        )
        return

    if not check_max_combinations(conditions, max_combinations=MAX_COMBINATIONS):
        print(
            "\033[1;31mWarning: The number of combinations exceeds the maximum limit of \033[0m\033[1;33m{}\033[0m".format(
                MAX_COMBINATIONS
            )
        )
        return

    parlay_group = generate_parlays(matches, conditions)
    print_parlays(parlay_group)

    print(
        "\n\033[1;36mAverage Multiplier: \033[0m\033[1;33m{:.2f}\033[0m".format(
            parlay_group.avg_multiplier
        ),
        "\033[1;36mTotal Probability: \033[0m\033[1;33m{:.2f} %\033[0m".format(
            parlay_group.total_probability * 100
        ),
        "\033[1;36mExecution time: \033[0m\033[1;33m{:.2f} seconds\033[0m".format(
            perf_counter() - start
        ),
    )


if __name__ == "__main__":
    main()

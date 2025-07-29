from functools import cached_property

from pydantic import BaseModel


class Match(BaseModel):
    home_team: str
    away_team: str
    home: float
    draw: float
    away: float

    def __str__(self):
        # Highlight the home team in blue and the away team in red
        return f"\033[1;34m{self.home_team}\033[0m vs \033[1;31m{self.away_team}\033[0m: H: {self.home}, D: {self.draw}, A: {self.away}"


class Bet(BaseModel):
    match: Match
    rate: float
    outcome: str
    probability: float

    def __str__(self):
        # Highlight the outcome in green
        return f"{self.match.home_team} vs {self.match.away_team}: \033[1;32m{self.outcome}\033[0m @ {self.rate}"


class Parlay(BaseModel):
    bets: list[Bet]
    rate: float
    outcomes: list[str]
    probability: float

    def __str__(self):
        return f"Parlay Bet: {self.rate} with bets: {', '.join(str(bet) for bet in self.bets)}"


class ParlayGroup(BaseModel):
    parlays: list[Parlay]

    def __str__(self):
        return f"Parlay Group: {self.total_probability} with parlays: {', '.join(str(parlay) for parlay in self.parlays)}"

    @cached_property
    def total_probability(self):
        return sum(parlay.probability for parlay in self.parlays)

    @cached_property
    def avg_multiplier(self):
        return sum([parlay.rate / len(self.parlays) for parlay in self.parlays]) / len(
            self.parlays
        )

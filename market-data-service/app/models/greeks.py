from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Greeks:

    delta: float

    gamma: float

    theta: float

    vega: float
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OptionGreeks:
    iv: float | None

    delta: float | None

    gamma: float | None

    theta: float | None

    vega: float | None

    rho: float | None

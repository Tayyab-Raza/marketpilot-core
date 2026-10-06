"""Extension interfaces for proprietary/private analytics packages."""
from __future__ import annotations
from typing import Protocol


class TrapModel(Protocol):
    def score(self, technical: dict, fno: dict, context: dict) -> dict: ...


class ForecastModel(Protocol):
    def predict(self, features: dict) -> dict: ...


class StrategyModel(Protocol):
    def generate(self, technical: dict, fno: dict, regime: dict, forecast: dict, traps: dict) -> dict: ...

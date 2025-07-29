"""
Part of sopel-rep

Copyright 2024 dgw, technobabbl.es
"""
from __future__ import annotations


class ArgumentError(Exception):
    """Exception to raise if the caller passes invalid arguments."""
    ...


class CooldownError(Exception):
    """Exception to raise if the caller is in cooldown."""
    def __init__(self, remaining_time: float):
        super().__init__()
        self.remaining_time = remaining_time


class NonexistentNickError(Exception):
    """Exception to raise if someone tries to luv/h8 a nonexistent nick."""
    ...

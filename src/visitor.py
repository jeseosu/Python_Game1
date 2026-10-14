from abc import ABC, abstractmethod


class Visitor(ABC):
    def __init__(self, name, race, gold_pouch):
        self._name = name
        self._race = race
        self._gold_pouch = gold_pouch
        self._is_served = False

    @property
    def name(self):
        return self._name

    @property
    def race(self):
        return self._race

    @property
    def gold_pouch(self):
        return self._gold_pouch

    def pay(self, amount):
        if self._gold_pouch >= amount:
            self._gold_pouch -= amount
            return amount
        return 0

    @abstractmethod
    def interact(self):
        pass

    def __str__(self):
        return f"{self._name} ({self._race}) - {self._gold_pouch} золота"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}', '{self._race}', {self._gold_pouch})"
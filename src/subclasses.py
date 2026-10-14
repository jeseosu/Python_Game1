from src.visitor import Visitor
import random

class Customer(Visitor):
    def __init__(self, name, race, gold_pouch, favorite_drink):
        super().__init__(name, race, gold_pouch)
        self._favorite_drink = favorite_drink

    def interact(self):
        return f"{self.name} спокійно сидить і чекає на свій {self._favorite_drink}."

class Adventurer(Visitor):
    def __init__(self, name, race, gold_pouch, level):
        super().__init__(name, race, gold_pouch)
        self._level = level

    def interact(self):
        return f"{self.name} голосно розповідає про вбитого дракона! Рівень: {self._level}."

class Troublemaker(Visitor):
    def __init__(self, name, race, gold_pouch, threat_level):
        super().__init__(name, race, gold_pouch)
        self._threat_level = threat_level
        self._is_causing_trouble = True

    @property
    def is_causing_trouble(self):
        return self._is_causing_trouble

    def calm_down(self):
        self._is_causing_trouble = False

    def interact(self):
        if self._is_causing_trouble:
            return f"{self.name} ПРОВОКУЄ БІЙКУ! Рівень загрози: {self._threat_level}!"
        return f"{self.name} сердито сопе, але поводиться тихо."
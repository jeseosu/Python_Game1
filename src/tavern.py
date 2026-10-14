from src.visitor import Visitor
from src.subclasses import Troublemaker


class Tavern:
    def __init__(self, name):
        self._name = name
        self._visitors = []
        self._gold = 50
        self._reputation = 20

    @property
    def gold(self):
        return self._gold

    @property
    def reputation(self):
        return self._reputation

    @property
    def visitors(self):
        return self._visitors

    def add_visitor(self, visitor):
        if isinstance(visitor, Visitor):
            self._visitors.append(visitor)
            self._reputation += 1
        else:
            raise TypeError("Можна додавати лише об'єкти типу Visitor")

    def remove_visitor(self, visitor):
        if visitor in self._visitors:
            self._visitors.remove(visitor)

    def serve_visitor(self, visitor_name):
        visitor = self.search_by_name(visitor_name)
        if visitor:
            earned = visitor.pay(10)
            if earned > 0:
                self._gold += earned
                self._reputation += 2
                self.remove_visitor(visitor)
                return f"Ви обслужили {visitor.name} і заробили {earned} золота!"
            else:
                self.remove_visitor(visitor)
                return f"У {visitor.name} недостатньо золота! Ви вигнали його."
        return "Відвідувача з таким іменем не знайдено."

    def resolve_conflict(self):
        troublemakers = self.filter_by_type(Troublemaker)
        active_troublemakers = [t for t in troublemakers if t.is_causing_trouble]

        if active_troublemakers:
            t = active_troublemakers[0]
            self.remove_visitor(t)
            self._reputation += 5
            return f"Ви епічно викинули {t.name} у вікно! Репутація зросла."
        return "У таверні зараз спокійно, конфліктів немає."

    def search_by_name(self, name):
        for v in self._visitors:
            if v.name.lower() == name.lower():
                return v
        return None

    def filter_by_type(self, visitor_type):
        return [v for v in self._visitors if isinstance(v, visitor_type)]

    def sort_visitors_by_gold(self):
        self._visitors.sort(key=lambda v: v.gold_pouch, reverse=True)

    def __str__(self):
        return f"Таверна '{self._name}' | Золото: {self._gold} | Репутація: {self._reputation} | Гостей: {len(self._visitors)}"
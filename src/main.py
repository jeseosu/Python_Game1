import random
from src.tavern import Tavern
from src.subclasses import Customer, Adventurer, Troublemaker


def generate_random_visitor():
    names = ["Гімлі", "Леголас", "Гендальф", "Боба", "Торін", "Арагорн", "Орк-Валера"]
    races = ["Гном", "Ельф", "Людина", "Орк", "Гоблін"]
    drinks = ["Ель", "Медовуха", "Вино", "Вода"]

    v_type = random.choice(["Customer", "Adventurer", "Troublemaker"])
    name = random.choice(names) + f"-{random.randint(1, 99)}"
    race = random.choice(races)
    gold = random.randint(5, 50)

    if v_type == "Customer":
        return Customer(name, race, gold, random.choice(drinks))
    elif v_type == "Adventurer":
        return Adventurer(name, race, gold, random.randint(1, 100))
    else:
        return Troublemaker(name, race, gold, random.randint(1, 10))


def main():
    print("=" * 50)
    print("ЛАСКАВО ПРОСИМО ДО СИМУЛЯТОРА ФЕНТЕЗІ-ТАВЕРНИ!")
    print("=" * 50)

    tavern_name = input("Як назвемо вашу таверну? ")
    my_tavern = Tavern(tavern_name)

    while True:
        print("\n" + "=" * 40)
        print(my_tavern)
        print("=" * 40)
        print("1. Відкрити двері (чекати на нових гостей)")
        print("2. Оглянути зал (переглянути всіх відвідувачів)")
        print("3. Обслужити відвідувача")
        print("4. Вирішити конфлікт (якщо є бешкетники)")
        print("5. Відсортувати гостей за багатством (вивести найбагатших)")
        print("0. Закрити таверну (Вийти)")

        choice = input("\nОберіть дію: ")

        if choice == '1':
            new_guests_count = random.randint(1, 3)
            for _ in range(new_guests_count):
                visitor = generate_random_visitor()
                my_tavern.add_visitor(visitor)
                print(f"🚪 До таверни зайшов: {visitor.name} ({type(visitor).__name__})")
                print(f"   💬 {visitor.interact()}")

        elif choice == '2':
            if not my_tavern.visitors:
                print("У таверні порожньо. Тільки мухи літають.")
            else:
                print("\n--- Гості в залі ---")
                for v in my_tavern.visitors:
                    print(v)

        elif choice == '3':
            if not my_tavern.visitors:
                print("Немає кого обслуговувати!")
                continue

            print("Кого ви хочете обслужити?")
            for v in my_tavern.visitors:
                print(f"- {v.name}")
            name_to_serve = input("Введіть ім'я: ")
            result = my_tavern.serve_visitor(name_to_serve)
            print(f"🍺 {result}")

        elif choice == '4':
            result = my_tavern.resolve_conflict()
            print(f"⚔️ {result}")

        elif choice == '5':
            my_tavern.sort_visitors_by_gold()
            print("Гостей відсортовано за кількістю золота в гаманці!")
            for v in my_tavern.visitors:
                print(f"{v.name}: {v.gold_pouch} монет")

        elif choice == '0':
            print(f"Ви закриваєте таверну '{tavern_name}'. Зароблено золота: {my_tavern.gold}. До зустрічі!")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":

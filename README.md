# MemeMatch: тест «Який ти мем?» (Flask)

Інтерактивний тест (варіант 13). 8 питань, 8 мемів 2025 року (6 7, Tung Tung Sahur,
Tralalero Tralala, Ballerina Cappuccina, Chill Guy, Skibidi Toilet, Gigachad, Пес Патрон).
Результат рахується **на сервері** (косинусна схожість профілю користувача з профілем мему),
статистика зберігається в SQLite, результатом можна поділитися за посиланням.

## Запуск
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
pytest                   # тести бекенду
```

## Структура
```
app.py          Flask-застосунок, маршрути та API        (бекенд)
scoring.py      валідація відповідей, підбір мему        (бекенд)
data.py         питання, ваги, профілі мемів             (бекенд)
tests/          pytest-тести                              (бекенд)
templates/      index.html                                (фронтенд)
static/         style.css, script.js                      (фронтенд)
instance/       stats.db (створюється автоматично)
```

## API (контракт між бекендом і фронтендом)
| Метод | URL | Опис |
|---|---|---|
| GET | `/api/questions` | питання та варіанти (без ваг) + назви рис |
| POST | `/api/submit` | тіло `{"answers":[{"q":1,"o":0},...]}` → `result`, `ranking`, `traits`, `rarity` |
| GET | `/api/meme/<id>` | мем і його рідкість (для сторінки з посиланням) |
| GET | `/api/stats` | загальна статистика по мемах |
| GET | `/result/<id>` | сторінка результату, якою можна ділитися |

Помилки валідації: HTTP 400 і `{"error": "..."}`.

## Розподіл ролей
- Бекенд: `app.py`, `scoring.py`, `data.py`, `tests/`, API
- Фронтенд: `templates/`, `static/`

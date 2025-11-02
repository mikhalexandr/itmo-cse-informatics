# Author = Mikhalchenkov Alexandr Nikolaevich
# Group = P3109
# Date = 02.11.2025
# Variant = 501651 % 3 = 0
import re

CRON_FIELD = r"(?:\*|\*\/\d+|\d{1,2}(?:-\d{1,2})?(?:/\d+)?(?:,\d{1,2}(?:-\d{1,2})?(?:/\d+)?)*)"
CRON_REGEX = re.compile(
    r"^" + r"\s+".join([CRON_FIELD]*5) + r"$"
)


def is_valid_cron(expression):
    return bool(CRON_REGEX.match(expression.strip()))


tests = [
    ("30 14 * * *", True),              # в 14:30 каждый день
    ("*/5 * * * *", True),              # каждые 5 минут
    ("0 0 1 1 *", True),                # в полночь 1 января
    ("1-10/2 0 1,15 * 1-5", True),      # сложное выражение
    ("12 8 * *", False),                # только 4 поля
    ("* * * * * *", False),             # 6 полей
    ("0 0 1-32 1 *", True),             # формат разрешён, диапазон не проверяется
    ("5,10,15 0-23 * 1-12 0-6", True),  # несколько значений и диапазоны
    ("* * * * ", False),                # пробел в конце, 4 поля
]

all_passed = True
tmp = 0
for expression, expected in tests:
    tmp += 1
    result = is_valid_cron(expression)
    print(f"Тест {tmp}: {expression:25} -> {result}, ожидается: {expected},"
          f" {"Совпадает" if result == expected else "Не совпадает"}")
    if result != expected:
        all_passed = False

if all_passed:
    print("Все тесты пройдены успешно!")
else:
    print("Что-то пошло не так!")

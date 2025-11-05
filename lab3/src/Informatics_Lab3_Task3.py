# Author = Mikhalchenkov Alexandr Nikolaevich
# Group = P3109
# Date = 06.11.2025
# Variant = 501651 % 3 = 0
import re

r_min = r"(?:[0-9]|[1-5][0-9])"         # 0-59
r_hr = r"(?:[0-9]|1[0-9]|2[0-3])"       # 0-23
r_dom = r"(?:[1-9]|[12][0-9]|3[01])"    # 1-31
r_mon = r"(?:[1-9]|1[0-2])"             # 1-12
r_dow = r"[0-6]"                        # 0-6


def build_field_regex(base):
    variant_1 = rf"{base}(?:-{base})?(?:/\d+)?"
    # Число, диапазон, шаг:
    # {base} - число, разрешённое для данного поля (например, 7)
    # (?:-{base})? - необязательный диапазон (например, 7-13)
    # (?:/\d+)? - необязательный шаг (например, 7-13/2 или 7/4)
    # Варианты: 5, 7-10, 7/4, 7-10/2
    variant_2 = r"(?:\*\/\d+)"
    # Звёздочка со шагом:
    # \* - звёздочка (любой допускается)
    # \/ - экранированный слэш
    # \d+ - шаг
    # Варианты: */5, */10 - "каждые 5 минут", "каждые 10 дней"
    variant_3 = r"(?:\*)"
    # Просто звёздочка:
    # * - "любое значение" в поле cron
    item = rf"(?:{variant_1}|{variant_2}|{variant_3})"
    field = rf"{item}(?:,{item})*"
    return field


minute_regex = build_field_regex(r_min)
hour_regex = build_field_regex(r_hr)
day_regex = build_field_regex(r_dom)
month_regex = build_field_regex(r_mon)
weekday_regex = build_field_regex(r_dow)

cron_regex = re.compile(
    rf"^{minute_regex}\s+{hour_regex}\s+{day_regex}\s+{month_regex}\s+{weekday_regex}$"
)


def is_valid_cron(expr):
    return bool(cron_regex.fullmatch(expr.strip()))


tests = [
    ("30 14 * * *", True),              # в 14:30 каждый день
    ("*/5 * * * *", True),              # каждые 5 минут
    ("0 0 1 1 *", True),                # в полночь 1 января
    ("1-10/2 0 1,15 * 1-5", True),      # сложное выражение
    ("12 8 * *", False),                # только 4 поля
    ("* * * * * *", False),             # 6 полей
    ("0 0 1-32 1 *", False),            # 32 - вне диапазона дней месяца
    ("5,10,15 0-23 * 1-12 0-6", True),  # несколько значений и диапазоны
    ("* * * * ", False),                # пробел в конце, 4 поля
    ("60 12 * * *", False),             # 60 минут - ошибка
    ("0 24 1 1 1", False),              # 24 часа - ошибка
    ("0 0 0 1 1", False),               # 0 день месяца - ошибка
    ("0 0 1 13 1", False),              # 13 месяц - ошибка
    ("0 0 1 1 7", False),               # 7 день недели - ошибка
    ("0-59 12 * * *", True),            # диапазон минута от 0 до 59 - ок
    ("0-60 12 * * *", False),           # диапазон минута от 0 до 60 - ошибка
]

all_passed = True
for index, (expression, expected) in enumerate(tests, 1):
    result = is_valid_cron(expression)
    print(f"Тест {index}: {expression:25} -> {result}, ожидается: {expected},"
          f" {'Совпадает' if result == expected else 'Не совпадает'}")
    if result != expected:
        all_passed = False

if all_passed:
    print("Все тесты пройдены успешно!")
else:
    print("Что-то пошло не так!")

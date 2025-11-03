# Author = Mikhalchenkov Alexandr Nikolaevich
# Group = P3109
# Date = 03.11.2025
# Variant = 501651 % 5 = 1
import re


def words_with_one_vowel(text):
    vowels = f"{"аеёиоуыэюя"}{"аеёиоуыэюя".capitalize()}-"
    words = re.findall(r"\b[А-ЯЁа-яё][а-яё-]*\b", text)
    res = []
    for word in words:
        vowels_in_word = re.findall(rf"[{vowels}]", word)
        if vowels_in_word:
            if len(set(v.lower() for v in vowels_in_word if v != "-")) == 1:
                res.append(word)
    res.sort(key=lambda w: (len(w), w.lower()))
    return res


tests = [
    {
        'input': "\t  А у кого другой преподаватель ведёт? Ну, вот он очень старается, чтобы вам было неприятно, "
                 "но неприятно в хорошем смысле слова, поэтому он придумывает интересные задания\n"
                 "\t  © Балакшин П.В.",
        'expected': ["А", "у", "но", "Ну", "он", "он", "вам", "вот", "кого"]
    },
    {
        'input': "\t  С: А можно аннотацию на камне принести?\n"
                 "\t  П: На надгробном?..\n"
                 "\t  © Балакшин П.В.",
        'expected': ["А", "на", "На", "можно"]
    },
    {
        'input': "\t  П: Что-то вас сегодня мало... Значит придётся применять репрессивные меры.\n"
                 "\t  С: Какие например?\n"
                 "\t  П: Пороть.\n"
                 "\t  С: Тех, кто пришёл?\n"
                 "\t  П: Ну, а вдруг вам понравится...\n"
                 "\t  © Балакшин П.В.",
        'expected': ["а", "Ну", "вам", "вас", "кто", "Тех", "вдруг", "Пороть", "Что-то"]
    },
    {
        'input': "\t  В основном я шучу про ПСЖ, но не только\n"
                 "\t  © Балакшин П.В.",
        'expected': ["я", "не", "но", "про", "шучу", "только", "основном"]
    },
    {
        'input': "\t  Что-то вас много, надо кого-нибудь отчислить...\n"
                 "\t  © Балакшин П.В.",
        'expected': ["вас", "много", "Что-то"]
    },
]

all_passed = True
for index, test in enumerate(tests, 1):
    result = words_with_one_vowel(test["input"])
    print(f"Тест {index}:")
    print(f"\tВход:\n{test["input"]}")
    print(f"\tОжидается: {", ".join(test["expected"])}")
    print(f"\tНайдено: {", ".join(result)}")
    if result != test["expected"]:
        print("Не cовпадает\n")
        all_passed = False
    else:
        print("Cовпадает\n")

if all_passed:
    print("Все тесты пройдены успешно!")
else:
    print("Что-то пошло не так!")

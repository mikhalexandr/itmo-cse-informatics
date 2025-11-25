import time
from pathlib import Path

from lab4.src.mandatory_task.convert import (
    hcl_to_dict as custom_hcl_to_dict,
    dict_to_bin as custom_dict_to_bin
)
from lab4.src.optional_task_1.convert import (
    bin_to_dict as custom_bin_to_dict,
    dict_to_toml as custom_dict_to_toml
)
from lab4.src.optional_task_2.convert import (
    hcl_to_dict as library_hcl_to_dict,
    dict_to_bin as library_dict_to_bin,
    bin_to_dict as library_bin_to_dict,
    dict_to_toml as library_dict_to_toml
)
from lab4.src.optional_task_3.convert import (
    dict_to_xml as custom_dict_to_xml
)


def print_results(title, total_time, _iterations):
    avg_time_sec = total_time / _iterations
    avg_time_ms = avg_time_sec * 1000
    ops_per_sec = 1 / avg_time_sec if avg_time_sec > 0 else 0

    print("=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)
    print(f"  ► Общее время:          {total_time:.4f} сек")
    print(f"  ► Среднее на операцию:  {avg_time_ms:.4f} мс")
    print(f"  ► Производительность:   {ops_per_sec:,.0f} оп/сек")
    print("-" * 60 + "\n")


def benchmark_custom_hcl_to_toml_via_bin(_hcl_data, _iterations=100):
    title = "[Custom] HCL -> Binary -> TOML"

    start_time = time.time()

    for _ in range(_iterations):
        binary_data = custom_dict_to_bin(custom_hcl_to_dict(_hcl_data))
        toml_data = custom_dict_to_toml(custom_bin_to_dict(binary_data))

    total_time = time.time() - start_time
    print_results(title, total_time, _iterations)


def benchmark_library_hcl_to_toml_via_bin(_hcl_data, _iterations=100):
    title = "[Library] HCL -> Binary -> TOML"

    start_time = time.time()

    for _ in range(_iterations):
        binary_data = library_dict_to_bin(library_hcl_to_dict(_hcl_data))
        toml_data = library_dict_to_toml(library_bin_to_dict(binary_data))

    total_time = time.time() - start_time
    print_results(title, total_time, _iterations)


def benchmark_custom_hcl_to_xml_via_bin(_hcl_data, _iterations=100):
    title = "[Custom] HCL -> Binary -> XML"

    start_time = time.time()

    for _ in range(_iterations):
        binary_data = custom_dict_to_bin(custom_hcl_to_dict(_hcl_data))
        xml_data = custom_dict_to_xml(custom_bin_to_dict(binary_data))

    total_time = time.time() - start_time
    print_results(title, total_time, _iterations)


if __name__ == "__main__":
    SRC = Path(__file__).parent.parent

    with open(SRC / "optional_task_4/data/schedule.hcl", "r", encoding="utf-8") as f:
        hcl_data = f.read()

    iterations = int(input("Введите количество итераций: "))

    print(f"\nЗАПУСК БЕНЧМАРКОВ ({iterations} итераций)...\n")

    benchmark_custom_hcl_to_toml_via_bin(hcl_data, iterations)
    benchmark_library_hcl_to_toml_via_bin(hcl_data, iterations)
    benchmark_custom_hcl_to_xml_via_bin(hcl_data, iterations)

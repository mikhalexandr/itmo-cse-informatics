from pathlib import Path

from lab4.src.formats import BinSerializer, TomlSerializer


def bin_to_dict(_binary_data):
    bin_serializer = BinSerializer()
    _dict = bin_serializer.deserialize(_binary_data)
    return _dict


def dict_to_toml(_dict):
    toml_serializer = TomlSerializer()
    _toml_data = toml_serializer.serialize(_dict)
    return _toml_data


if __name__ == "__main__":
    SRC = Path(__file__).parent.parent

    with open(SRC / "optional_task_1/data/schedule.bin", "rb") as f:
        binary_data = f.read()

    toml_data = dict_to_toml(bin_to_dict(binary_data))

    with open(SRC / "optional_task_1/data/schedule.toml", "w") as f:
        f.write(toml_data)

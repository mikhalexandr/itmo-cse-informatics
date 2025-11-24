import pickle
from pathlib import Path

import hcl2
import toml


def hcl_to_dict(_hcl_data):
    _dict = hcl2.loads(_hcl_data)
    return _dict


def dict_to_bin(_dict):
    _binary_data = pickle.dumps(_dict)
    return _binary_data


def bin_to_dict(_binary_data):
    _dict = pickle.loads(_binary_data)
    return _dict


def dict_to_toml(_dict):
    _toml_data = toml.dumps(_dict)
    return _toml_data


if __name__ == "__main__":
    SRC = Path(__file__).parent.parent

    with open(SRC / "optional_task_2/data/schedule.hcl", "r") as f:
        hcl_data = f.read()

    binary_data = dict_to_bin(hcl_to_dict(hcl_data))

    with open(SRC / "optional_task_2/data/schedule.bin", "wb") as f:
        f.write(binary_data)


    with open(SRC / "optional_task_2/data/schedule.bin", "rb") as f:
        binary_data = f.read()

    toml_data = dict_to_toml(bin_to_dict(binary_data))

    with open(SRC / "optional_task_2/data/schedule.toml", "w") as f:
        f.write(toml_data)

from pathlib import Path

from lab4.src.formats import BinCodec, HCLParser


def hcl_to_dict(_hcl_data):
    hcl_parser = HCLParser(_hcl_data)
    _dict = hcl_parser.parse()
    return _dict


def dict_to_bin(_dict):
    bin_codec = BinCodec()
    _binary_data = bin_codec.serialize(_dict)
    return _binary_data


if __name__ == "__main__":
    SRC = Path(__file__).parent.parent

    with open(SRC / "mandatory_task/data/schedule.hcl", encoding="utf-8") as f:
        hcl_data = f.read()

    binary_data = dict_to_bin(hcl_to_dict(hcl_data))

    with (
        open(SRC / "mandatory_task/data/schedule.bin", "wb") as f1,
        open(SRC / "optional_task_1/data/schedule.bin", "wb") as f2,
        open(SRC / "optional_task_3/data/schedule.bin", "wb") as f3
    ):
        f1.write(binary_data)
        f2.write(binary_data)
        f3.write(binary_data)

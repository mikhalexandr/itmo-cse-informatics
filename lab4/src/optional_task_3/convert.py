from pathlib import Path

from lab4.src.formats import BinCodec, XMLSerializer


def bin_to_dict(_binary_data):
    bin_serializer = BinCodec()
    _dict = bin_serializer.deserialize(_binary_data)
    return _dict


def dict_to_xml(_dict):
    toml_serializer = XMLSerializer()
    _xml_data = toml_serializer.serialize(_dict)
    return _xml_data


if __name__ == "__main__":
    SRC = Path(__file__).parent.parent

    with open(SRC / "optional_task_3/data/schedule.bin", "rb") as f:
        binary_data = f.read()

    xml_data = dict_to_xml(bin_to_dict(binary_data))

    with open(SRC / "optional_task_3/data/schedule.xml", "w") as f:
        f.write(xml_data)

import datetime


class XMLSerializer:
    def __init__(self):
        self._lines = []

    @staticmethod
    def _escape(s):
        s = str(s)
        return (s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    def _walk(self, value, tag_name, level):
        indent = "    " * level
        if isinstance(value, (list, tuple)):
            for item in value:
                self._walk(item, tag_name, level)
            return
        if isinstance(value, dict):
            self._lines.append(f"{indent}<{tag_name}>")
            for k, v in value.items():
                self._walk(v, k, level + 1)
            self._lines.append(f"{indent}</{tag_name}>")
            return
        if value is None:
            self._lines.append(f"{indent}<{tag_name} />")
        elif isinstance(value, (datetime.datetime, datetime.date)):
            str_val = value.isoformat()
            self._lines.append(f"{indent}<{tag_name}>{str_val}</{tag_name}>")
        else:
            str_val = self._escape(value)
            self._lines.append(f"{indent}<{tag_name}>{str_val}</{tag_name}>")

    def serialize(self, data, root_tag="schedule"):
        self._lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        if isinstance(data, dict):
            self._lines.append(f"<{root_tag}>")
            for key, value in data.items():
                self._walk(value, key, level=1)
            self._lines.append(f"</{root_tag}>")
        else:
            self._walk(data, root_tag, level=0)
        return "\n".join(self._lines)

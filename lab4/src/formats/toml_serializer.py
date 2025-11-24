import datetime


class TomlSerializer:
    @staticmethod
    def _escape_string(s):
        chars = {
            '\\': '\\\\',
            '"': '\\"',
            '\b': '\\b',
            '\f': '\\f',
            '\n': '\\n',
            '\r': '\\r',
            '\t': '\\t'
        }
        return ''.join(chars.get(c, c) for c in s)

    def _format_value(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{self._escape_string(value)}"'
        elif isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        elif isinstance(value, (list, tuple)):
            if not value:
                return "[]"
            items = [self._format_value(item) for item in value]
            return f"[{', '.join(items)},]"
        elif value is None:
            return ""
        else:
            return f'"{self._escape_string(str(value))}"'

    def _walk(self, data, prefix=""):
        if not isinstance(data, dict):
            return ""
        lines = []
        primitives = {}
        tables = {}
        arrays_of_tables = {}
        for k, v in data.items():
            if isinstance(v, dict):
                tables[k] = v
            elif isinstance(v, (list, tuple)) and len(v) > 0 and isinstance(v[0], dict):
                arrays_of_tables[k] = v
            else:
                primitives[k] = v
        for k, v in primitives.items():
            if v is not None:
                lines.append(f'{k} = {self._format_value(v)}')
        for k, v_list in arrays_of_tables.items():
            full_key = f"{prefix}.{k}" if prefix else k
            for item in v_list:
                if lines:
                    lines.append("")
                lines.append(f"[[{full_key}]]")
                content = self._walk(item, full_key)
                if content:
                    lines.append(content)
        for k, v in tables.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if lines:
                lines.append("")
            lines.append(f"[{full_key}]")
            content = self._walk(v, full_key)
            if content:
                lines.append(content)
        return "\n".join(lines)

    def serialize(self, data):
        if not isinstance(data, dict):
            if isinstance(data, (list, tuple)):
                return ""
            return str(data)
        result = self._walk(data, "").strip()
        return result + "\n\n"

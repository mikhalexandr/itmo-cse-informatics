import datetime


class HCLSyntaxError(Exception):
    pass


class HCLParser:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def _convert_value(value):
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            content = value[1:-1]
            if '-' in content and len(content) >= 10:
                try:
                    return datetime.datetime.fromisoformat(content)
                except ValueError:
                    try:
                        return datetime.date.fromisoformat(content)
                    except ValueError:
                        pass
            return content
        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
            return int(value)
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        return value

    def _raise_error(self, message, index=None):
        if index is None:
            index = len(self.text)
        line_num = self.text.count('\n', 0, index) + 1
        last_newline = self.text.rfind('\n', 0, index)
        col_num = index - last_newline
        raise HCLSyntaxError(f"Line {line_num}, Col {col_num}: {message}")

    def _tokenize(self):
        tokens = []
        i = 0
        n = len(self.text)
        special_chars = {'{', '}', '=', ','}
        while i < n:
            char = self.text[i]
            if char.isspace():
                i += 1
                continue
            if char in special_chars:
                tokens.append(char)
                i += 1
                continue
            if char == '"':
                start_idx = i
                j = i + 1
                found_end = False
                while j < n:
                    if self.text[j] == '"' and self.text[j - 1] != '\\':
                        found_end = True
                        break
                    j += 1
                if not found_end:
                    self._raise_error("Unterminated string literal", start_idx)
                token_val = self.text[i:j + 1]
                tokens.append(token_val)
                i = j + 1
                continue
            if char == '[':
                start_idx = i
                j = i + 1
                balance = 1
                while j < n and balance > 0:
                    if self.text[j] == '[':
                        balance += 1
                    elif self.text[j] == ']':
                        balance -= 1
                    j += 1
                if balance > 0:
                    self._raise_error("Unbalanced bracket '['", start_idx)
                token_val = self.text[i:j]
                tokens.append(token_val)
                i = j
                continue
            if char == '#' or (char == '/' and i + 1 < n and self.text[i + 1] == '/'):
                while i < n and self.text[i] != '\n':
                    i += 1
                continue
            j = i
            while j < n:
                curr = self.text[j]
                if curr.isspace() or curr in special_chars or curr == '"' or curr == '[':
                    break
                j += 1
            token_val = self.text[i:j]
            if token_val:
                tokens.append(token_val)
            i = j
        return tokens

    def _parse_list_content(self, list_str):
        content = list_str[1:-1].strip()
        if not content:
            return []
        sub_parser = HCLParser(content)
        tokens = sub_parser._tokenize()
        items = []
        for t in tokens:
            if t != ',':
                items.append(self._convert_value(t))
        return items

    def parse(self):
        try:
            tokens = self._tokenize()
        except HCLSyntaxError:
            raise
        root = {}
        stack = [(root, None, None)]
        i = 0
        n = len(tokens)
        while i < n:
            current_token = tokens[i]
            if current_token == '}':
                if len(stack) <= 1:
                    raise HCLSyntaxError(f"Unexpected closing brace '}}' at token position {i}")
                completed_obj, block_name, block_key = stack.pop()
                parent_obj = stack[-1][0]
                final_val = completed_obj
                if block_key:
                    final_val = {block_key: completed_obj}
                if block_name in parent_obj:
                    if isinstance(parent_obj[block_name], list):
                        parent_obj[block_name].append(final_val)
                    else:
                        parent_obj[block_name] = [parent_obj[block_name], final_val]
                else:
                    parent_obj[block_name] = final_val
                i += 1
                continue
            if i + 1 < n and tokens[i + 1] == '=':
                if i + 2 >= n:
                    raise HCLSyntaxError(f"Unexpected end of input after '=' for key '{current_token}'")
                key = current_token
                value_token = tokens[i + 2]
                if value_token.startswith('['):
                    try:
                        converted_val = self._parse_list_content(value_token)
                    except Exception as e:
                        raise HCLSyntaxError(f"Error parsing list for key '{key}': {str(e)}")
                else:
                    converted_val = self._convert_value(value_token)
                current_dict = stack[-1][0]
                if key in current_dict:
                    if isinstance(current_dict[key], list):
                        current_dict[key].append(converted_val)
                    else:
                        current_dict[key] = [current_dict[key], converted_val]
                else:
                    current_dict[key] = converted_val
                i += 3
                continue
            if i + 1 < n:
                if tokens[i + 1] == '{':
                    block_name = current_token
                    block_key = None
                    stack.append(({}, block_name, block_key))
                    i += 2
                    continue
                elif i + 2 < n and tokens[i + 2] == '{':
                    block_name = current_token
                    block_key = tokens[i + 1].strip('"')
                    stack.append(({}, block_name, block_key))
                    i += 3
                    continue
            raise HCLSyntaxError(f"Unexpected token '{current_token}'")
        if len(stack) > 1:
            unclosed_block = stack[-1][1]
            raise HCLSyntaxError(f"Unexpected end of file. Unclosed block '{unclosed_block}'")
        return root

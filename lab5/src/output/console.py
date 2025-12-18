import pandas as pd

BORDER_CHARS = {
    'thick_h': '═',
    'thin_h': '─',
    'thick_v': '║',
    'thin_v': '│',
    'corner_tl': '╔',
    'corner_tr': '╗',
    'corner_bl': '╚',
    'corner_br': '╝',
    'cross_top': '╦',
    'cross_bottom': '╩',
    'cross_left': '╠',
    'cross_right': '╣',
    'cross': '╬',
}


def get_column_widths(cols):
    col_widths = []
    for c in range(cols):
        if c == 1:
            col_widths.append(15)
        elif c == 2:
            col_widths.append(10)
        elif c == 3:
            col_widths.append(3)
        elif c < 5:
            col_widths.append(7)
        else:
            col_widths.append(3)
    return col_widths


def get_vertical_border_char(row_idx, col_idx, is_horizontal_border=False, border_type='thin'):
    in_table = row_idx >= 3
    is_thick_border = border_type == 'thick'

    if col_idx == 3 or col_idx > 4:
        if is_horizontal_border:
            return BORDER_CHARS['thick_h'] if is_thick_border else BORDER_CHARS['thin_h']
        else:
            return ' '

    if is_horizontal_border:
        return BORDER_CHARS['cross']
    if in_table:
        return BORDER_CHARS['thick_v']
    return BORDER_CHARS['thin_v']


def format_value(value, col_idx, width):
    if value == '' or pd.isna(value):
        value_str = ''
    else:
        try:
            num_value = float(value)
            value_str = str(int(num_value)) if num_value.is_integer() else str(value)
        except (ValueError, TypeError):
            value_str = str(value)
    return value_str.rjust(width) if col_idx < 5 else value_str.center(width)


def build_horizontal_border(row_idx, col_widths, border_type='thin'):
    cols = len(col_widths)
    left_char = BORDER_CHARS['cross_left']
    border_char = BORDER_CHARS['thick_h'] if border_type == 'thick' else BORDER_CHARS['thin_h']
    right_char = BORDER_CHARS['cross_right']

    line = left_char
    for col_idx in range(cols):
        line += border_char * col_widths[col_idx]
        if col_idx < cols - 1:
            line += get_vertical_border_char(row_idx, col_idx, is_horizontal_border=True, border_type=border_type)
        else:
            line += right_char
    return line


def build_top_border(cols, col_widths):
    top_border = BORDER_CHARS['corner_tl']
    for c in range(cols):
        top_border += BORDER_CHARS['thick_h'] * col_widths[c]
        if c < cols - 1:
            if c == 3 or c > 4:
                top_border += BORDER_CHARS['thick_h']
            else:
                top_border += BORDER_CHARS['cross_top']
        else:
            top_border += BORDER_CHARS['corner_tr']
    return top_border


def build_bottom_border(cols, col_widths):
    bottom_border = BORDER_CHARS['corner_bl']
    for c in range(cols):
        bottom_border += BORDER_CHARS['thick_h'] * col_widths[c]
        if c < cols - 1:
            if c == 3 or c > 4:
                bottom_border += BORDER_CHARS['thick_h']
            else:
                bottom_border += BORDER_CHARS['cross_bottom']
        else:
            bottom_border += BORDER_CHARS['corner_br']
    return bottom_border


def print_formatted_table(df):
    df_formatted = df.fillna('')
    rows, cols = df_formatted.shape
    col_widths = get_column_widths(cols)

    # Верхняя граница
    print(build_top_border(cols, col_widths))

    # Основные строки
    for r in range(rows):
        line = BORDER_CHARS['thick_v']
        for c in range(cols):
            value = df_formatted.iloc[r, c]
            line += format_value(value, c, col_widths[c])
            if c < cols - 1:
                line += get_vertical_border_char(r, c)
            else:
                line += BORDER_CHARS['thick_v']
        print(line)

        # Горизонтальные разделители
        if r < rows - 1:
            if r == 2:
                print(build_horizontal_border(r, col_widths, border_type='thick'))
            else:
                print(build_horizontal_border(r, col_widths, border_type='thin'))

    # Нижняя граница
    print(build_bottom_border(cols, col_widths))

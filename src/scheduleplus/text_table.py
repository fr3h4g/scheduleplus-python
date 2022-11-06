EXTRA_SPACE = 3


def table_line(width):
    return "".zfill(width - 1).replace("0", "-") + " "


def table(column_names, table_data):
    col_sizes = {}
    for index, col in enumerate(column_names):
        if index not in col_sizes:
            col_sizes[index] = len(col) + EXTRA_SPACE

    for row in table_data:
        for index, col in enumerate(row):
            if index not in col_sizes:
                col_sizes[index] = len(col) + EXTRA_SPACE
            if len(col) + EXTRA_SPACE > col_sizes[index]:
                col_sizes[index] = len(col) + EXTRA_SPACE

    header = ""
    for index, col in enumerate(column_names):
        header += f"{col:{col_sizes[index]}}"
    header += "\n"
    for col_size in col_sizes:
        header += table_line(col_sizes[col_size])
    header += "\n"

    data = ""
    for row in table_data:
        for index, col in enumerate(row):
            data += f"{col:{col_sizes[index]}}"
        data += "\n"

    return header + data

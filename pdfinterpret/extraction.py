from pdfminer.layout import LTTextBoxHorizontal


def split_texts(lines):
    return list(map(lambda x: list(filter(lambda t: t != "", x.get_text().split('\n'))), lines))


def extract_tuples(line):
    lines = sorted(line, key=lambda x: x.x0)
    tuples = [x if len(x) > 1 else x[0] for x in list(zip(*split_texts(lines)))]
    return tuples


def extract_lines_of_column(column):
    lines = sorted(column, key=lambda l: l.y0, reverse=True)
    arrays = [x if len(x) > 1 else x[0] for x in split_texts(lines)]
    return arrays if len(arrays) > 1 else arrays[0]


def get_line_boxes(page, rounding=3):
    lines = []
    boxes = [t for t in page if isinstance(t, LTTextBoxHorizontal)]
    boxes = sorted(boxes, key=lambda x: x.y0, reverse=True)
    prev_line = None
    current_line = []
    for b in boxes:
        if round(b.y0, rounding) != prev_line:
            if len(current_line):
                tuples = extract_tuples(current_line)
                lines.append(tuples)
                current_line = []

        current_line.append(b)
        prev_line = round(b.y0, rounding)

    tuples = extract_tuples(current_line)
    lines.append(tuples)
    return lines


def get_column_boxes(page, rounding=3):
    columns = []
    boxes = [t for t in page if isinstance(t, LTTextBoxHorizontal)]
    boxes = sorted(boxes, key=lambda x: (x.x0, x.x1))
    prev_column_x0 = None
    prev_column_x1 = None
    current_column = []
    for b in boxes:
        if round(b.x0, rounding) != prev_column_x0:
            if round(b.x1, rounding) != prev_column_x1:
                if len(current_column):
                    columns.append(extract_lines_of_column(current_column))
                    current_column = []

        current_column.append(b)
        prev_column_x0 = round(b.x0, rounding)
        prev_column_x1 = round(b.x1, rounding)

    columns.append(extract_lines_of_column(current_column))
    return columns

import pymupdf
import pandas as pd

from typing import Callable, Iterable


from pathlib import Path

name_headers = ["Full Name", "Name", "Student"]
terminal_headers = ["Total", "Max"]
terminal_row_headers = ["Total", "Max"]


SKIP = ["This Week's Assignments"]


def _partition_while(
    predicate: Callable[[any], bool], iterable: Iterable[any], behavior: str = "left"
) -> tuple[list[any], list[any]]:
    """Partitions into two lists while predicate is true.

    Args:
        predicate: A Callable that returns something evaluating to True or not.
        iterable: The thing to iterate over.
        behavior
            left: On failure to match, include with the left group (trues)
            right: On failure to match, include with the right group (falses)
            remove: Don't include the matching item at all.
    """
    _allowed_behaviors = ["left", "right", "remove"]
    if behavior not in _allowed_behaviors:
        raise ValueError(f"behavior must be one of {_allowed_behaviors}")
    iterator = iter(iterable)
    true_part = []
    false_part = []
    for item in iterator:
        if predicate(item):
            true_part.append(item)
        else:
            if behavior == "left":
                true_part.append(item)
            elif behavior == "right":
                false_part.append(item)

            false_part.extend(iterator)
            break
    return true_part, false_part


def _compact(lst):
    """Remove Nones from the list."""
    return [x for x in lst if x is not None]


def parse_header(lines):
    name_line = lines.pop(0)

    def is_not_terminal_header(header):
        return header not in terminal_headers

    header_lines, other_lines = _partition_while(
        is_not_terminal_header, lines, behavior="left"
    )
    non_empty_header_lines = [line for line in header_lines if line.strip()]
    return [name_line, *non_empty_header_lines], other_lines


def _parse_table(page: str, skip_last_row: bool = True, skip_last_column: bool = True):
    if any(title for title in SKIP if page.lstrip().startswith(title)):
        return None
    lines = page.strip().split("\n")
    table_name = lines.pop(0)
    keys, lines = parse_header(lines)

    all_values = []
    index = 0
    num_keys = len(keys)
    num_lines = len(lines)
    while index < num_lines:
        all_values.append(lines[index : index + num_keys])
        index += len(keys)

    if skip_last_row:
        all_values.pop()

    df = pd.DataFrame(all_values, columns=keys)
    if skip_last_column:
        df.drop(df.columns[[-1]], axis=1, inplace=True)

    return (table_name, df)


def extract_tables(pdf_path: Path):
    doc = pymupdf.open(pdf_path)
    _results = dict(_compact([_parse_table(page.get_text()) for page in doc]))

    print()
    for name, df in _results.items():
        print(name)
        print(df)

    doc.close()

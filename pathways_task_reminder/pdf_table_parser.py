import pymupdf
import numpy as np
import pandas as pd
from pathways_task_reminder import constants as const

from pathways_task_reminder.utils.enumerable import compact, partition_while


from pathlib import Path


class PDFTableParser:
    SKIP_TABLES = [const.THIS_WEEKS_ASSIGNMENTS]
    TERMINAL_HEADERS = ["Total", "Max"]

    def extract_tables(self, pdf_path: Path) -> dict[str, pd.DataFrame]:
        doc = pymupdf.open(pdf_path)
        tables = dict(compact([self._parse_table(page.get_text()) for page in doc]))
        doc.close()
        return tables

    def _parse_table(
        self, page: str, skip_last_row: bool = True, skip_last_column: bool = True
    ):
        if any(title for title in self.SKIP_TABLES if page.lstrip().startswith(title)):
            return None
        lines = page.strip().split("\n")
        table_name = lines.pop(0)
        keys, lines = self._parse_header(lines)

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

        # interpret all strings as integers after replacing non-breaking space
        # with NaN
        df.iloc[:, 1:] = (
            df.iloc[:, 1:]
            .replace("\xa0", np.nan)
            .apply(pd.to_numeric, errors="coerce")
            .astype("Int64")
        )
        return (table_name, df)

    def _parse_header(self, lines):
        name_line = lines.pop(0)

        def is_not_terminal_header(header):
            return header not in self.TERMINAL_HEADERS

        header_lines, other_lines = partition_while(
            is_not_terminal_header, lines, behavior="left"
        )
        non_empty_header_lines = [line for line in header_lines if line.strip()]
        return [name_line, *non_empty_header_lines], other_lines

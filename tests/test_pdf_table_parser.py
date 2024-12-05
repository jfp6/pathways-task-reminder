import pandas as pd
from pathways_task_reminder.pdf_table_parser import PDFTableParser


def test_extract_tables(pathways_pdf_path):
    tables = PDFTableParser().extract_tables(pathways_pdf_path)
    assert isinstance(tables, dict)
    for name, table in tables.items():
        assert isinstance(name, str)
        assert isinstance(table, pd.DataFrame)

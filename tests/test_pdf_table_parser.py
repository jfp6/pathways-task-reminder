from pathlib import Path
from pathways_task_reminder.pdf_table_parser import PDFTableParser


def test_extract_tables():
    path = Path("test.pdf")
    tables = PDFTableParser().extract_tables(path)
    print(tables)

from pathlib import Path
from pathways_task_reminder.utils.pdf_processing import extract_tables


def test_extract_tables():
    path = Path("test.pdf")
    tables = extract_tables(path)

import pytest
from pathways_task_reminder.student_reporter import StudentReporter


@pytest.mark.skip
def test_create_student_tables_from_pdf(pathways_pdf_path):
    reporter = StudentReporter.create_from_pdf(pathways_pdf_path)
    tables = reporter.create_student_tables()


def test_create_student_tables(tables):
    reports = StudentReporter().create_student_reports(tables)
    for student, report in reports.items():
        print(f"<p>{student}</p>")
        print()
        print(report.to_html())

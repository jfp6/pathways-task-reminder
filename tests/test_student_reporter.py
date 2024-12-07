import pytest
from pathways_task_reminder.student_reporter import StudentReporter


@pytest.fixture
def student_report(tables):
    reports = StudentReporter().create_student_reports(tables)
    return reports[0]


@pytest.mark.skip
def test_create_student_tables_from_pdf(pathways_pdf_path):
    reporter = StudentReporter.create_from_pdf(pathways_pdf_path)
    _ = reporter.create_student_tables()


def test_create_student_tables(tables):
    reports = StudentReporter().create_student_reports(tables)
    for student, report in reports.items():
        print(f"<p>{student}</p>")
        print()
        print(report.to_html())


def test_to_image_path(student_report):
    path = student_report.to_image_path()
    print(path)

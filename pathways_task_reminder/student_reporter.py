from pathways_task_reminder.pdf_table_parser import PDFTableParser
import dataclasses
import pandas as pd
from pathways_task_reminder import constants as const


from tabulate import tabulate


def dataframe_to_tabulate_table(df, tablefmt: str = "github"):
    """
    Converts a Pandas DataFrame to a format suitable for tabulate, including indices and handling <NA> values.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        str: The formatted table as a string.
    """
    display_df = df.where(pd.notna(df), None)

    first_header = df.columns.name or df.index.name
    header_row = [first_header, *display_df.columns.tolist()]
    rows = [[index] + row.tolist() for index, row in display_df.iterrows()]

    tabulate_data = tabulate(
        rows, headers=header_row, tablefmt=tablefmt, numalign="right"
    )
    return tabulate_data


@dataclasses.dataclass
class StudentReport:
    ASSIGNMENT_INDEX = "week"
    ASSIGNMENT_VALUES = "units"

    SKILL_INDEX = ["level", "units"]
    SKILL_VALUES = "skill"
    MEAN_UNITS_TEXT = "Your Average Units Completed Each Week of The Semester"

    skill_df: pd.DataFrame
    assignment_series: pd.Series

    def to_html(self):
        assignment_df = self.assignment_series.to_frame(name=self.ASSIGNMENT_VALUES).T
        parts = [
            "<br/>",
            dataframe_to_tabulate_table(assignment_df, tablefmt="html"),
            "<br/>",
            dataframe_to_tabulate_table(self.skill_df, tablefmt="html"),
            "<br/>",
            f"{self.MEAN_UNITS_TEXT}: {self.mean_units_per_week()}",
            "<br/>",
        ]
        return "\n".join(parts)

    def mean_units_per_week(self):
        return self.assignment_series.mean()


class StudentReporter:
    @classmethod
    def create_from_pdf(cls, pdf_path):
        tables = PDFTableParser().extract_tables(pdf_path)
        return cls().create_student_reports(tables)

    def create_student_reports(self, tables):
        student_series = self._create_student_series(tables)
        return self._create_student_reports_from_series(student_series)

    def _create_student_series(self, tables):
        return {key: self._extract_students(df) for key, df in tables.items()}

    @staticmethod
    def _extract_students(df):
        """Returns a list of student series."""
        return {
            row[0]: pd.Series(row[1:], index=df.columns[1:])
            for row in df.itertuples(index=False)
        }

    def _create_student_reports_from_series(self, student_series_by_table_name):
        student_names = student_series_by_table_name[
            const.STUDENT_LEVEL_BY_SKILL
        ].keys()
        return {
            name: self._assemble_student(name, student_series_by_table_name)
            for name in student_names
        }

    def _assemble_student(self, name, student_series):
        skill_levels = student_series[const.STUDENT_LEVEL_BY_SKILL][name]
        skill_nums = student_series[const.TOTAL_ASSIGNMENTS_BY_SKILL][name]

        skill_df = pd.DataFrame(
            [skill_levels, skill_nums], index=StudentReport.SKILL_INDEX
        )
        skill_df.columns.name = StudentReport.SKILL_VALUES
        assignment_series = student_series[const.ASSIGNMENTS_SUBMITTED_BY_WEEK][name]
        assignment_series.index.name = StudentReport.ASSIGNMENT_INDEX
        return StudentReport(skill_df=skill_df, assignment_series=assignment_series)

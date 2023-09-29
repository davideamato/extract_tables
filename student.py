"""
    Contains the objects for table extraction 
"""

from collections import Counter
from pdf_strings import (
    desired_tables,
    detail_string,
    valid_exams,
    ib_permutations,
)

from pandas import isna

from grade_entry import GradeEntry


class Student:
    """
    Class for a single pdf/student
    """

    def __init__(self, id_num, extracted_tables, table_headers, internal_mapping):
        self.unique_id = id_num
        self.internal_mapping = internal_mapping

        self.completed_qualifications = None
        self.uncompleted_qualifications = None
        self.exam_results = None

        target_tables = desired_tables()

        for header, tbl in zip(table_headers, extracted_tables):
            if header == target_tables[0]:
                # print("")
                # print("Completed Qualification")
                # print(tbl)
                self.completed_qualifications = tbl
            elif header == target_tables[1]:
                # print("")
                # print("Predicted Grades")
                # print(tbl)
                self.uncompleted_qualifications = tbl
            elif header == target_tables[2]:
                # print("")
                # print("Exam Results")
                # print(tbl)
                self.exam_results = tbl

        self.predicted_entries = []
        self.completed_entries = []
        self.results_entries = []

        self.predicted_grade_entries()
        self.examresult_entries()
        self.completed_grade_entries()

        self.which_grades = {
            "results": self.results_entries,
            "completed": self.completed_entries,
            "predicted": self.predicted_entries,
        }

        self.sanitise_ib_grades()

    def __repr__(self):
        return "{} \n {} \n {}".format(
            self.completed_qualifications,
            self.uncompleted_qualifications,
            self.exam_results,
        )

    def sanitise_ib_grades(self):

        all_quals = set(self.get_all_qualifications())

        # Intersection not empty => it is IB
        if all_quals & ib_permutations():
            # Get grade entries that are not empty
            non_empty_grade_entries_key = [
                entry_key
                for entry_key in self.which_grades
                if self.which_grades.get(entry_key)
            ]

            # Iterate over non-empty grade entries
            for grade_entries_key in non_empty_grade_entries_key:

                current_entries = self.which_grades.get(grade_entries_key)

                # Filter out standard level subjects and extended essays
                grade_entries = [
                    entry
                    for entry in current_entries
                    if not (
                        "S" in str(entry.grade).upper()
                        or "stand lvl" in str(entry.subject).lower()
                        or "standard lvl" in str(entry.subject).lower()
                        or 'ext essay' in str(entry.subject).lower()
                        or 'extended essay' in str(entry.subject).lower()
                    )
                ]

                for entry in grade_entries:
                    # Convert to string
                    if not isinstance(entry.grade, str):
                        grade = str(entry.grade)
                    else:
                        grade = entry.grade

                    if "H" in grade:
                        # If higher level, remove H
                        entry.grade = grade.replace("H", "")
                        entry.grade_info[0] = entry.grade
                    elif "h" in grade:
                        entry.grade = grade.replace("h", "")
                        entry.grade_info[0] = entry.grade

                    # Get actual subject name
                    subject = entry.subject.split('Value:')[0].split('Predicted Grade:')[0].split("Grade:")[0].strip()
                    entry.subject = subject
                    entry.grade_info[1] = subject

                self.which_grades[grade_entries_key] = grade_entries

    def get_all_qualifications(self):
        return [
            item.qualification
            for grade_entries in self.which_grades.values()
            if grade_entries
            for item in grade_entries
        ]

    def unique_qualifications(self):
        return set(self.get_all_qualifications())

    def get_main_qualification(self):
        qualifications = self.get_all_qualifications()
        if not qualifications:
            return ""

        if len(set(qualifications)) == 1:
            return qualifications[0]
        else:
            return Counter(qualifications).most_common(1)[0][0]

    def get_grade_for_qualification(self, target_qualification):
        for values in self.which_grades.values():
            if values:
                for item in values:
                    # It is the qualification we are looking for.
                    # The grade is not None AND year is not None (implies it is a module/detail entry)
                    if (
                        target_qualification == item.qualification
                        and item.grade is not None
                        and item.year is not None
                    ):
                        yield item.grade

    def is_detailed_entry(self, input_qualification, rowCounter):
        target = input_qualification["Date"][rowCounter]
        if not isinstance(target, str):
            return False

        if target not in detail_string():
            return False

        return True

    def handle_detailed_entry(self, input_qualification, rowCounter):

        if "Exam" in set(input_qualification.columns):
            qualification_identifier = "Exam"
        elif "Exam Level" in set(input_qualification.columns):
            qualification_identifier = "Exam Level"
        else:
            raise NotImplementedError

        if not isna(input_qualification[qualification_identifier][rowCounter - 1]):
            qualification = input_qualification[qualification_identifier][
                rowCounter - 1
            ]
        else:
            qualification = None

        output = []

        if self.is_qual_valid(qualification):

            qualification = self.get_valid_qualification(qualification)

            all_module_details = input_qualification["Body"][rowCounter]

            # Ignores the first entry which would just be the date
            individual_modules = all_module_details.split("Title:")[1:]
            # print(individual_modules)
            for module in individual_modules:

                module_info = module.split("Date:")[0]
                predicted = False
                exam = False

                if "Predicted Grade:" in module_info:
                    grade = module_info.split("Predicted Grade:")[1]
                    predicted = True
                elif "Grade:" in module_info:
                    grade = module_info.split("Grade:")[1]
                elif "Value:" in module_info:
                    grade = module_info.split("Value:")[1]
                else:
                    grade = None

                if grade is not None:
                    grade = ''.join(e for e in grade if e.isnumeric())

                entry = GradeEntry(
                    qualification,
                    module_info,
                    grade,
                    predicted,
                    None,
                    exam,
                )
                output.append(entry)

        return output

    def completed_grade_entries(self):
        if self.completed_qualifications is None:
            return None

        for row in self.completed_qualifications.index:

            if self.is_qual_valid(self.completed_qualifications["Exam"][row]):

                qual = self.get_valid_qualification(self.completed_qualifications['Exam'][row])

                entry = GradeEntry(
                    qual,
                    self.completed_qualifications["Subject"][row],
                    self.completed_qualifications["Grade"][row],
                    False,
                    self.completed_qualifications["Date"][row].split("-")[-1],
                    False,
                )

                self.completed_entries.append(entry)

            elif self.is_detailed_entry(self.completed_qualifications, row):

                detailed_entries = self.handle_detailed_entry(
                    self.completed_qualifications, row
                )
                self.completed_entries += detailed_entries

        return self.completed_entries

    def examresult_entries(self):
        if self.exam_results is None:
            return None

        for row in self.exam_results.index:

            if self.is_qual_valid(self.exam_results["Exam Level"][row]):

                qual = self.get_valid_qualification(self.exam_results['Exam Level'][row])
                entry = GradeEntry(
                    qual,
                    self.exam_results["Subject"][row],
                    self.exam_results["Grade"][row],
                    False,
                    self.exam_results["Date"][row].split("-")[-1],
                    True,
                )

                self.results_entries.append(entry)

            elif self.is_detailed_entry(self.exam_results, row):

                detailed_entries = self.handle_detailed_entry(self.exam_results, row)
                self.results_entries += detailed_entries

        return self.results_entries

    def predicted_grade_entries(self):
        if self.uncompleted_qualifications is None:
            return None

        for row in self.uncompleted_qualifications.index:

            is_pred_grade = isna(
                self.uncompleted_qualifications["Predicted\rGrade"][row]
            )
            is_grade = isna(self.uncompleted_qualifications["Grade"][row])

            if is_pred_grade ^ is_grade:

                if is_pred_grade:
                    valid_grade = self.uncompleted_qualifications["Grade"][row]
                else:
                    valid_grade = self.uncompleted_qualifications["Predicted\rGrade"][
                        row
                    ]

                if isna(self.uncompleted_qualifications["Exam"][row]):
                    qualification = self.uncompleted_qualifications["Body"][row]
                else:
                    qualification = self.uncompleted_qualifications["Exam"][row]

                if self.is_qual_valid(qualification):

                    qualification = self.get_valid_qualification(qualification)

                    entry = GradeEntry(
                        qualification,
                        self.uncompleted_qualifications["Subject"][row],
                        valid_grade,
                        True,
                        self.uncompleted_qualifications["Date"][row].split("-")[-1],
                        False,
                    )
                    self.predicted_entries.append(entry)

            elif (not is_pred_grade) & (not is_grade):

                if "Unnamed" in str(self.uncompleted_qualifications["Grade"][row]):
                    valid_grade = self.uncompleted_qualifications["Predicted\rGrade"][
                        row
                    ]
                else:
                    valid_grade = self.uncompleted_qualifications["Grade"][row]

                if isna(self.uncompleted_qualifications["Exam"][row]):
                    qualification = self.uncompleted_qualifications["Body"][row]
                else:
                    qualification = self.uncompleted_qualifications["Exam"][row]

                if self.is_qual_valid(qualification):

                    qualification = self.get_valid_qualification(qualification)

                    entry = GradeEntry(
                        qualification,
                        self.uncompleted_qualifications["Subject"][row],
                        valid_grade,
                        True,
                        self.uncompleted_qualifications["Date"][row].split("-")[-1],
                        False,
                    )
                    self.predicted_entries.append(entry)

            elif self.is_detailed_entry(self.uncompleted_qualifications, row):

                detailed_entries = self.handle_detailed_entry(self.uncompleted_qualifications, row)
                self.predicted_entries += detailed_entries

        return self.predicted_entries

    def is_qual_valid(self, qual):
        if isna(qual):
            return False

        qual = ''.join(char for char in str(qual) if char.isprintable() and not char.isspace())
        if qual in [''.join(char for char in exam if char.isprintable() and not char.isspace()) for exam in valid_exams(self.internal_mapping)]:
            return True
        else:
            return False

    def get_valid_qualification(self, qual):
        return self.internal_mapping.get(''.join(e for e in str(qual) if e.isprintable() and not e.isspace()))

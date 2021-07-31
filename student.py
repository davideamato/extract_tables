'''
    Contains the objects for table extraction 
'''

from utils import InputError, completed_qualification_valid_exams, desired_tables, detail_string, escape_backslash_r, exam_results_valid_exams, is_abs_path

from pandas import isna
import os


class GradeEntry:
    '''
        Class to store the grades
    '''

    def __init__(self, qualification, subject, grade, is_predicted, year):
        self.qualification = escape_backslash_r(qualification)
        self.subject = escape_backslash_r(subject)
        self.grade = grade
        self.is_predicted = is_predicted
        self.year = year

    def __repr__(self):
        return r"Qualification: {} Subject: {} Grade: {} Year: {} Predicted {}".format(
            self.qualification, self.subject, self.grade, self.year, self.is_predicted)

    def __str__(self):
        return r"Qualification: {} Subject: {} Grade: {} Year: {} Predicted {}".format(
            self.qualification, self.subject, self.grade, self.year, self.is_predicted)


class ExtractedStudents:
    '''
        Class that stores all the students and co-ordinates the output
    '''

    def __init__(self, applicant_ids):
        self.student_ids = applicant_ids

        self.num_students = len(applicant_ids)

        self.all_students = [None]*self.num_students

        self.index = self.num_students

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration

        self.index -= 1

        return self.all_students[self.index]

    def add_student_sequentially(self, new_student, counter):
        if new_student.ucas_id == self.student_ids[counter]:
            self.all_students[counter] = new_student
        else:
            raise RuntimeError("The order of adding students is incorrect \n"
                               "This should be done sequentially IDs in list should correspond")

    def populate_worksheet(self, desired_data, ws):
        if desired_data not in self.all_students[0].which_grades.keys():
            raise InputError(False, "Key given not found in dictionary")

        ws.cell(row=1, column=1, value="{}".format("UCAS ID"))
        ws.cell(row=1, column=2, value="{}".format("Qualification Type"))

        for i in range(0, 8, 2):
            ws.cell(row=1, column=3 + i, value="{}".format("Subject"))
            ws.cell(row=1, column=4 + i, value="{}".format("Grade"))

        lb = 2

        for row_counter, student in zip(range(lb, self.num_students+lb), self.all_students):

            ws.cell(row=row_counter, column=1,
                    value="{}".format(student.ucas_id))

            if student.which_grades[desired_data]:
                ws.cell(row=row_counter, column=2, value="{}".format(
                    student.which_grades[desired_data][0].qualification))
                col_counter = 3

                for entry in student.which_grades[desired_data]:
                    ws.cell(row=row_counter, column=col_counter,
                            value="{}".format(entry.subject))
                    ws.cell(row=row_counter, column=col_counter +
                            1, value="{}".format(entry.grade))
                    col_counter += 2

        return ws

    def write_to_excel(self, input_abs_path):
        is_abs_path(input_abs_path)

        from openpyxl import Workbook

        wb = Workbook()

        # Create and populate workshets
        completed = wb.create_sheet("Completed Qualifications")
        completed = self.populate_worksheet("completed", completed)

        predicted = wb.create_sheet("Predicted Grades")
        predicted = self.populate_worksheet("predicted", predicted)

        exam_results = wb.create_sheet("Exam Results")
        exam_results = self.populate_worksheet("results", exam_results)

        compiled_single = wb.create_sheet("Compiled", 0)

        wb.save(os.path.join(input_abs_path, "output.xlsx"))

        return 0


class StudentGrades:
    '''
        Class for a single pdf/student
    '''

    def __init__(self, id, extracted_tables, table_headers):
        self.ucas_id = id

        self.completed_qualifications = None
        self.uncompleted_qualifications = None
        self.exam_results = None

        target_tables = desired_tables()

        for header, tbl in zip(table_headers, extracted_tables):
            if header == target_tables[0]:
                self.completed_qualifications = tbl
            elif header == target_tables[1]:
                self.uncompleted_qualifications = tbl
            elif header == target_tables[2]:
                self.exam_results = tbl

        self.predicted_entries = []
        self.completed_entries = []
        self.results_entries = []

        self.predicted_grade_entries()
        self.examresult_entries()
        self.completed_grade_entries()

        self.which_grades = {"completed": self.completed_entries,
                             "predicted": self.predicted_entries,
                             "results": self.results_entries}

    def __repr__(self):
        return "{} \n {} \n {}".format(self.completed_qualifications,
                                       self.uncompleted_qualifications,
                                       self.exam_results)

    # def handle_detailed_entry(self, input_qualification, rowCounter):
    #     target = input_qualification['Date'][rowCounter]
    #     if type(target) is str:
    #         if target in detail_string():
    #             output = []
    #             all_module_details = qualification = self.uncompleted_qualifications['Body'][row]

    #         elif type(self.uncompleted_qualifications['Date'][row]) is str:
    #             if is_pred_grade & is_grade and self.uncompleted_qualifications['Date'][row] in detail_string():
    #                 all_module_details = qualification = self.uncompleted_qualifications['Body'][row]
    #                 individual_modules = all_module_details.split("Title:")
    #                 print(individual_modules)
    #                 for module in individual_modules:
    #                     module_info = module.split("Date:")[0]
    #                     entry = GradeEntry(
    #                         None,
    #                         module_info,
    #                         None,
    #                         True,
    #                         None,
    #                     )
    #                     self.predicted_entries.append(entry)

    def completed_grade_entries(self):
        if self.completed_qualifications is None:
            return None

        for row in self.completed_qualifications.index:

            if self.is_completed_qual_valid(row):

                entry = GradeEntry(
                    self.completed_qualifications['Exam'][row],
                    self.completed_qualifications['Subject'][row],
                    self.completed_qualifications['Grade'][row],
                    False,
                    self.completed_qualifications['Date'][row].split("-")[-1],
                )

                self.completed_entries.append(entry)

        return self.completed_entries

    def is_completed_qual_valid(self, row):
        if isna(self.completed_qualifications['Exam'][row]):
            return False

        if self.completed_qualifications['Exam'][row] in completed_qualification_valid_exams():
            return True
        else:
            return False

    def examresult_entries(self):
        if self.exam_results is None:
            return None

        for row in self.exam_results.index:

            if self.is_examresult_valid(row):

                entry = GradeEntry(
                    self.exam_results['Exam Level'][row],
                    self.exam_results['Subject'][row],
                    self.exam_results['Grade'][row],
                    False,
                    self.exam_results['Date'][row].split("-")[-1],
                )

                self.results_entries.append(entry)

        return self.results_entries

    def is_examresult_valid(self, row):
        if isna(self.exam_results['Exam Level'][row]):
            return False

        if self.exam_results['Exam Level'][row] in exam_results_valid_exams():
            return True
        else:
            return False

    def predicted_grade_entries(self):
        if self.uncompleted_qualifications is None:
            return None

        for row in self.uncompleted_qualifications.index:

            is_pred_grade = isna(
                self.uncompleted_qualifications['Predicted\rGrade'][row])
            is_grade = isna(self.uncompleted_qualifications['Grade'][row])

            if is_pred_grade ^ is_grade:

                if is_pred_grade:
                    valid_grade = self.uncompleted_qualifications['Grade'][row]
                else:
                    valid_grade = self.uncompleted_qualifications['Predicted\rGrade'][row]

                if isna(self.uncompleted_qualifications['Body'][row]):
                    qualification = self.uncompleted_qualifications['Exam'][row]
                else:
                    qualification = self.uncompleted_qualifications['Body'][row]

                entry = GradeEntry(
                    qualification,
                    self.uncompleted_qualifications['Subject'][row],
                    valid_grade,
                    True,
                    self.uncompleted_qualifications['Date'][row].split(
                        "-")[-1],
                )
                self.predicted_entries.append(entry)

            elif type(self.uncompleted_qualifications['Date'][row]) is str:
                if is_pred_grade & is_grade and self.uncompleted_qualifications['Date'][row] in detail_string():
                    all_module_details = qualification = self.uncompleted_qualifications[
                        'Body'][row]
                    individual_modules = all_module_details.split("Title:")
                    print(individual_modules)
                    for module in individual_modules:
                        module_info = module.split("Date:")[0]
                        entry = GradeEntry(
                            None,
                            module_info,
                            None,
                            True,
                            None,
                        )
                        self.predicted_entries.append(entry)

        return self.predicted_entries


from utils import desired_tables, raw_table_headers

import pandas as pd

class GradeEntry:
    def __init__(self, qualification, subject, grade, is_predicted, year):
        self.qualification = qualification
        self.subject = subject
        self.grade = grade
        self.is_predicted = is_predicted
        self.year = year

    def __repr__(self):
        # return "Entry Qualification: %s"
        return "Qualification: %s Subject: %s Grade: %s Year: %s Is Predicted? %r" \
            % (self.qualification, self.subject, self.grade, self.year, self.is_predicted)

    def __str__(self):
        return "Qualification: %s \n Subject: %s \n Grade: %s \n Year: %s \n Is Predicted? %r" \
            % (self.qualification, self.subject, self.grade, self.year, self.is_predicted)

class ExtractedStudents:
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
            raise RuntimeError("The order of adding students is incorrect \n" \
                "This should be done sequentially IDs in list should correspond")

    def write_to_file(self, input_abs_path):
        return 0

    

class StudentGrades:

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

        self.not_yet_completed_predicted_grades()        

    def not_yet_completed_predicted_grades(self):
        if self.uncompleted_qualifications is not None:

            for row in self.uncompleted_qualifications.index:
                is_pred_grade = pd.isna(self.uncompleted_qualifications['Predicted\rGrade'][row])
                is_grade = pd.isna(self.uncompleted_qualifications['Grade'][row])
                if is_pred_grade ^ is_grade :
                    if is_pred_grade:
                        valid_grade = self.uncompleted_qualifications['Grade'][row] 
                    else:
                        valid_grade = self.uncompleted_qualifications['Predicted\rGrade'][row] 

                    if pd.isna(self.uncompleted_qualifications['Body'][row]):
                        qualification = self.uncompleted_qualifications['Exam'][row]
                    else:
                        qualification = self.uncompleted_qualifications['Body'][row] 

                    entry = GradeEntry(
                        qualification,
                        self.uncompleted_qualifications['Subject'][row],
                        valid_grade,
                        True,
                        self.uncompleted_qualifications['Date'][row].split("-")[-1],
                    )
                    self.predicted_entries.append(entry)

        return self.predicted_entries








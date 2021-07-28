
from utils import desired_tables

class ExtractedStudents:
    def __init__(self, applicant_ids):
        self.student_ids = applicant_ids 

        num_students = len(applicant_ids)

        self.all_students = [None]*num_students

    def add_student_sequentially(self, new_student, counter):
        if new_student.ucas_id == self.student_ids[counter]:
            self.all_students[counter] = new_student
        else:
            raise RuntimeError("The order of adding students is incorrect \n" \
                "This should be done sequentially IDs in list should correspond")

class StudentGrades:

    def __init__(self, id, extracted_tables, table_headers):
        self.ucas_id = id

        target_tables = desired_tables() 

        for header, tbl in zip(table_headers, extracted_tables):
            if header == target_tables[0]:
                self.completed_qualifications = tbl 
            elif header == target_tables[1]:
                self.uncompleted_qualifications = tbl
            elif header == target_tables[2]:
                self.exam_results = tbl




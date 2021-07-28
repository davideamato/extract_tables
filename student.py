
from utils import desired_tables

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




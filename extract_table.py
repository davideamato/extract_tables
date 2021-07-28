
import subprocess

from collections import Counter

import os
import tabula

from utils import desired_tables, get_all_files_in_dir, fix_broken_table, get_applicant_ids
from student import StudentGrades

path_to_files = os.path.abspath("pdfs/")

all_files = get_all_files_in_dir(path_to_files)
applicant_ids = get_applicant_ids(path_to_files)
# print(applicant_ids)

TARGET_TABLES = desired_tables()
EXIT_STRING = 'Type of school, college or training centre:'

# tables = tabula.read_pdf(file, pages="all", lattice=True, guess=True, pandas_options={"header": 0},)
# for table in tables:
#     print(table)
#     print(table.columns)

#     # if 'Type of school, college or training centre:' in table.columns:
#     #     print("EXIT CONDITION")
#     print("")

all_students = [0]*len(all_files)
counter = 0

for file, app_id in zip(all_files, applicant_ids):

    # print(app_id)

    page_number = 2
    exit_loop = False

    grade_tables = []
    grade_counters = []

    while True:
        try:
            tables = tabula.read_pdf(file, pages=str(page_number), lattice=True, guess=True, pandas_options={"header": 0},)
        except subprocess.CalledProcessError:
            break

        for table in tables:

            table_headers = table.columns
            header_counter = Counter(list(table_headers.values))

            if header_counter in TARGET_TABLES:
                table = fix_broken_table(page_number, table, file)
                grade_tables.append(table)
                grade_counters.append(header_counter)

                print(table)
                print("")
            elif EXIT_STRING in table_headers:
                exit_loop = True 

        if exit_loop:
            all_students[counter] = StudentGrades(app_id, grade_tables, grade_counters)
            break

        page_number += 1

    counter += 1



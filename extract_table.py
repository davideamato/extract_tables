
from logging import exception
import subprocess
import tabula
import os

from collections import Counter

from utils import desired_tables, get_all_files_in_dir, fix_broken_table, get_applicant_ids

path_to_files = os.path.abspath("pdfs/")

all_files = get_all_files_in_dir(path_to_files)
applicant_ids = get_applicant_ids(path_to_files)
print(applicant_ids)

file = all_files[0]
id = applicant_ids[0]

# tables = tabula.read_pdf(file, pages="all", lattice=True, guess=True, pandas_options={"header": 0},)

# for table in tables:
#     print(table)
#     print(table.columns)

#     # if 'Type of school, college or training centre:' in table.columns:
#     #     print("EXIT CONDITION")
#     print("")


target_tables = desired_tables()
exit_string = 'Type of school, college or training centre:'

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
        if header_counter in target_tables:
            table = fix_broken_table(page_number, table, file)
            grade_tables.append(table)
            grade_counters.append(header_counter)

            print(table)
            print("")
        elif exit_string in table_headers:
            exit_loop = True 


    if exit_loop:
        break


    page_number += 1




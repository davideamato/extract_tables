
from logging import exception
import subprocess
import tabula
import os

from collections import Counter

from utils import get_all_files_in_dir, fix_broken_table


all_files = get_all_files_in_dir(os.path.abspath("pdfs/"))
# print(all_files)

# file = 'UCAS_Applicant_1462950865_unicode.pdf'
file = all_files[0]


acheived_headers = ['Date', 'Body', 'Exam', 'Subject', 'Grade', 'Result', 'Centre Number']
achieved_counter = Counter(acheived_headers)
predicted_headers = ['Date', 'Body', 'Exam', 'Subject', 'Grade', 'Result', 'Centre\rNumber', 'Predicted\rGrade']
predicted_counter = Counter(predicted_headers)
examresults_headers = ['Date', 'Body', 'Exam Level', 'Sitting', 'Subject', 'Grade']
examresults_counter = Counter(examresults_headers)

page_number = 2
exit_loop = False

while True:
    try:
        tables = tabula.read_pdf(file, pages=str(page_number), lattice=True, guess=True, pandas_options={"header": 0},)
    except subprocess.CalledProcessError:
        break

    for table in tables:
        # if not table.index:
        #     table.columns 

        header_counter = Counter(list(table.columns.values))
        if header_counter == achieved_counter:
            fix_broken_table(page_number, table, file)

            print(table)
        elif header_counter == predicted_counter or header_counter == examresults_counter:
            fix_broken_table(page_number, table, file)
            # exit_loop = True

            print(table)

    if exit_loop:
        break


    page_number += 1




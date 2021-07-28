
from logging import exception
import subprocess
import tabula
import os

from collections import Counter

from utils import desired_tables, get_all_files_in_dir, fix_broken_table


all_files = get_all_files_in_dir(os.path.abspath("pdfs/"))
# print(all_files)

# file = 'UCAS_Applicant_1462950865_unicode.pdf'
file = all_files[0]
tables = tabula.read_pdf(file, pages="all", lattice=True, guess=True, pandas_options={"header": 0},)

for table in tables:
    print(table)
    print(len(table.columns))
    print("")


target_tables = desired_tables()

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
        if header_counter in target_tables:
            table = fix_broken_table(page_number, table, file)

            print(table)
            print("")

    if exit_loop:
        break


    page_number += 1




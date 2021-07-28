'''
    File extract table of grades from UCAS forms
'''

import subprocess

from collections import Counter

import os
import tabula

from utils import desired_tables, get_all_files_in_dir, fix_broken_table, get_applicant_ids
from student import ExtractedStudents
from student import StudentGrades

path_to_files = os.path.abspath("pdfs/")

# Generates full path to the files to extract data from
all_files = get_all_files_in_dir(path_to_files)
# Extracts UCAS IDs from file name
applicant_ids = get_applicant_ids(path_to_files)
# print(applicant_ids)

# From the PDFs, these are the headers of the tables we want
# They have been placed in a counter for easy comparison
TARGET_TABLES = desired_tables()
# First table after the desired ones that always occur
EXIT_STRING = 'Type of school, college or training centre:'

# Initialise object to store extracted information
all_students = ExtractedStudents(applicant_ids)
counter = 0

print("Extracting tables for {} students".format(len(all_files)))

# Iterate over all files and applicant IDs
for file, app_id in zip(all_files, applicant_ids):

    # print("")
    # print(app_id)

    # Start on 2nd page as 1st doesn't contain impt info 
    page_number = 2
    exit_loop = False

    # Initialise list to store the pandas dataframes from tabula
    grade_tables = []
    grade_counters = []

    # Total number of pages not known before hand
    while True:
        try:
            # Extract table from pdf
            tables = tabula.read_pdf(file, pages=str(page_number), lattice=True,
                                     guess=True, pandas_options={"header": 0},)
        except subprocess.CalledProcessError:
            all_students.add_student_sequentially(
                StudentGrades(app_id, grade_tables, grade_counters), counter)
            # If EOF reached before exit table
            # This shouldn't happen
            break

        # Iterate over all tables on the page
        for table in tables:

            # Get the table header
            table_headers = table.columns
            header_counter = Counter(list(table_headers.values))

            # Determine if it is a targe table
            if header_counter in TARGET_TABLES:
                # Fix table if it is across two pages
                table = fix_broken_table(page_number, table, file)

                # Add to list that stores the tables
                grade_tables.append(table)
                grade_counters.append(header_counter)

                # print(table)
                # print("")
            elif EXIT_STRING in table_headers:
                # Exit condition
                exit_loop = True

        if exit_loop:
            # Add completed form to all students
            all_students.add_student_sequentially(
                StudentGrades(app_id, grade_tables, grade_counters), counter)
            break

        # Go to next page in document
        page_number += 1

    # Go to next student
    counter += 1

all_students.write_to_file(path_to_files)

for student in all_students:
    print("UCAS ID: {}".format(student.ucas_id))
    print(student.uncompleted_qualifications)
    print("")
    # print("{}".format(student.predicted_entries))
    if student.predicted_entries:
        for entry in student.predicted_entries:
            print(entry)
            # print("{}".format(entry.qualification))
            # print("{}".format(entry.subject))
            # print("{}".format(entry.grade))
    print("")
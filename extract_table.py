'''
    File extract table of grades from UCAS forms
'''

import subprocess

from collections import Counter
from tqdm import tqdm


import logging
import tabula

from utils import initialise_logger, desired_tables,  fix_broken_table, get_exit_string,  get_files_and_ids, get_internal_mapping
from student import ExtractedStudents
from student import Student
import settings

# import pandas as pd
# pd.set_option('display.max_columns', None)

PATH_TO_FILES = settings.path_to_pdfs_to_extract
INTERNAL_MAPPING = get_internal_mapping(
    settings.path_to_mapping_file, settings.qualification_mapping_sheet_name)
# print(INTERNAL_MAPPING)

# Generates full path to the files to extract data from
# Extracts unique IDs from file name
ALL_FILES, APPLICANT_IDS = get_files_and_ids(PATH_TO_FILES)
# print(ALL_FILES)
# print(APPLICANT_IDS)

# From the PDFs, these are the headers of the tables we want
# They have been placed in a counter for easy comparison
TARGET_TABLES = desired_tables()
# First table after the desired ones that always occur
EXIT_STRING = get_exit_string()

if __name__ == "__main__":

    initialise_logger()

    # Initialise object to store extracted information
    all_students = ExtractedStudents(APPLICANT_IDS, INTERNAL_MAPPING)
    counter = 0

    total_num_files = len(ALL_FILES)
    print("Extracting tables for {} students".format(total_num_files))

    pbar = tqdm(total=total_num_files, desc="Table Processing: ")
    # Iterate over all files and applicant IDs
    for file, app_id in zip(ALL_FILES, APPLICANT_IDS):

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
                    Student(app_id, grade_tables, grade_counters), counter)
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
                    Student(app_id, grade_tables, grade_counters), counter)
                # print("")
                break

            # Go to next page in document
            page_number += 1

        # Go to next student
        counter += 1
        pbar.update()

    pbar.close()

    # for student in all_students:
    #     print("ID: {}".format(student.unique_id))
    #     # print(student.uncompleted_qualifications)
    #     # print("")
    #     # print("{}".format(student.predicted_entries))
    #     if student.completed_entries:
    #         print("Completed Qualifications")
    #         # print(student.completed_qualifications)
    #         for entry in student.completed_entries:
    #             print(entry)
    #     print("")
    #     if student.predicted_entries:
    #         print("Predicted Grades")
    #         # print(student.uncompleted_qualifications)
    #         for entry in student.predicted_entries:
    #             print(entry)
    #     print("")
    #     if student.results_entries:
    #         print("Examination Results")
    #         # print(student.exam_results)
    #         for entry in student.results_entries:
    #             print(entry)
    #     print("")
    #     print("")

    all_students.write_to_excel(PATH_TO_FILES)

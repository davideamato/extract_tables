"""
    File extract table of grades from UCAS forms
"""

import subprocess

from collections import Counter
from tqdm import tqdm

import logging
import tabula

from utils import (
    check_output_dirs_exist,
    copy_file,
    copy_pdfs_to_pool,
    get_current_time,
    get_subject_mapping,
    initialise_logger,
    fix_broken_table,
    get_files_and_ids,
    update_previous_id_database,
    get_internal_mapping,
    order_pdfs_to_target_id_input,
)
from pdf_strings import (
    desired_tables,
    get_exit_string,
)
from extracted_students import ExtractedStudents
from student import Student
import settings

initialise_logger()

PATH_TO_FILES = settings.path_to_pdfs_to_extract
INTERNAL_MAPPING = get_internal_mapping(
    settings.path_to_mapping_file, settings.qualification_mapping_sheet_name
)
MATH_MAPPING = get_subject_mapping(settings.path_to_mapping_file, settings.maths_mapping_sheet_name)
PHYS_MAPPING = get_subject_mapping(settings.path_to_mapping_file, settings.physics_mapping_sheet_name)
FM_MAPPING = get_subject_mapping(settings.path_to_mapping_file, settings.further_maths_mapping_sheet_name)

# Generates full path to the files to extract data from
# Extracts unique IDs from file name
ALL_FILES, APPLICANT_IDS = get_files_and_ids(PATH_TO_FILES)

# From the PDFs, these are the headers of the tables we want
# They have been placed in a counter for easy comparison
TARGET_TABLES = desired_tables()
# First table after the desired ones that always occur
EXIT_STRING = get_exit_string()

if __name__ == "__main__":

    start_time = get_current_time()
    print(f"Start Time: {start_time}")

    check_output_dirs_exist()
    ALL_FILES, APPLICANT_IDS = order_pdfs_to_target_id_input(ALL_FILES, APPLICANT_IDS)

    # Initialise object to store extracted information
    all_students = ExtractedStudents(APPLICANT_IDS, MATH_MAPPING, PHYS_MAPPING, FM_MAPPING)
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
                tables = tabula.read_pdf(
                    file,
                    pages=str(page_number),
                    lattice=True,
                    guess=True,
                    pandas_options={"header": 0},
                )
            except subprocess.CalledProcessError:
                logging.warning("EOF reached before exit condition")
                logging.warning(f"Check file with ID: {app_id}")
                all_students.add_student_sequentially(
                    Student(app_id, grade_tables, grade_counters, INTERNAL_MAPPING), counter
                )
                copy_file(file, all_students, app_id)
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

                elif EXIT_STRING in table_headers:
                    # Exit condition
                    exit_loop = True

            if exit_loop:
                # Add completed form to all students
                all_students.add_student_sequentially(
                    Student(app_id, grade_tables, grade_counters, INTERNAL_MAPPING), counter
                )
                copy_file(file, all_students, app_id)
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

    all_students.write_to_excel(settings.output_path)
    copy_pdfs_to_pool(ALL_FILES)
    update_previous_id_database(
        settings.path_to_database_of_extracted_pdfs, APPLICANT_IDS
    )

    end_time = get_current_time()
    print(f"End Time: {end_time}")

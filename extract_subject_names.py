"""
    File to extract subject names from UCAS applications
"""

from email import header
import subprocess

from collections import Counter
from tqdm import tqdm


import tabula

from utils import (
    get_current_time,
    fix_broken_table,
    get_files_and_ids,
    get_internal_mapping,
    order_pdfs_to_target_id_input,
    escape_backslash_r,
    initialise_logger
)
from pdf_strings import (
    desired_tables,
    get_exit_string,
    ib_permutations,
    valid_exams,
    detail_string,
)
from pandas import isna

import settings


def is_qual_valid(qual):
    if isna(qual):
        return False

    qual = ''.join(char for char in str(qual) if char.isprintable() and not char.isspace())
    if qual in [''.join(char for char in exam if char.isprintable() and not char.isspace()) for exam in valid_exams(INTERNAL_MAPPING)]:
        return True
    else:
        return False

def get_valid_qualification(qual):
    return INTERNAL_MAPPING.get(''.join(e for e in str(qual) if e.isprintable() and not e.isspace()))

def is_detailed_entry(input_qualification, rowCounter):
    target = input_qualification["Date"][rowCounter]
    if not isinstance(target, str):
        return False

    if target not in detail_string():
        return False

    return True

def all_valid_quals(mapping):
    return set(mapping.values())

initialise_logger()

PATH_TO_FILES = settings.path_to_pdfs_to_extract
INTERNAL_MAPPING = get_internal_mapping(
    settings.path_to_mapping_file, settings.qualification_mapping_sheet_name
)

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

    ALL_FILES, APPLICANT_IDS = order_pdfs_to_target_id_input(ALL_FILES, APPLICANT_IDS)

    total_num_files = len(ALL_FILES)
    print("Extracting tables for {} students".format(total_num_files))

    # Initialise subject names dictionaries
    math_names = {}
    phys_names = {}
    fm_names = {}
    math_totals = {}
    phys_totals = {}
    fm_totals = {}

    for qual in all_valid_quals(INTERNAL_MAPPING):
        math_names[qual] = {}
        phys_names[qual] = {}
        fm_names[qual] = {}
        math_totals[qual] = 0
        phys_totals[qual] = 0
        fm_totals[qual] = 0

    pbar = tqdm(total=total_num_files, desc="Table Processing: ")
    # Iterate over all files and applicant IDs
    for file, app_id in zip(ALL_FILES, APPLICANT_IDS):

        # Start on 2nd page as 1st doesn't contain impt info
        page_number = 2
        exit_loop = False

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

                    if header_counter == TARGET_TABLES[0]:
                        qual_key = 'Exam'
                    elif header_counter == TARGET_TABLES[1]:
                        qual_key = 'Exam'
                    elif header_counter == TARGET_TABLES[2]:
                        qual_key = 'Exam Level'

                    for row in table.index:

                        if is_qual_valid(table[qual_key][row]):
                            qual = get_valid_qualification(table[qual_key][row])

                            subject = escape_backslash_r(str(table['Subject'][row]))

                            if subject in math_names[qual].keys():
                                math_names[qual][subject] += 1
                                math_totals[qual] += 1

                            elif subject in phys_names[qual].keys():
                                phys_names[qual][subject] += 1
                                phys_totals[qual] += 1

                            elif subject in fm_names[qual].keys():
                                fm_names[qual][subject] += 1
                                fm_totals[qual] += 1

                            else:
                                if 'math' in subject.lower() and 'further' not in subject.lower():
                                    math_names[qual][subject] = 1
                                    math_totals[qual] += 1

                                elif 'further' in subject.lower() and 'math' in subject.lower():
                                    fm_names[qual][subject] = 1
                                    fm_totals[qual] += 1

                                elif 'physics' in subject.lower():
                                    phys_names[qual][subject] = 1
                                    phys_totals[qual] += 1

                        elif is_detailed_entry(table, row):

                            if not isna(table[qual_key][row - 1]):
                                qual = table[qual_key][row - 1]
                            else:
                                qual = None

                            if is_qual_valid(qual):
                                qual = get_valid_qualification(qual)

                                if qual in ib_permutations():

                                    all_module_details = table["Body"][row]
                                    individual_modules = all_module_details.split("Title:")[1:]

                                    for module in individual_modules:

                                        subject = module.split("Date:")[0].split('Value:')[0].split('Predicted Grade:')[0].split("Grade:")[0].strip()

                                        if subject in math_names[qual].keys():
                                            math_names[qual][subject] += 1
                                            math_totals[qual] += 1

                                        elif subject in phys_names[qual].keys():
                                            phys_names[qual][subject] += 1
                                            phys_totals[qual] += 1

                                        elif subject in fm_names[qual].keys():
                                            fm_names[qual][subject] += 1
                                            fm_totals[qual] += 1

                                        else:
                                            if 'math' in subject.lower() and 'further' not in subject.lower():
                                                math_names[qual][subject] = 1
                                                math_totals[qual] += 1

                                            elif 'further' in subject.lower() and 'math' in subject.lower():
                                                fm_names[qual][subject] = 1
                                                fm_totals[qual] += 1

                                            elif 'physics' in subject.lower():
                                                phys_names[qual][subject] = 1
                                                phys_totals[qual] += 1

                elif EXIT_STRING in table_headers:
                    # Exit condition
                    exit_loop = True

            if exit_loop:
                break

            # Go to next page in document
            page_number += 1

        # Go to next student
        pbar.update()

    pbar.close()

    print('\r\r\n\nSubject names for MATHEMATICS found in this batch, per valid qualification, with number of occurances:')
    for qual in math_names:
        print('\r\nQualification: {}'.format(qual))
        for name, val in math_names[qual].items():
            print("{:<36}: {:.1%}%".format(name, (val/math_totals[qual])))

    print('\r\n\r\nSubject names for PHYSICS found in this batch, per valid qualification, with number of occurances:')
    for qual in phys_names:
        print('\r\nQualification: {}'.format(qual))
        for name, val in phys_names[qual].items():
            print("{:<36}: {:.1%}%".format(name, (val/phys_totals[qual])))

    print('\r\n\r\nSubject names for FURTHER MATHEMATICS found in this batch, per valid qualification, with number of occurances:')
    for qual in fm_names:
        print('\r\nQualification: {}'.format(qual))
        for name in fm_names[qual]:
            print("{:<40}: {:.1%}%".format(name, (val/fm_totals[qual])))

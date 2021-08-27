import os
import logging
import shutil

from collections import Counter
from pandas import read_excel
import numpy as np

import tabula
import settings


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def initialise_logger():
    if not os.path.exists(settings.output_path):
        raise NotADirectoryError("Output Directory NOT Found")

    if os.path.exists(settings.path_to_log):
        os.remove(settings.path_to_log)

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename=settings.path_to_log, datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    logging.info("Start")


def get_internal_mapping(path_to_file, sheet_name):
    if not path_to_file.endswith(".xlsx"):
        logging.error("Mapping file not in xlsx format")
        raise InputError(not path_to_file.endswith(".xlsx"),
                         "Input file must be in xlsx format")

    input_file = path_to_file

    from openpyxl import load_workbook

    wb = load_workbook(filename=input_file, read_only=True)
    ws = wb[sheet_name]

    # Maps values in columns after 2nd to value in 1st column
    output_dict = dict()

    for row in ws.rows:
        val = None
        for cell in row:
            if val is None:
                # Value in first column is the desired string
                val = cell.value
            else:
                # Other values is what we have
                output_dict[cell.value] = val

    logging.info("Mapping file loaded")

    return output_dict


def is_file_valid(file):
    if file.endswith(".pdf") and "unicode" in file:
        return True
    else:
        logging.info(f"{file} is not valid. Unicode or .pdf not in file name")
        return False


def is_abs_path(input_path):
    if not os.path.isabs(input_path):
        logging.error("Absolut path to file not provided")
        raise InputError(os.path.isabs(input_path),
                         "Path provided is not absolute")

    return True


def check_output_dirs_exist():
    if not os.path.exists(settings.output_path):
        raise NotADirectoryError("Output folder does not exists")

    if not os.path.exists(settings.path_to_pdf_pool):
        raise NotADirectoryError("PDF pool does not exists")

    marker_names = [key for key in settings.allocation_details.keys()]

    for name in marker_names:
        folder_name = name + str(settings.batch_number)
        marker_path = os.path.join(settings.output_path, folder_name)
        if not os.path.exists(marker_path):
            raise NotADirectoryError(f"{folder_name} Folder does not exists")


def check_ids_correspond(ids_from_pdf_folder):
    data_from_sheet = read_excel(
        settings.path_to_target_file, engine="openpyxl", header=None)
    ids_from_excel = data_from_sheet.values.flatten().tolist()

    # Enforce same type - both Integers
    ids_from_pdf_folder = [int(item) for item in ids_from_pdf_folder]
    ids_from_excel = [int(item) for item in ids_from_excel]

    # Convert to set to allow for testing intersection
    ids_from_pdf_folder = set(ids_from_pdf_folder)
    ids_from_excel = set(ids_from_excel)

    intersection = ids_from_excel & ids_from_pdf_folder

    # Intersection lap is empty => No overlap
    if not intersection:
        logging.error(
            f"Mismatch in IDs."
            f"IDs in {settings.path_to_pdfs_to_extract} folder don't "
            f"match IDs in {settings.target_ucas_id_file} file")
        raise InputError(not intersection,
                         "IDs from PDF folder does not match IDs to extract in Excel file")

    # Difference between set and intersection
    not_in_excel = (ids_from_pdf_folder - intersection)
    not_in_folder = (ids_from_excel - intersection)
    # A set is not empty => something is missing
    # Both empty => no issues
    if not_in_excel or not_in_folder:
        logging.error(
            f"Overlap in IDs between Excel file and folder of PDFs not 100% match")

        # Convert to list to iterate over
        not_in_folder = list(not_in_folder)
        not_in_excel = list(not_in_excel)
        for item in not_in_folder:
            logging.error(f"{item} ID not in folder but in Excel file")
        for item in not_in_excel:
            logging.error(f"{item} ID not in Excel file but in folder")

        raise InputError(not not_in_excel or not not_in_folder,
                         f"Overlap in IDs between Excel file and folder of PDFs not 100% match")

    return ids_from_excel

def order_pdfs_to_target_id_input(all_pdf_paths, ids_from_all_pdfs):

    # Perform check to see if IDs from PDFs and target IDs correspond
    target_ids = check_ids_correspond(ids_from_all_pdfs)
    # Convert to numpy array to get argwhere to work 
    target_ids = np.asarray(list(target_ids))

    if type(ids_from_all_pdfs) is not list:
        ids_from_all_pdfs = list(ids_from_all_pdfs)

    # Enforced type being integer for comparison
    ids_from_all_pdfs = [int(item) for item in ids_from_all_pdfs]

    # Location of ID from pdfs in target ids list 
    id_locs = [np.argwhere(target_ids == current_id).item() for current_id in ids_from_all_pdfs]

    # Sort list based on id_locs, then extract the paths from it
    sorted_pdf_paths = [path for _, path in sorted(zip(id_locs, all_pdf_paths), key=lambda pair: pair[0])]

    target_ids = [str(item) for item in target_ids.tolist()]

    return sorted_pdf_paths, target_ids


def copy_file(path_to_file, extracted_students_instance, id):
    marker_name, numbering = extracted_students_instance.student_to_marker_mapping[id]
    original_filename = os.path.basename(path_to_file)

    new_filename = str(numbering) + "_" + original_filename
    path_to_new_dir = os.path.join(
        settings.output_path, marker_name, new_filename)

    shutil.copy(path_to_file, path_to_new_dir)


def copy_pdfs_to_pool(all_pdf_paths):
    output_path = settings.path_to_pdf_pool
    for file in all_pdf_paths:
        shutil.copy(file, output_path)


def get_files_and_ids(abs_path):

    # Test if path is absolute
    is_abs_path(abs_path)

    logging.info("Assembling list of files to analyse...")

    # Remove duplicates in files
    # BUT doesn't address repeated IDs
    lst_of_paths = list(set([os.path.join(abs_path, file) for file in os.listdir(
        abs_path) if is_file_valid(file)]))

    # Extract IDs from file names
    lst_of_ids = [file.split("_")[3] for file in lst_of_paths]

    num_files = len(lst_of_paths)
    logging.info(f"Total of {num_files} files")
    print(f"Total of {num_files} files in {settings.path_to_pdfs_to_extract}")

    # If all are unique, then no issues
    if len(lst_of_ids) == len(set(lst_of_ids)):
        logging.info("No duplicate files")
        print("No duplicate files")
        return lst_of_paths, lst_of_ids

    # If there are repetitions, remove it from the lsit of IDs and paths
    counter = 1
    num_repetitions = 0
    for unique_id in lst_of_ids[1:]:
        if unique_id in lst_of_ids[:counter]:
            logging.info(
                f"Duplicate file present for {unique_id}, file {lst_of_paths[counter]} removed")
            lst_of_ids.pop(counter)
            lst_of_paths.pop(counter)
            num_repetitions += 1
        else:
            counter += 1

    logging.info(f"Total of {num_repetitions} repeated files removed")
    print(f"Total of {num_repetitions} repeated files excluded")
    print("Check log for details")

    return lst_of_paths, lst_of_ids


def check_broken_table(current_page_number, filename, current_table):
    '''
        Determines if a table continues onto the next page
        If it does, return a the data in a form that can be appended to the original table
    '''

    # Extract tables from next page
    tables = tabula.read_pdf(filename, pages=str(
        current_page_number + 1), lattice=True, guess=True, pandas_options={"header": 0},)

    if not tables:
        return None

    # Table at the top of the page
    top_table = tables[0]
    top_table_header = top_table.columns

    current_table_header = current_table.columns
    current_table_length = len(current_table_header)

    if top_table.empty:
        table_length = len(top_table_header)
        if table_length == current_table_length:
            return top_table_header.to_series()
        elif detail_string() in top_table_header:
            return move_data_out_of_header(top_table, current_table_header, table_length)
        else:
            return None

    elif len(top_table_header) == current_table_length:
        return move_data_out_of_header(top_table, current_table_header, current_table_length)
    else:
        return None


def move_data_out_of_header(top_table, cur_table_header, table_length):

    from pandas import DataFrame as pdDF

    # Moves header into next row
    top_table = top_table.reset_index().T.reset_index().T

    # But, I have a new cloumn, so delete
    del top_table[0]

    # Create a new data frame instead of renaming columns as that creates issues
    # Only select table headers that are relevant for table at top of the page
    return pdDF(top_table.values, columns=cur_table_header[:table_length])


def fix_broken_table(current_page_number, current_table, filename):

    continued_values = check_broken_table(
        current_page_number, filename, current_table)

    if continued_values is not None:
        # add new row to end of DataFrame
        # current_table.loc[len(current_table.index)] = continued_values
        updated_table = current_table.append(
            continued_values, ignore_index=True, sort=False)

        # print(updated_table)
        return updated_table
    else:
        return current_table


def escape_backslash_r(input_string):
    if input_string is not None:
        return input_string.encode('unicode-escape').decode().replace("\\r", " ").strip()


def get_exit_string():
    return 'Type of school, college or training centre:'


def raw_table_headers():
    acheived_headers = ['Date', 'Body', 'Exam',
                        'Subject', 'Grade', 'Result', 'Centre Number']
    predicted_headers = ['Date', 'Body', 'Exam', 'Subject',
                         'Grade', 'Result', 'Centre\rNumber', 'Predicted\rGrade']
    examresults_headers = ['Date', 'Body',
                           'Exam Level', 'Sitting', 'Subject', 'Grade']

    return (acheived_headers, predicted_headers, examresults_headers)


def desired_tables():

    acheived_headers, predicted_headers, examresults_headers = raw_table_headers()
    achieved_counter = Counter(acheived_headers)
    predicted_counter = Counter(predicted_headers)
    examresults_counter = Counter(examresults_headers)

    return (achieved_counter, predicted_counter, examresults_counter)


def completed_qualification_valid_exams():
    return {"GCE Advanced\rLevel",
            "Cambridge Pre-\rU Certificate\r(Principal\rSub",
            "IB Total points",
            "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
            "Pearson\rEdexcel\rInternational\rAdvanced\rLevel",
            "Singapore-\rIntegrated\rProgramme-\rCambridge\rGCE\rAdvanced\rLevel",
            "SQA Advanced\rHighers",
            "SQA\rAdvanced\rHighers",
            "Spain-Titulo\rde Bachiller",
            "USA-Advanced\rPlacement Test",
            "USA-\rAdvanced\rPlacement\rTest",
            "International\rBaccalaureate\rDiploma",
            "Matura-\rPoland",
            "France-\rBaccalaureat",
            "France-\rBaccalaureat",
            "France\r-Baccalaureat",
            "France-\rOption\rInternationale\rdu\rBaccalaureat",
            "France -\rBaccalaureat\rGeneral (from\r2021)",
            "France\r-Baccalaureat",
            "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)",
            "All India Senior School Certificate (CBSE)",
            }


def exam_results_valid_exams():
    return {
        "Reformed A Level\rEngland",
        "SQA Advanced\rHighers",
        "Pre-U Certificate",
        "GCE A Level (H2)",
        "GCE A Level (H1)",
        "Cambridge\rInternational A\rLevel",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)",
    }


def predicted_qualification_valid_exams():
    return {
        "GCE\rAdvanced\rLevel",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Pearson\rEdexcel\rInternational\rAdvanced\rLevel",
        "Singapore-\rIntegrated\rProgramme-\rCambridge\rGCE\rAdvanced\rLevel",
        "SQA Advanced\rHighers",
        "SQA\rAdvanced\rHighers",
        "France -\rBaccalaureat\rGeneral (from\r2021)",
        "France\r-Baccalaureat",
        "International\rBaccalaureate\rDiploma",
        "Spain-Titulo\rde Bachiller",
        "Matura-\rPoland",
        "Romania-\rDiploma de\rBacalaureat",
        "India-Indian\rSchool\rCertificate\r(ISC)",
        "ISC",
        "ILC",
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)",
    }


def valid_exams():
    output_set = set()
    output_set = output_set.union(predicted_qualification_valid_exams())
    output_set = output_set.union(exam_results_valid_exams())
    output_set = output_set.union(completed_qualification_valid_exams())
    return output_set


def qualifications_with_overall_score():
    return {
        "France - Baccalaureat General (from 2021)",
        "France -Baccalaureat",
        "International Baccalaureate Diploma",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
        "Spain-Titulo de Bachiller",
        "Romania- Diploma de Bacalaureat",
        "India-Indian School Certificate (ISC)",
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip",
        "All India Senior School Certificate (CBSE)",
        "France- Option Internationale du Baccalaureat (OIB)",
        "New Matura- Poland",
        "Matura- Poland",
        "Italy-Diploma di Esame di Stato",
        "Diploma de Ensino Secundario- Portugal",
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)",
        "Zeugnis der Allgemeine Hochschulreif e",
        "Abitur",
    }


def ib_permutations():
    return {
        "International Baccalaureate Diploma",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
    }


def detail_string():
    return "Module Details/Unit Grades"


def math_mapping():
    return {"GCE Advanced Level": {"Mathematics", "Mathematics (MEI)", "Mathematics A"},
            "Reformed A Level": {"Mathematics"},
            "Reformed A Level England": {"Mathematics"},
            "Cambridge International A Level": {"Mathematics"},
            "Cambridge Pre-U Certificate (Principal Subject)": {"Mathematics (principal subject)"},
            "Pre-U Certificate": {"Mathematics"},
            "SQA Advanced Highers": {"Mathematics C847", "Mathematics"},
            "Pearson Edexcel International Advanced Level": {"Mathematics"},
            "ILC": {"Mathematics"},
            "USA-Advanced Placement Test": {"AP Calculus BC",
                                            "AP Calculus\rBC",
                                            "CALCULUS BC",
                                            },
            "USA- Advanced Placement Test": {"AP Calculus BC",
                                             "AP Calculus\rBC",
                                             "CALCULUS BC",
                                             },
            "IB": {"Math Analysis & Appr",
                   "Mathematics",
                   "Mathematics Analysis"},
            "Int. Baccalaureate": {"Math Analysis & Appr",
                                   "Mathematics",
                                   "Mathematics Analysis"},
            "International Baccalaureate Diploma": {"Math Analysis & Appr",
                                                    "Mathematics Analysis",
                                                    "Mathematics",
                                                    },
            "Matura- Poland": {"Mathematics - basic level",
                               "Mathematics - bilingual",
                               "Mathematics - extended level", },
            "New Matura- Poland": {
                "Mathematics Level: Basic",
                "Mathematics Level: Advanced",
    },
        "Romania- Diploma de Bacalaureat": {"Mathematics"},
        "France- Baccalaureat": {"Mathematics Specialism",
                                 "Expert Mathematics"},
        "France - Baccalaureat General (from 2021)": {"mathematics",
                                                      "Mathematics", },
        "France- Option Internationale du Baccalaureat (OIB)": {"Mathematics Major (Specialism)",
                                                                "Mathematics Experts (Advanced)", },
        "France - Option Internationale du Baccalaureat (OIB) (from 2021)": {
                "Mathematics"
    },
        "Singapore- Integrated Programme- Cambridge GCE Advanced Level": {"Mathematics"},
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip": {
                "Mathematics",
    },
        "India-Indian School Certificate (ISC)": {"Mathematics"},
        "All India Senior School Certificate (CBSE)": {"Mathematics",
                                                       "MATHEMATICS", },
        "GCE A Level (H2)": {"Mathematics"},
        "Hong Kong Diploma of Secondary Education": {"Mathematics (compulsory component)",
                                                     "Mathematics"},
        "Spain-Titulo de Bachiller": {"Mathematics"},
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)": {"Mathematics advanced", "Mathematics advanced course", "Mathematics"},
        "Abitur": {"Mathematics advanced", "Mathematics advanced course", "Mathematics"},
        "Italy-Diploma di Esame di Stato": {"Mathematics"},
    }


def fm_mapping():
    return {"GCE Advanced Level": {"Further Mathematics (MEI)",
                                   "Further Mathematics"},
            "Reformed A Level": {"Further Mathematics"},
            "Reformed A Level England": {"Further Mathematics"},
            "Cambridge International A Level": {"Further Mathematics"},
            "Pearson Edexcel International Advanced Level": {"Further Mathematics"},
            "Cambridge Pre-U Certificate (Principal Subject)": {"Further Mathematics (principal subject)"},
            "Pre-U Certificate": {"Further Mathematics"},
            "SQA Advanced Highers": {
                "Mathematics of Mechanics C802",
                "Mathematics of Mechanics"
    },
        "Singapore- Integrated Programme- Cambridge GCE Advanced Level": {"Further Mathematics"},
        "GCE A Level (H2)": {"Further Mathematics"},
        "Hong Kong Diploma of Secondary Education": {"Calculus & Statistics",
                                                     "Calculus & Algebra"},
    }


def physics_mapping():
    return {"GCE Advanced Level": {"Physics A", "Physics"},
            "Reformed A Level": {"Physics"},
            "Reformed A Level England": {"Physics"},
            "Pearson Edexcel International Advanced Level": {"Physics"},
            "Cambridge International A Level": {"Physics"},
            "Cambridge Pre-U Certificate (Principal Subject)": {"Physics (principal subject)"},
            "Pre-U Certificate": {"Physics"},
            "SQA Advanced Highers": {"Physics C857", "Physics"},
            "ILC": {"Physics"},
            "Pearson Edexcel International Advanced Level": {"Physics"},
            "IB": {"Physics"},
            "Int. Baccalaureate": {"Physics"},
            "International Baccalaureate Diploma": {"Physics"},
            "USA-Advanced Placement Test": {"AP Physics C: Electricity and Magnetism",
                                            "AP Physics C: Mechanics",
                                            "AP Physics 1",
                                            "AP Physics C ELECTRICITY AND MAGNETISM",
                                            "AP Physics C MECHANICS"
                                            },
            "USA- Advanced Placement Test": {"AP Physics C: Electricity and Magnetism",
                                             "AP Physics C: Mechanics",
                                             "AP Physics 1",
                                             "AP Physics C ELECTRICITY AND MAGNETISM",
                                             "AP Physics C MECHANICS"
                                             },
            "Matura- Poland": {"Physics",
                               "Physics - bilingual",
                               },
            "New Matura- Poland": {
                "Physics Level: Advanced",
    },
        "Romania- Diploma de Bacalaureat": {"Physics"},
        "France - Baccalaureat General (from 2021)": {"physics",
                                                      "Physics", },
        "France- Baccalaureat": {"Physics-Chemistry Specialism",
                                 "Expert Mathematics"},
        "France- Option Internationale du Baccalaureat (OIB)": {"Physics Chemistry Major (Specialism)",
                                                                "Physics and chemistry"
                                                                "Physics & chemistry",
                                                                "Physics & Chemistry"},
        "France - Option Internationale du Baccalaureat (OIB) (from 2021)": {
                "Physics & Chemistry",
                "Physics & chemistry",
                "Physics and chemistry"
    },
        "India-Indian School Certificate (ISC)": {"Physics"},
        "All India Senior School Certificate (CBSE)": {"Physics",
                                                       "PHYSICS", },
        "Singapore- Integrated Programme- Cambridge GCE Advanced Level": {"Physics"},
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip": {
                "Physics"
    },
        "GCE A Level (H2)": {"Physics"},
        "Hong Kong Diploma of Secondary Education": {"Physics",
                                                     },
        "Spain-Titulo de Bachiller": {"Physics and Chemistry",
                                      "Physics"},
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)": {"Physics advanced course", "Physics", "Physics advanced"},
        "Abitur": {"Physics advanced course", "Physics", "Physics advanced"},
        "Italy-Diploma di Esame di Stato": {"Physics"},
    }

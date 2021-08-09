import os
import logging
import tabula

from collections import Counter
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
    print(f"Total of {num_repetitions} repeated files removed")
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
    return set(["GCE Advanced\rLevel",
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
                ])


def exam_results_valid_exams():
    return set([
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
    ])


def predicted_qualification_valid_exams():
    return set([
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
    ])


def valid_exams():
    output_set = set()
    output_set = output_set.union(predicted_qualification_valid_exams())
    output_set = output_set.union(exam_results_valid_exams())
    output_set = output_set.union(completed_qualification_valid_exams())
    return output_set


def qualifications_with_overall_score():
    return set([
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
    ])


def ib_permutations():
    return set([
        "International Baccalaureate Diploma",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
    ])


def detail_string():
    return "Module Details/Unit Grades"


def math_mapping():
    return {"GCE Advanced Level": set(["Mathematics", "Mathematics (MEI)", "Mathematics A"]),
            "Reformed A Level": set(["Mathematics"]),
            "Reformed A Level England": set(["Mathematics"]),
            "Cambridge International A Level": set(["Mathematics"]),
            "Cambridge Pre-U Certificate (Principal Subject)": set(["Mathematics (principal subject)"]),
            "Pre-U Certificate": set(["Mathematics"]),
            "SQA Advanced Highers": set(["Mathematics C847", "Mathematics"]),
            "Pearson Edexcel International Advanced Level": set(["Mathematics"]),
            "ILC": set(["Mathematics"]),
            "USA-Advanced Placement Test": set(["AP Calculus BC",
                                                "AP Calculus\rBC",
                                                "CALCULUS BC",
                                                ]),
            "USA- Advanced Placement Test": set(["AP Calculus BC",
                                                 "AP Calculus\rBC",
                                                 "CALCULUS BC",
                                                 ]),
            "IB": set(["Math Analysis & Appr",
                       "Mathematics Analysis"]),
            "Int. Baccalaureate": set(["Math Analysis & Appr",
                                       "Mathematics Analysis"]),
            "International Baccalaureate Diploma": set(["Math Analysis & Appr",
                                                        "Mathematics Analysis",
                                                        "Mathematics",
                                                        ]),
            "Matura- Poland": set(["Mathematics - basic level",
                                   "Mathematics - bilingual",
                                   "Mathematics - extended level", ]),
            "New Matura- Poland": set([
                "Mathematics Level: Basic",
                "Mathematics Level: Advanced",
            ]),
            "Romania- Diploma de Bacalaureat": set(["Mathematics"]),
            "France- Baccalaureat": set(["Mathematics Specialism",
                                         "Expert Mathematics"]),
            "France - Baccalaureat General (from 2021)": set(["mathematics",
                                                              "Mathematics", ]),
            "France- Option Internationale du Baccalaureat (OIB)": set(["Mathematics Major (Specialism)",
                                                                        "Mathematics Experts (Advanced)", ]),
            "France - Option Internationale du Baccalaureat (OIB) (from 2021)": set([
                "Mathematics"
            ]),
            "Singapore- Integrated Programme- Cambridge GCE Advanced Level": set(["Mathematics"]),
            "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip": set([
                "Mathematics",
            ]),
            "India-Indian School Certificate (ISC)": set(["Mathematics"]),
            "All India Senior School Certificate (CBSE)": set(["Mathematics",
                                                               "MATHEMATICS", ]),
            "GCE A Level (H2)": set(["Mathematics"]),
            "Hong Kong Diploma of Secondary Education": set(["Mathematics (compulsory component)",
                                                             "Mathematics"]),
            "Spain-Titulo de Bachiller": set(["Mathematics"]),
            "Zeugnis der Allgemeine Hochschulreif e (Abitur)": set(["Mathematics advanced", "Mathematics advanced course", "Mathematics"]),
            "Abitur": set(["Mathematics advanced", "Mathematics advanced course", "Mathematics"]),
            "Italy-Diploma di Esame di Stato": set(["Mathematics"]),
            }


def fm_mapping():
    return {"GCE Advanced Level": set(["Further Mathematics (MEI)",
                                       "Further Mathematics"]),
            "Reformed A Level": set(["Further Mathematics"]),
            "Reformed A Level England": set(["Further Mathematics"]),
            "Cambridge International A Level": set(["Further Mathematics"]),
            "Pearson Edexcel International Advanced Level": set(["Further Mathematics"]),
            "Cambridge Pre-U Certificate (Principal Subject)": set(["Further Mathematics (principal subject)"]),
            "Pre-U Certificate": set(["Further Mathematics"]),
            "SQA Advanced Highers": set([
                "Mathematics of Mechanics C802",
                "Mathematics of Mechanics"
            ]),
            "Singapore- Integrated Programme- Cambridge GCE Advanced Level": set(["Further Mathematics"]),
            "GCE A Level (H2)": set(["Further Mathematics"]),
            "Hong Kong Diploma of Secondary Education": set(["Calculus & Statistics",
                                                             "Calculus & Algebra"]),
            }


def physics_mapping():
    return {"GCE Advanced Level": set(["Physics A", "Physics"]),
            "Reformed A Level": set(["Physics"]),
            "Reformed A Level England": set(["Physics"]),
            "Pearson Edexcel International Advanced Level": set(["Physics"]),
            "Cambridge International A Level": set(["Physics"]),
            "Cambridge Pre-U Certificate (Principal Subject)": set(["Physics (principal subject)"]),
            "Pre-U Certificate": set(["Physics"]),
            "SQA Advanced Highers": set(["Physics C857", "Physics"]),
            "ILC": set(["Physics"]),
            "Pearson Edexcel International Advanced Level": set(["Physics"]),
            "IB": set(["Physics"]),
            "Int. Baccalaureate": set(["Physics"]),
            "International Baccalaureate Diploma": set(["Physics"]),
            "USA-Advanced Placement Test": set(["AP Physics C: Electricity and Magnetism",
                                                "AP Physics C: Mechanics",
                                                "AP Physics 1",
                                                "AP Physics C ELECTRICITY AND MAGNETISM",
                                                "AP Physics C MECHANICS"
                                                ]),
            "USA- Advanced Placement Test": set(["AP Physics C: Electricity and Magnetism",
                                                 "AP Physics C: Mechanics",
                                                 "AP Physics 1",
                                                 "AP Physics C ELECTRICITY AND MAGNETISM",
                                                 "AP Physics C MECHANICS"
                                                 ]),
            "Matura- Poland": set(["Physics",
                                   "Physics - bilingual",
                                   ]),
            "New Matura- Poland": set([
                "Physics Level: Advanced",
            ]),
            "Romania- Diploma de Bacalaureat": set(["Physics"]),
            "France - Baccalaureat General (from 2021)": set(["physics",
                                                              "Physics", ]),
            "France- Baccalaureat": set(["Physics-Chemistry Specialism",
                                         "Expert Mathematics"]),
            "France- Option Internationale du Baccalaureat (OIB)": set(["Physics Chemistry Major (Specialism)",
                                                                        "Physics and chemistry"
                                                                        "Physics & chemistry",
                                                                        "Physics & Chemistry"]),
            "France - Option Internationale du Baccalaureat (OIB) (from 2021)": set([
                "Physics & Chemistry",
                "Physics & chemistry",
                "Physics and chemistry"
            ]),
            "India-Indian School Certificate (ISC)": set(["Physics"]),
            "All India Senior School Certificate (CBSE)": set(["Physics",
                                                               "PHYSICS", ]),
            "Singapore- Integrated Programme- Cambridge GCE Advanced Level": set(["Physics"]),
            "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip": set([
                "Physics"
            ]),
            "GCE A Level (H2)": set(["Physics"]),
            "Hong Kong Diploma of Secondary Education": set(["Physics",
                                                             ]),
            "Spain-Titulo de Bachiller": set(["Physics and Chemistry",
                                              "Physics"]),
            "Zeugnis der Allgemeine Hochschulreif e (Abitur)": set(["Physics advanced course", "Physics", "Physics advanced"]),
            "Abitur": set(["Physics advanced course", "Physics", "Physics advanced"]),
            "Italy-Diploma di Esame di Stato": set(["Physics"]),
            }

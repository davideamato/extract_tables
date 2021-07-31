import os
import tabula

from collections import Counter


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def is_file_valid(file):
    return file.endswith(".pdf") and "unicode" in file


def is_abs_path(input_path):
    if not os.path.isabs(input_path):
        raise InputError(os.path.isabs(input_path),
                         "Path provided is not absolute")

    return True


def get_all_files_in_dir(abs_path):

    if is_abs_path(abs_path):
        return [os.path.join(abs_path, file) for file in os.listdir(abs_path) if is_file_valid(file)]


def get_applicant_ids(abs_path):

    if is_abs_path(abs_path):
        return [file.split("_")[2] for file in os.listdir(abs_path) if is_file_valid(file)]


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
    elif tables[0].empty:
        return tables[0].columns.to_series()
    elif len(tables[0].columns) == len(current_table.columns):
        # print(tables[0])
        # Moves header into next row
        tables[0] = tables[0].reset_index().T.reset_index().T
        # But, I have a new cloumn, so delete
        del tables[0][0]
        # Rename header so it can append easily
        tables[0].columns = current_table.columns
        # print(tables[0])
        return tables[0]
    else:
        return None


def fix_broken_table(current_page_number, current_table, filename):

    continued_values = check_broken_table(
        current_page_number, filename, current_table)

    if continued_values is not None:
        # add new row to end of DataFrame
        # current_table.loc[len(current_table.index)] = continued_values
        updated_table = current_table.append(
            continued_values, ignore_index=True)

        # print(updated_table)
        return updated_table
    else:
        return current_table


def raw_table_headers():
    acheived_headers = ['Date', 'Body', 'Exam',
                        'Subject', 'Grade', 'Result', 'Centre Number']
    predicted_headers = ['Date', 'Body', 'Exam', 'Subject',
                         'Grade', 'Result', 'Centre\rNumber', 'Predicted\rGrade']
    examresults_headers = ['Date', 'Body',
                           'Exam Level', 'Sitting', 'Subject', 'Grade']

    return (acheived_headers, predicted_headers, examresults_headers)


def escape_backslash_r(input_string):
    if input_string is not None:
        return input_string.encode('unicode-escape').decode().replace("\\r", " ")


def desired_tables():

    acheived_headers, predicted_headers, examresults_headers = raw_table_headers()
    achieved_counter = Counter(acheived_headers)
    predicted_counter = Counter(predicted_headers)
    examresults_counter = Counter(examresults_headers)

    return (achieved_counter, predicted_counter, examresults_counter)


def completed_qualification_valid_exams():
    return set(["GCE Advanced\rLevel",
            "Cambridge Pre-\rU Certificate\r(Principal\rSub",
            "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
            "Pearson\rEdexcel\rInternational\rAdvanced\rLevel",
            "Singapore-\rIntegrated\rProgramme-\rCambridge\rGCE\rAdvanced\rLevel"
            "SQA Advanced\rHighers",
            "SQA\rAdvanced\rHighers",
            "Spain-Titulo\rde Bachiller",
            "USA-Advanced\rPlacement Test",
            "International\rBaccalaureate\rDiploma",
            "Matura-\rPoland"
            "France-\rBaccalaureat",
            "France-\rOption\rInternationale\rdu\rBaccalaureat",
            "France -\rBaccalaureat\rGeneral (from\r2021)",
            "France\r-Baccalaureat",
            "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)"
    ])
    #  "GCE Advanced\rSubsidiary",
    #  "USA - SAT\r(redesigned\rfrom 2016)", "USA-SAT\rSubject" )


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
        "IB Total points"
        ])


def predicted_qualification_valid_exams():
    return set([
        "GCE\rAdvanced\rLevel",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Pearson\rEdexcel\rInternational\rAdvanced\rLevel",
        "Singapore-\rIntegrated\rProgramme-\rCambridge\rGCE\rAdvanced\rLevel"
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
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)"
        ])


def detail_string():
    return "Module Details/Unit Grades"


def math_mapping():
    return {"GCE Advanced Level": set(["Mathematics", "Mathematics (MEI)", "Mathematics A"]),
            "SQA Scottish Highers": set(["Mathematics C847", "Mathematics"]),
            "Pearson Edexcel International Advanced Level": set(["Mathematics"]),
            "ILC": set(["Mathematics"]),
            "USA-Advanced Placement Test": set(["AP Calculus BC",
                                            "AP Calculus\rBC"
                                            "CALCULUS BC"
                                            ]),
            # "IB": set(["Math Analysis & Appr"]),
            "Int. Baccalaureate": set(["Math Analysis & Appr"]),
            # "International Baccalaureate Diploma": set(["Math Analysis & Appr"]),
            "Cambridge International A Level": set(["Mathematics"]),
            "Singapore- Integrated Programme- Cambridge GCE Advanced Level": set(["Mathematics"]),
            "Cambridge Pre-U Certificate (Principal Subject)": set(["Mathematics (principal subject)"]),
            }


def fm_mapping():
    return {"GCE Advanced Level": set(["Further Mathematics (MEI)", "Further Mathematics"]),
            "Cambridge International A Level": set(["Further Mathematics"]),
            "Pearson Edexcel International Advanced Level": set(["Further Mathematics"]),
            "Singapore- Integrated Programme- Cambridge GCE Advanced Level": set(["Further Mathematics"]),
            "Cambridge Pre-U Certificate (Principal Subject)": set(["Further Mathematics (principal subject)"]),
            }


def physics_mapping():
    return {"GCE Advanced Level": set(["Physics A", "Physics"]),
            "SQA Scottish Highers": set(["Physics C857", "Physics"]),
            "Cambridge International A Level": set(["Physics"]),
            "Cambridge Pre-U Certificate (Principal Subject)": set(["Physics (principal subject)"]),
            "ILC": set(["Physics"]),
            "Pearson Edexcel International Advanced Level": set(["Physics"]),
            # "IB": set(["Physics"]),
            "Int. Baccalaureate": set(["Physics"]),
            # "International Baccalaureate\rDiploma": set(["Physics"]),
            "USA-Advanced Placement Test": set(["AP Physics C: Electricity and Magnetism",
                                            "AP Physics C: Mechanics",
                                            "AP Physics 1",
                                            "AP Physics C ELECTRICITY AND MAGNETISM",
                                            "AP Physics C MECHANICS"
                                            ]),
            "Singapore- Integrated Programme- Cambridge GCE Advanced Level": set(["Physics"]),
            }

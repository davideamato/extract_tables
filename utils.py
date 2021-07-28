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

import os
import tabula

from collections import Counter

def get_all_files_in_dir(abs_path):

    if not os.path.isabs(abs_path):
        raise InputError(os.path.isabs(abs_path), "Path provided is not absolute")

    return [os.path.join(abs_path, file) for file in os.listdir(abs_path) if file.endswith(".pdf")]

def check_broken_table(current_page_number, filename, current_table):

    tables = tabula.read_pdf(filename, pages=str(current_page_number + 1), lattice=True, guess=True, pandas_options={"header": 0},)

    print("{} {}".format(len(tables[0].columns), len(current_table.columns)))

    if tables[0].empty:
        return tables[0].columns.values
    elif len(tables[0].columns) == len(current_table.columns):
        tables[0].columns = current_table.columns
        return tables[0]
    else:
        return None


def fix_broken_table(current_page_number, current_table, filename):

    continued_values = check_broken_table(current_page_number, filename, current_table)

    if continued_values is not None:
        #add new row to end of DataFrame
        # current_table.loc[len(current_table.index)] = continued_values
        updated_table = current_table.append(continued_values, ignore_index=True)

        return updated_table
    else:
        return current_table

def desired_tables():
    acheived_headers = ['Date', 'Body', 'Exam', 'Subject', 'Grade', 'Result', 'Centre Number']
    achieved_counter = Counter(acheived_headers)
    predicted_headers = ['Date', 'Body', 'Exam', 'Subject', 'Grade', 'Result', 'Centre\rNumber', 'Predicted\rGrade']
    predicted_counter = Counter(predicted_headers)
    examresults_headers = ['Date', 'Body', 'Exam Level', 'Sitting', 'Subject', 'Grade']
    examresults_counter = Counter(examresults_headers)

    return (achieved_counter, predicted_counter, examresults_counter)
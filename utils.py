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

def get_all_files_in_dir(abs_path):

    if not os.path.isabs(abs_path):
        raise InputError(os.path.isabs(abs_path), "Path provided is not absolute")

    return [os.path.join(abs_path, file) for file in os.listdir(abs_path) if file.endswith(".pdf")]

def check_broken_table(current_page_number, filename):

    tables = tabula.read_pdf(filename, pages=str(current_page_number + 1), lattice=True, guess=True, pandas_options={"header": 0},)

    if tables[0].empty:
        return tables[0].columns.values
    else:
        return None


def fix_broken_table(current_page_number, current_table, filename):
    continued_values = check_broken_table(current_page_number, filename)
    if continued_values is not None:
        #add new row to end of DataFrame
        current_table.loc[len(current_table.index)] = continued_values
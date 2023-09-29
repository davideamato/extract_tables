#########################################
############## USER INPUTS ##############
#########################################
############## MAIN INPUTS ##############
#########################################

# IMPORTANT NOTE: IT IS ASSUMED THAT THE BATCH NUMBERS WILL KEEP INCREASING
# EVEN AFTER THE CYCLE CHANGES! THIS IS VITAL FOR THE REMAINING WORKFLOW!
# THE BATCH NUMBERS MUST BE UNIQUE!!!
batch_number = 1
cycle = 'Nov'

# Base directory where the files are located
base_directory = '../Shirin'
# Name of banner file
banner_name = 'Batch ' + str(batch_number) + '.xlsx'
# Keys are the initials of markers, values are the weighting of applications to be allocated
# to that person.
allocation_details = {
    "DA": 1,
    "PV": 1,
}

#########################################
############ AUXILIARY INPUTS ###########
#########################################

# Location of the PDF files
path_to_pdfs = 'PDFs from UCAS/' + 'Batch ' + str(batch_number)

# Location of the mapping file
path_to_mapping = ''
# Name of mapping file
mapping_name = 'mapping.xlsx'

# Path to banner file
path_to_banner = 'Excel from Banner'

# Path to database CSV
path_to_database = 'data'
# Name of database CSV
database_name = 'previously_extracted.csv'

# Path to output directory
output_path = 'output'


# _ is used as a delimeter to split the filename of the pdf
# This index is for which item in the list (from split) corresponds to the
# ID of an applicant
pdf_filename_split_delimeter = "_"
pdf_filename_split_index = 2

# Sheet name of the qualification mapping in mapping file
qualification_mapping_sheet_name = "Mapping"
maths_mapping_sheet_name = 'Maths'
physics_mapping_sheet_name = 'Physics'
further_maths_mapping_sheet_name = 'FM'

is_id_file_banner = True
is_banner_cumulative = True
# Column in banner file that contains IDs
which_column = "F"

database_headers = ["ID No.", "Batch No.", "Timestamp"]
database_header_id_num_index = 0
database_header_batch_index = 1
database_header_timestamp_index = 2

terminate_if_batch_num_repeated = True

#########################################
############# END OF INPUTS #############
#########################################

import os

def get_full_file_path(path, filename):
    """Combines path and filename to return full abs path as raw string"""
    return (
        os.path.abspath(os.path.join(path, filename)).encode("unicode-escape").decode()
    )


def get_full_path(path):
    """Combines path and filename to return full abs path as raw string"""
    return os.path.abspath(path).encode("unicode-escape").decode()


path_to_pdfs_to_extract = get_full_path(os.path.join(base_directory, path_to_pdfs))

path_to_mapping_file = get_full_file_path(os.path.join(base_directory, path_to_mapping), mapping_name)

path_to_target_file = get_full_file_path(os.path.join(base_directory, path_to_banner), banner_name)

assert (
    max(
        database_header_id_num_index,
        database_header_batch_index,
        database_header_timestamp_index,
    )
    < len(database_headers)
)

path_to_database_of_extracted_pdfs = get_full_file_path(os.path.join(base_directory, path_to_database), database_name)

output_path = get_full_path(os.path.join(base_directory, output_path))

path_to_pdf_pool = os.path.join(base_directory, output_path, "pool")
path_to_pdf_pool = get_full_path(path_to_pdf_pool)

if not os.path.exists(path_to_pdf_pool):
    os.makedirs(path_to_pdf_pool)

if not os.path.exists(path_to_database_of_extracted_pdfs):
    os.makedirs(os.path.join(base_directory, path_to_database))

output_filename = f"grades_{batch_number}.xlsx"

log_filename = f"execution_log_{batch_number}.log"
path_to_log = get_full_file_path(output_path, log_filename)
ids_in_folder_file = f"id_log_{batch_number}.txt"
path_to_folder_ids = get_full_file_path(output_path, ids_in_folder_file)

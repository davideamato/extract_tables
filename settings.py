'''
    Module for configuring the script
'''

import os

def get_full_file_path(path, filename):
    """Combines path and filename to return full abs path as raw string"""
    return (
        os.path.abspath(os.path.join(path, filename)).encode(
            "unicode-escape").decode()
    )


def get_full_path(path):
    """Combines path and filename to return full abs path as raw string"""
    return (
        os.path.abspath(path).encode("unicode-escape").decode()
    )

##############################################
############### INPUT RELATED ################ 
##############################################

path_to_pdfs_to_extract = os.path.join(".", "pdfs")
path_to_pdfs_to_extract = get_full_path(path_to_pdfs_to_extract)

qualification_mapping_filename = "mapping.xlsx"
qualification_mapping_sheet_name = 'Mapping'
path_to_mapping_file = path_to_pdfs_to_extract
path_to_mapping_file = get_full_file_path(path_to_mapping_file, qualification_mapping_filename)

target_ucas_id_file = "target_ids.xlsx"
path_to_target_file = path_to_pdfs_to_extract
path_to_target_file = get_full_file_path(path_to_target_file, target_ucas_id_file)

# IMPORTANT NOTE: IT IS ASSUMED THAT THE BATCH NUMBERS WILL KEEP INCREASING
# EVEN AFTER THE CYCLE CHANGES! THIS IS VITAL FOR THE REMAINING WORKFLOW!
# THE BATCH NUMBERS MUST BE UNIQUE!!!
batch_number = 1
cycle = "Nov"
allocation_details = {
    "AP": 1,
    "TM": 1, 
    "EN": 1,
}

##############################################
############### OUTPUT RELATED ############### 
##############################################

path_to_pdf_pool = os.path.join(".", "pool") 
path_to_pdf_pool = get_full_path(path_to_pdf_pool)

output_path = os.path.join("." ,"output")
output_path = get_full_path(output_path)

output_filename = "grades.xlsx"

log_filename = "execution_log.log"
path_to_log = get_full_file_path(output_path, log_filename)
ids_in_folder_file = "id_log.txt"
path_to_folder_ids = get_full_file_path(output_path, ids_in_folder_file)
'''
    Module for configuring the script
'''

from utils import get_full_file_path, get_full_path

##############################################
############### INPUT RELATED ################ 
##############################################

path_to_pdfs_to_extract = "/pdfs" 
path_to_pdfs_to_extract = get_full_path(path_to_pdfs_to_extract)

qualification_mapping_filename = "mapping.xlsx"
qualification_mapping_sheet_name = 'Mapping'
path_to_mapping_file = "/pdfs"
path_to_mapping_file = get_full_file_path(path_to_mapping_file, qualification_mapping_filename)

target_ucas_id_file = "target_ids.xlsx"
path_to_target_file = "/pdfs"
path_to_target_file = get_full_file_path(path_to_target_file, target_ucas_id_file)

batch_number = 1
allocation_details = {
    "AP": 1,
    "TM": 1, 
    "EN": 1,
}

##############################################
############### OUTPUT RELATED ############### 
##############################################

path_to_pdf_pool = "/pool"
path_to_pdf_pool = get_full_path(path_to_pdf_pool)

output_path = "/output"
output_path = get_full_path(output_path)

output_filename = "grades.xlsx"

log_filename = "execution_log.log"
path_to_log = get_full_file_path(output_path, log_filename)
ids_in_folder_file = "id_log.yaml"
path_to_folder_ids = get_full_file_path(output_path, ids_in_folder_file)
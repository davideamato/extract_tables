import os
import unittest

import settings
from utils import get_files_and_ids


class TestIDCorrespondence(unittest.TestCase):
    def banner_target_no_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_no_database_is_cumulative(self):
        # determine behaviour
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_is_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_not_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_is_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def id_only_target_succeeds(self):
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        path_to_files = os.path.join(".", "a")

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass


class TestFileIDCorrespondence(unittest.TestCase):
    def banner_target_no_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_no_database_is_cumulative(self):
        # determine behaviour
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_is_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_not_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def banner_target_with_database_is_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

    def id_only_target_succeeds(self):
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = True
        settings.path_to_database_of_extracted_pdfs = True
        pass

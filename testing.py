import os
import unittest

import settings
from utils import get_files_and_ids


class TestIDCorrespondence(unittest.TestCase):
    def banner_target_no_database_not_cumulative(self):
        # suceeds
        # Should have same behaviour as if banner is not target
        path_to_files = os.path.join(".", "test_no_database_not_cumulative")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = False

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_no_database_is_cumulative(self):
        # same behaviour as previous
        # no database means it doesn't matter whether or not it is cumulative
        path_to_files = os.path.join(".", "test_no_database_cumulative")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "test_with_database_not_cumulative")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_is_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "test_with_database_cumulative")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_not_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_is_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def id_only_target_succeeds(self):
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass


class TestFileIDCorrespondence(unittest.TestCase):
    def banner_target_no_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)

        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_no_database_is_cumulative(self):
        # determine behaviour
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_not_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_is_cumulative(self):
        # suceeds
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_not_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def banner_target_with_database_is_cumulative_fails(self):
        # failure situation
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

    def id_only_target_succeeds(self):
        path_to_files = os.path.join(".", "a")
        all_files, applicant_ids = get_files_and_ids(path_to_files)
        settings.is_id_file_banner = True
        settings.is_banner_cumulative = True

        settings.path_to_target_file = path_to_files
        settings.path_to_database_of_extracted_pdfs = path_to_files
        pass

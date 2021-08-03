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

    top_table = tables[0]
    top_table_header = top_table.columns

    if top_table.empty:
        table_length = len(top_table_header)
        if table_length == len(current_table.columns):
            return top_table_header.to_series()
        elif detail_string() in top_table_header:
            top_table = top_table.reset_index().T.reset_index().T
            del top_table[0]
            from pandas import DataFrame as pdDF
            # new_table = pdDF(top_table.values, columns = current_table.columns[:table_length])
            return pdDF(top_table.values, columns=current_table.columns[:table_length])
        else:
            return None

    elif len(top_table_header) == len(current_table.columns):
        # print(top_table)
        # Moves header into next row
        top_table = top_table.reset_index().T.reset_index().T
        # But, I have a new cloumn, so delete
        del top_table[0]
        # Rename header so it can append easily
        new_col_names = dict(zip(top_table_header, current_table.columns))
        top_table = top_table.rename(columns=new_col_names, inplace=True)
        # top_table_header = current_table.columns
        # print(top_table)
        return top_table
    else:
        return None


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
        return input_string.encode('unicode-escape').decode().replace("\\r", "").replace(" ", "").strip()


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
                "USA-\rAdvanced\rPlacement\rTest",
                "International\rBaccalaureate\rDiploma",
                "Matura-\rPoland"
                "France-\rBaccalaureat",
                "France\r-Baccalaureat",
                "France-\rOption\rInternationale\rdu\rBaccalaureat",
                "France -\rBaccalaureat\rGeneral (from\r2021)",
                "France\r-Baccalaureat",
                "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)"
                "All India\rSenior School\rCertificate\r(CBSE)"
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
        "IB Total points"
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)"
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


def valid_exams():
    return predicted_qualification_valid_exams() | exam_results_valid_exams() | completed_qualification_valid_exams()


def qualifications_with_overall_score():
    return set([
        "France - Baccalaureat General (from 2021)".replace(" ", ""),
        "France -Baccalaureat".replace(" ", ""),
        "International Baccalaureate Diploma".replace(" ", ""),
        "IB",
        "IB Standard Level".replace(" ", ""),
        "Int. Baccalaureate".replace(" ", ""),
        "IB Total points".replace(" ", ""),
        "Spain-Titulo de Bachiller".replace(" ", ""),
        "Romania- Diploma de Bacalaureat".replace(" ", ""),
        "India-Indian School Certificate (ISC)".replace(" ", ""),
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip".replace(
            " ", ""),
        "All India Senior School Certificate (CBSE)".replace(" ", ""),
        "France- Option Internationale du Baccalaureat (OIB)".replace(" ", ""),
        "New Matura- Poland".replace(" ", ""),
        "Matura- Poland".replace(" ", ""),
        "Italy-Diploma di Esame di Stato".replace(" ", ""),
        "Diploma de Ensino Secundario- Portugal".replace(" ", ""),
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)".replace(" ", ""),
        "Zeugnis der Allgemeine Hochschulreif e".replace(" ", ""),
        "Abitur".replace(" ", ""),
    ])


def ib_permutations():
    return set([
        "International Baccalaureate Diploma".replace(" ", ""),
        "IB".replace(" ", ""),
        "IB Standard Level".replace(" ", ""),
        "Int. Baccalaureate".replace(" ", ""),
        "IB Total points".replace(" ", ""),
    ])


def detail_string():
    return "Module Details/Unit Grades"


def math_mapping():
    return {"GCEAdvancedLevel": set(["Mathematics", "Mathematics(MEI)", "MathematicsA"]),
            "ReformedALevel": set(["Mathematics"]),
            "ReformedALevelEngland": set(["Mathematics"]),
            "CambridgeInternationalALevel": set(["Mathematics"]),
            "CambridgePre-UCertificate(PrincipalSubject)": set(["Mathematics(principalsubject)"]),
            "Pre-UCertificate": set(["Mathematics"]),
            "SQAScottishHighers": set(["MathematicsC847", "Mathematics"]),
            "PearsonEdexcelInternationalAdvancedLevel": set(["Mathematics"]),
            "ILC": set(["Mathematics"]),
            "USA-AdvancedPlacementTest": set(["APCalculusBC",
                                              "APCalculusBC"
                                              "CALCULUSBC"
                                              ]),
            "IB": set(["MathAnalysis&Appr",
                       "MathematicsAnalysis"]),
            "Int.Baccalaureate": set(["MathAnalysis&Appr",
                                      "MathematicsAnalysis"]),
            "InternationalBaccalaureateDiploma": set(["MathAnalysis&Appr",
                                                      "MathematicsAnalysis",
                                                      "Mathematics",
                                                      ]),
            "Matura-Poland": set(["Mathematics-basiclevel",
                                  "Mathematics-bilingual",
                                  "Mathematics-extendedlevel"]),
            "NewMatura-Poland": set([
                "MathematicsLevel: Basic",
                "MathematicsLevel: Advanced",
            ]),
            "Romania-DiplomadeBacalaureat": set(["Mathematics"]),
            "France-Baccalaureat": set(["MathematicsSpecialism",
                                        "ExpertMathematics"]),
            "France-BaccalaureatGeneral(from2021)": set(["mathematics",
                                                         "Mathematics", ]),
            "France-OptionInternationaleduBaccalaureat(OIB)": set(["MathematicsMajor(Specialism)",
                                                                   "MathematicsExperts(Advanced)"]),
            "France-OptionInternationaleduBaccalaureat(OIB)(from2021)": set([
                "Mathematics"
            ]),
            "Singapore-IntegratedProgramme-CambridgeGCEAdvancedLevel": set(["Mathematics"]),
            "Singapore-IntegratedProgramme-NatUniSingaporeHighSchofMaths&ScienceDip": set([
                "Mathematics"
            ]),
            "India-IndianSchoolCertificate(ISC)": set(["Mathematics"]),
            "AllIndiaSeniorSchoolCertificate(CBSE)": set(["Mathematics",
                                                          "MATHEMATICS", ]),
            "GCEALevel(H2)": set(["Mathematics"]),
            "HongKongDiplomaofSecondaryEducation": set(["Mathematics(compulsorycomponent)",
                                                        "Mathematics"]),
            "Spain-TitulodeBachiller": set(["Mathematics"]),
            "ZeugnisderAllgemeineHochschulreife(Abitur)": set(["Mathematicsadvanced", "Mathematicsadvancedcourse", "Mathematics"]),
            "Abitur": set(["Mathematicsadvanced", "Mathematicsadvancedcourse", "Mathematics"]),
            "Italy-DiplomadiEsamediStato": set(["Mathematics"]),
            }


def fm_mapping():
    return {"GCEAdvancedLevel": set(["FurtherMathematics(MEI)",
                                     "FurtherMathematics"]),
            "ReformedALevel": set(["FurtherMathematics"]),
            "ReformedALevelEngland": set(["Further Mathematics"]),
            "CambridgeInternationalALevel": set(["FurtherMathematics"]),
            "PearsonEdexcelInternationalAdvancedLevel": set(["FurtherMathematics"]),
            "CambridgePre-UCertificate(PrincipalSubject)": set(["FurtherMathematics(principalsubject)"]),
            "Pre-UCertificate": set(["FurtherMathematics"]),
            "SQAScottishHighers": set([
                "MathematicsofMechanics C802",
                "MathematicsofMechanics"
            ]),
            "Singapore-IntegratedProgramme-CambridgeGCEAdvancedLevel": set(["FurtherMathematics"]),
            "GCEALevel(H2)": set(["FurtherMathematics"]),
            "HongKongDiplomaofSecondaryEducation": set(["Calculus&Statistics",
                                                        "Calculus&Algebra"]),
            }


def physics_mapping():
    return {"GCEAdvancedLevel": set(["PhysicsA", "Physics"]),
            "ReformedALevel": set(["Physics"]),
            "ReformedALevelEngland": set(["Physics"]),
            # "Pearson Edexcel International Advanced Level": set(["Physics"]),
            "CambridgeInternationalALevel": set(["Physics"]),
            "CambridgePre-UCertificate(PrincipalSubject)": set(["Physics(principalsubject)"]),
            "Pre-UCertificate": set(["Physics"]),
            "SQAScottishHighers": set(["PhysicsC857", "Physics"]),
            "ILC": set(["Physics"]),
            "PearsonEdexcelInternationalAdvancedLevel": set(["Physics"]),
            "IB": set(["Physics"]),
            "Int.Baccalaureate": set(["Physics"]),
            "InternationalBaccalaureateDiploma": set(["Physics"]),
            "USA-AdvancedPlacementTest": set(["APPhysicsC:ElectricityandMagnetism",
                                              "APPhysicsC:Mechanics",
                                              "APPhysics1",
                                              "APPhysicsCELECTRICITYANDMAGNETISM",
                                              "APPhysicsCMECHANICS"
                                              ]),
            "Matura-Poland": set(["Physics",
                                  "Physics-bilingual",
                                  ]),
            "New Matura-Poland": set([
                "PhysicsLevel:Advanced",
            ]),
            "Romania-DiplomadeBacalaureat": set(["Physics"]),
            "France-BaccalaureatGeneral(from2021)": set(["physics",
                                                         "Physics", ]),
            "France-Baccalaureat": set(["Physics-ChemistrySpecialism", ]),
            "France-OptionInternationaleduBaccalaureat(OIB)": set(["PhysicsChemistryMajor(Specialism)",
                                                                   "Physics&Chemistry"]),
            "France-OptionInternationaleduBaccalaureat(OIB)(from2021)": set([
                "Physics&Chemistry"
            ]),
            "India-IndianSchoolCertificate(ISC)": set(["Physics"]),
            "AllIndiaSeniorSchoolCertificate(CBSE)": set(["Physics",
                                                               "PHYSICS", ]),
            "Singapore-IntegratedProgramme-CambridgeGCEAdvancedLevel": set(["Physics"]),
            "Singapore-IntegratedProgramme-NatUniSingaporeHighSchofMaths&ScienceDip": set([
                "Physics"
            ]),
            "GCEALevel(H2)": set(["Physics"]),
            "HongKongDiplomaofSecondaryEducation": set(["Physics",
                                                             ]),
            "Spain-TitulodeBachiller": set(["PhysicsandChemistry",
                                              "Physics"]),
            "ZeugnisderAllgemeineHochschulreife(Abitur)": set(["Physicsadvancedcourse", "Physics", "Physicsadvanced"]),
            "Abitur": set(["Physicsadvancedcourse", "Physics", "Physicsadvanced"]),
            "Italy-DiplomadiEsamediStato": set(["Physics"]),
            }

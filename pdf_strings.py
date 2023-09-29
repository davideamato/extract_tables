from collections import Counter


def get_exit_string():
    return "Type of school, college or training centre:"


def raw_table_headers():
    acheived_headers = [
        "Date",
        "Body",
        "Exam",
        "Subject",
        "Grade",
        "Result",
        "Centre Number",
    ]
    predicted_headers = [
        "Date",
        "Body",
        "Exam",
        "Subject",
        "Grade",
        "Result",
        "Centre\rNumber",
        "Predicted\rGrade",
    ]
    examresults_headers = ["Date", "Body", "Exam Level", "Sitting", "Subject", "Grade"]

    return (acheived_headers, predicted_headers, examresults_headers)


def desired_tables():

    acheived_headers, predicted_headers, examresults_headers = raw_table_headers()
    achieved_counter = Counter(acheived_headers)
    predicted_counter = Counter(predicted_headers)
    examresults_counter = Counter(examresults_headers)

    return (achieved_counter, predicted_counter, examresults_counter)


def valid_exams(mapping):
    return set(mapping.keys())


def qualifications_with_overall_score():
    return {
        "France: French Baccalaureate Scientific stream",
        "World: IB - International Baccalaureate (IB) Diploma",
        "Spain: Bachillerato",
        "Romania: Diploma de Bacalaureat",
        "India: CISCE - ISC - Council for the Indian School Certificate Examination",
        "Singapore: National University of Singapore Diploma",
        "India: CBSE - AISSE - Central Board of Secondary Education Board",
        "France: OIB - Option Internationale du Baccalauréat",
        "Poland: Świadectwo dojrzalosci (Matura)",
        "Italy: Diploma di Esame di Stato",
        "Portugal: Diploma Nível Secundário de Educação",
        "Germany: Abiturprufung",
    }


def ib_permutations():
    return {
        "International Baccalaureate Diploma",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
        "World: IB - International Baccalaureate (IB) Diploma"
    }


def detail_string():
    return "Module Details/Unit Grades"

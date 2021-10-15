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


def completed_qualification_valid_exams():
    return {
        "GCE Advanced\rLevel",
        "Cambridge Pre-\rU Certificate\r(Principal\rSub",
        "IB Total points",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Pearson\rEdexcel\rInternational\rAdvanced\rLevel",
        "Singapore-\rIntegrated\rProgramme-\rCambridge\rGCE\rAdvanced\rLevel",
        "SQA Advanced\rHighers",
        "SQA\rAdvanced\rHighers",
        "Spain-Titulo\rde Bachiller",
        "USA-Advanced\rPlacement Test",
        "USA-\rAdvanced\rPlacement\rTest",
        "International\rBaccalaureate\rDiploma",
        "Matura-\rPoland",
        "France-\rBaccalaureat",
        "France-\rBaccalaureat",
        "France\r-Baccalaureat",
        "France-\rOption\rInternationale\rdu\rBaccalaureat",
        "France -\rBaccalaureat\rGeneral (from\r2021)",
        "France\r-Baccalaureat",
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)",
        "All India Senior School Certificate (CBSE)",
    }


def exam_results_valid_exams():
    return {
        "Reformed A Level\rEngland",
        "SQA Advanced\rHighers",
        "Pre-U Certificate",
        "GCE A Level (H2)",
        "GCE A Level (H1)",
        "Cambridge\rInternational A\rLevel",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)",
    }


def predicted_qualification_valid_exams():
    return {
        "GCE\rAdvanced\rLevel",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Cambridge\rPre-U\rCertificate\r(Principal\rSubject)",
        "Pearson\rEdexcel\rInternational\rAdvanced\rLevel",
        "Singapore-\rIntegrated\rProgramme-\rCambridge\rGCE\rAdvanced\rLevel",
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
        "Irish leaving\rcertificate -\rHigher level\r(first awarded\r2017)",
    }


def valid_exams():
    output_set = set()
    output_set = output_set.union(predicted_qualification_valid_exams())
    output_set = output_set.union(exam_results_valid_exams())
    output_set = output_set.union(completed_qualification_valid_exams())
    return output_set


def qualifications_with_overall_score():
    return {
        "France - Baccalaureat General (from 2021)",
        "France -Baccalaureat",
        "International Baccalaureate Diploma",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
        "Spain-Titulo de Bachiller",
        "Romania- Diploma de Bacalaureat",
        "India-Indian School Certificate (ISC)",
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip",
        "All India Senior School Certificate (CBSE)",
        "France- Option Internationale du Baccalaureat (OIB)",
        "New Matura- Poland",
        "Matura- Poland",
        "Italy-Diploma di Esame di Stato",
        "Diploma de Ensino Secundario- Portugal",
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)",
        "Zeugnis der Allgemeine Hochschulreif e",
        "Abitur",
    }


def ib_permutations():
    return {
        "International Baccalaureate Diploma",
        "IB",
        "IB Standard Level",
        "Int. Baccalaureate",
        "IB Total points",
    }


def detail_string():
    return "Module Details/Unit Grades"


def math_mapping():
    return {
        "GCE Advanced Level": {"Mathematics", "Mathematics (MEI)", "Mathematics A"},
        "Reformed A Level": {"Mathematics"},
        "Reformed A Level England": {"Mathematics"},
        "Cambridge International A Level": {"Mathematics"},
        "Cambridge Pre-U Certificate (Principal Subject)": {
            "Mathematics (principal subject)"
        },
        "Pre-U Certificate": {"Mathematics"},
        "SQA Advanced Highers": {"Mathematics C847", "Mathematics"},
        "Pearson Edexcel International Advanced Level": {"Mathematics"},
        "ILC": {"Mathematics"},
        "USA-Advanced Placement Test": {
            "AP Calculus BC",
            "AP Calculus\rBC",
            "CALCULUS BC",
        },
        "USA- Advanced Placement Test": {
            "AP Calculus BC",
            "AP Calculus\rBC",
            "CALCULUS BC",
        },
        "IB": {"Math Analysis & Appr", "Mathematics", "Mathematics Analysis"},
        "Int. Baccalaureate": {
            "Math Analysis & Appr",
            "Mathematics",
            "Mathematics Analysis",
        },
        "International Baccalaureate Diploma": {
            "Math Analysis & Appr",
            "Mathematics Analysis",
            "Mathematics",
        },
        "Matura- Poland": {
            "Mathematics - basic level",
            "Mathematics - bilingual",
            "Mathematics - extended level",
        },
        "New Matura- Poland": {
            "Mathematics Level: Basic",
            "Mathematics Level: Advanced",
        },
        "Romania- Diploma de Bacalaureat": {"Mathematics"},
        "France- Baccalaureat": {"Mathematics Specialism", "Expert Mathematics"},
        "France - Baccalaureat General (from 2021)": {
            "mathematics",
            "Mathematics",
        },
        "France- Option Internationale du Baccalaureat (OIB)": {
            "Mathematics Major (Specialism)",
            "Mathematics Experts (Advanced)",
        },
        "France - Option Internationale du Baccalaureat (OIB) (from 2021)": {
            "Mathematics"
        },
        "Singapore- Integrated Programme- Cambridge GCE Advanced Level": {
            "Mathematics"
        },
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip": {
            "Mathematics",
        },
        "India-Indian School Certificate (ISC)": {"Mathematics"},
        "All India Senior School Certificate (CBSE)": {
            "Mathematics",
            "MATHEMATICS",
        },
        "GCE A Level (H2)": {"Mathematics"},
        "Hong Kong Diploma of Secondary Education": {
            "Mathematics (compulsory component)",
            "Mathematics",
        },
        "Spain-Titulo de Bachiller": {"Mathematics"},
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)": {
            "Mathematics advanced",
            "Mathematics advanced course",
            "Mathematics",
        },
        "Abitur": {
            "Mathematics advanced",
            "Mathematics advanced course",
            "Mathematics",
        },
        "Italy-Diploma di Esame di Stato": {"Mathematics"},
    }


def fm_mapping():
    return {
        "GCE Advanced Level": {"Further Mathematics (MEI)", "Further Mathematics"},
        "Reformed A Level": {"Further Mathematics"},
        "Reformed A Level England": {"Further Mathematics"},
        "Cambridge International A Level": {"Further Mathematics"},
        "Pearson Edexcel International Advanced Level": {"Further Mathematics"},
        "Cambridge Pre-U Certificate (Principal Subject)": {
            "Further Mathematics (principal subject)"
        },
        "Pre-U Certificate": {"Further Mathematics"},
        "SQA Advanced Highers": {
            "Mathematics of Mechanics C802",
            "Mathematics of Mechanics",
        },
        "Singapore- Integrated Programme- Cambridge GCE Advanced Level": {
            "Further Mathematics"
        },
        "GCE A Level (H2)": {"Further Mathematics"},
        "Hong Kong Diploma of Secondary Education": {
            "Calculus & Statistics",
            "Calculus & Algebra",
        },
    }


def physics_mapping():
    return {
        "GCE Advanced Level": {"Physics A", "Physics"},
        "Reformed A Level": {"Physics"},
        "Reformed A Level England": {"Physics"},
        "Cambridge International A Level": {"Physics"},
        "Cambridge Pre-U Certificate (Principal Subject)": {
            "Physics (principal subject)"
        },
        "Pre-U Certificate": {"Physics"},
        "SQA Advanced Highers": {"Physics C857", "Physics"},
        "ILC": {"Physics"},
        "Pearson Edexcel International Advanced Level": {"Physics"},
        "IB": {"Physics"},
        "Int. Baccalaureate": {"Physics"},
        "International Baccalaureate Diploma": {"Physics"},
        "USA-Advanced Placement Test": {
            "AP Physics C: Electricity and Magnetism",
            "AP Physics C: Mechanics",
            "AP Physics 1",
            "AP Physics C ELECTRICITY AND MAGNETISM",
            "AP Physics C MECHANICS",
        },
        "USA- Advanced Placement Test": {
            "AP Physics C: Electricity and Magnetism",
            "AP Physics C: Mechanics",
            "AP Physics 1",
            "AP Physics C ELECTRICITY AND MAGNETISM",
            "AP Physics C MECHANICS",
        },
        "Matura- Poland": {
            "Physics",
            "Physics - bilingual",
        },
        "New Matura- Poland": {
            "Physics Level: Advanced",
        },
        "Romania- Diploma de Bacalaureat": {"Physics"},
        "France - Baccalaureat General (from 2021)": {
            "physics",
            "Physics",
        },
        "France- Baccalaureat": {"Physics-Chemistry Specialism", "Expert Mathematics"},
        "France- Option Internationale du Baccalaureat (OIB)": {
            "Physics Chemistry Major (Specialism)",
            "Physics and chemistry",
            "Physics & chemistry",
            "Physics & Chemistry",
        },
        "France - Option Internationale du Baccalaureat (OIB) (from 2021)": {
            "Physics & Chemistry",
            "Physics & chemistry",
            "Physics and chemistry",
        },
        "India-Indian School Certificate (ISC)": {"Physics"},
        "All India Senior School Certificate (CBSE)": {
            "Physics",
            "PHYSICS",
        },
        "Singapore- Integrated Programme- Cambridge GCE Advanced Level": {"Physics"},
        "Singapore- Integrated Programme- Nat Uni Singapore High Sch of Maths & Science Dip": {
            "Physics"
        },
        "GCE A Level (H2)": {"Physics"},
        "Hong Kong Diploma of Secondary Education": {
            "Physics",
        },
        "Spain-Titulo de Bachiller": {"Physics and Chemistry", "Physics"},
        "Zeugnis der Allgemeine Hochschulreif e (Abitur)": {
            "Physics advanced course",
            "Physics",
            "Physics advanced",
        },
        "Abitur": {"Physics advanced course", "Physics", "Physics advanced"},
        "Italy-Diploma di Esame di Stato": {"Physics"},
    }

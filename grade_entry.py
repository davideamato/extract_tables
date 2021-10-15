from utils import escape_backslash_r


class GradeEntry:
    """
    Class to store the grades
    """

    def __init__(
        self, qualification, subject, grade, is_predicted, year, is_exam_result
    ):
        if isinstance(grade, str):
            self.grade = escape_backslash_r(grade)
        else:
            self.grade = grade
        self.subject = escape_backslash_r(subject)
        self.qualification = escape_backslash_r(qualification)
        self.is_predicted = is_predicted
        self.is_exam_result = is_exam_result
        self.year = year

        self.grade_info = [self.grade, self.subject]

    def __repr__(self):
        return r"Qualification: {} Subject: {} Grade: {} Year: {} Predicted: {} Exam Result: {}".format(
            self.qualification,
            self.subject,
            self.grade,
            self.year,
            self.is_predicted,
            self.is_exam_result,
        )

    def __str__(self):
        return r"Qualification: {} Subject: {} Grade: {} Year: {} Predicted: {} Exam Result: {}".format(
            self.qualification,
            self.subject,
            self.grade,
            self.year,
            self.is_predicted,
            self.is_exam_result,
        )

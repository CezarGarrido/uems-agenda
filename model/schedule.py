class Schedule:
    def __init__(self, course_id, year, grade, weekday, professor_discipline_id, time, time_start, time_end, created_at):
        self.id = ""
        self.course_id = course_id
        self.year = year
        self.grade = grade
        self.weekday = weekday
        self.professor_discipline_id = professor_discipline_id
        self.time = time
        self.time_start = time_start
        self.time_end = time_end
        self.created_at = created_at

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "year": self.year,
            "grade": self.grade,
            "weekday": self.weekday,
            "professor_discipline_id": self.professor_discipline_id,
            "time": self.time,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "created_at": self.created_at,
        }

    def to_json(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "year": self.year,
            "grade": self.grade,
            "weekday": self.weekday,
            "professor_discipline_id": self.professor_discipline_id,
            "time": self.time,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "created_at": self.created_at,
        }
class Professor:
    def __init__(self, name, created_at):
        self.id = ""
        self.name = name
        self.disciplines = []
        self.created_at = created_at

    def to_dict(self):
        return {
            "name": self.name,
            "created_at": self.created_at,
        }

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "disciplines": self.disciplines,
            "created_at": self.created_at,
        }


class ProfessorDiscipline:
    def __init__(self, course_id, discipline_id, professor_id, created_at):
        self.id = ""
        self.course_id = course_id
        self.discipline_id = discipline_id
        self.professor_id = professor_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "discipline_id": self.discipline_id,
            "professor_id": self.professor_id,
            "created_at": self.created_at,
        }

    def to_json(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "discipline_id": self.discipline_id,
            "professor_id": self.professor_id,
            "created_at": self.created_at,
        }

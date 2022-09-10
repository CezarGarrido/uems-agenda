class Discipline:
    def __init__(self, course_id, initials, description, created_at):
        self.id = ""
        self.course_id = course_id
        self.initials = initials
        self.description = description
        self.created_at = created_at

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "initials": self.initials,
            "description": self.description,
            "created_at": self.created_at,
        }

    def to_json(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "initials": self.initials,
            "description": self.description,
            "created_at": self.created_at,
        }

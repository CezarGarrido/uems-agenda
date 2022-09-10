
class Course:
    def __init__(self, name, created_at) -> None:
        self.id = ""
        self.name = name
        self.created_at = created_at

    def to_dict(self):
        return {
            "name": self.name,
            "created_at": self.created_at
        }

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }

from pymongo import MongoClient
from enum import Enum
from datetime import datetime

# uri de conexão com o mongo
uri = "mongodb://admin:admin@localhost:27017"

# Nome do banco
db_name = "agenda"

# Abre uma conexão com o Mongo
class Course:
    def __init__(self, name) -> None:
        self.name = name
    def to_dict(self):
        return {
            "name": self.name,
        }

class Professor:
       def __init__(self,name, created_at):
         self.name = name
         self.created_at = created_at

       def to_dict(self):
           return {
                "name": self.name,
                "created_at": self.created_at,
            }

class Discipline:
    def __init__(self, initials, description, created_at):
        self.initials = initials
        self.description = description
        self.created_at = created_at

    def to_dict(self):
        return {
            "initials": self.initials,
            "description": self.description,
            "created_at": self.created_at,
        }

class ProfessorDiscipline:
    def __init__(self, discipline_id, professor_id, created_at):
        self.discipline_id = discipline_id
        self.professor_id = professor_id
        self.created_at = created_at
    def to_dict(self):
        return {
            "discipline_id": self.discipline_id,
            "professor_id": self.professor_id,
            "created_at": self.created_at,
        }

class WeekDay(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

class Schedule:
    def __init__(self, course_id, year, grade, weekday, professor_discipline_id, time, time_start, time_end, created_at):
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

class Agenda:
    def __init__(self, db) -> None:
        self.db = db
        self.repo_schedules = db["schedules"]
        self.repo_professor = db["professors"]
        self.repo_professor_disc = db["professor_disciplines"]
        self.repo_course = db["courses"]
        self.repo_discipline = db["disciplines"]

    def get_courses(self):
        print("Buscando todos os cursos...")
        courses = self.repo_course.find()
        print("id                       nome")
        for course in courses:
            print(course["_id"], course["name"])

    def create_course(self):
        name = ""
        while(name == ""):
            name = input("Informe o nome do curso: ")
            if name == "":
               print("Nome é obrigatório") 
        course = Course(name)
        count = self.repo_course.count_documents(course.to_dict())
        if count > 0:
            print("Um curso com o esse nome já existe.")
        else:
            res = self.repo_course.insert_one(course.to_dict())
            if res.inserted_id:
                print("Curso inserido com sucesso: ", res.inserted_id)

    def create_professor(self):
        name = ""
        while(name == ""):
            name = input("Informe o nome do professor: ")
            if name == "":
               print("Nome é obrigatório") 
        professor = Professor(name, datetime.now())

        count = self.repo_professor.count_documents({"name": name})
        if count > 0:
            print("Um professor com o esse nome já existe.")
        else:
            res = self.repo_professor.insert_one(professor.to_dict())
            if res.inserted_id:
                print("Professor inserido com sucesso: ", res.inserted_id)

    def create_discipline(self):
        name = ""
        initials = ""
        while(name == "" or initials == ""):
            name = input("Informe o nome da disciplina: ")
            initials = input("Informe as Sigla da disciplina: ")
            if name == "":
               print("Nome é obrigatório")
            if initials == "":
                print("Sigla é obrigatório")

        discipline = Discipline(initials, name, datetime.now())

        count = self.repo_discipline.count_documents({"initials": initials, "name": name})
        if count > 0:
            print("Uma disciplina com o esse nome já existe.")
        else:
            res = self.repo_discipline.insert_one(discipline.to_dict())
            if res.inserted_id:
                print("Disciplina inserida com sucesso: ", res.inserted_id)

    def create_professor_discipline(self):
        print("Selecione um Professor: ")
        professors = self.repo_professor.find()
        p_map_ids = {}
        for i, professor in enumerate(professors):
            p_map_ids[i] = professor["_id"] 
            print(f"{i} para {professor['name']}")

        index = int(input(""))
        professor_id = p_map_ids.get(index)
        d_map_ids = {}
        for i, professor in enumerate(professors):
            d_map_ids[i] = professor["_id"] 
            print(f"{i} para {professor['name']}")

        index = int(input(""))
        disciplines_id = d_map_ids.get(index)

def main():

    print("Selecione um opção: ")

    print("1 - Adicionar Novo Curso")
    print("2 - Adicionar Novo Professor")
    print("3 - Adicionar Nova Disciplina")
    print("4 - Adicionar Nova Aula do Professor")
    print("5 - Adicionar Novo Horário")
    print("")
    print("6 - Listar Cursos")
    print("7 - Listar Professores")
    print("8 - Listar Disciplinas")
    print("9 - Listar Horários")
    print("")
    print("q - para sair")

    client = MongoClient(uri)
    db = client[db_name]
    agenda = Agenda(db)

    choice = ""
    while(choice != "q"):
        choice = input("")
        if choice == "1":
            agenda.create_course()
        if choice == "2":
            agenda.create_professor()
        if choice == "3":
            agenda.create_discipline()
        if choice == "4":
            agenda.create_professor_discipline()
        if choice == "6":
            agenda.get_courses()

if __name__ == "__main__":
    main()

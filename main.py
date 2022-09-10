from crypt import methods
from pymongo import MongoClient
from datetime import datetime
from flask import Flask, request, json, Response
from model.course import Course
from model.discipline import Discipline
from model.professor import Professor, ProfessorDiscipline
from model.schedule import Schedule

app = Flask(__name__)

uri = "mongodb://admin:admin@localhost:27017"

db_name = "agenda"

client = MongoClient(uri)

db = client[db_name]

collection_courses = db.collection["courses"]
collection_disciplines = db.collection["disciplines"]
collection_professors = db.collection["professors"]
collection_professors_disc = db.collection["professors_disciplines"]
collection_schedules = db.collection["schedules"]


def error(message):
    return {
        "message": message,
    }


@app.route("/courses", methods=["POST"])
def create_course():
    data = request.json
    count = collection_courses.count_documents({"name": data["name"]})
    if count > 0:
        return Response(response=json.dumps(error("Curso já cadastrado.")),
                        status=500,
                        mimetype="application/json")
    else:
        course = Course(data["name"], datetime.now())

        res = collection_courses.insert_one(course.to_dict())

        if res.inserted_id:
            course.id = str(res.inserted_id)
            return Response(response=json.dumps(course.to_json()),
                            status=201,
                            mimetype="application/json")


@app.route("/disciplines", methods=["POST"])
def create_discipline():
    data = request.json

    count = collection_disciplines.count_documents({
        "course_id": data["course_id"],
        "initials": data["initials"],
    })

    if count > 0:
        return Response(response=json.dumps(error("Disciplina já cadastrada para esse curso.")),
                        status=500,
                        mimetype="application/json")

    else:
        d = Discipline(data["course_id"], data["initials"],
                       data["description"], datetime.now())

        res = collection_disciplines.insert_one(d.to_dict())

        if res.inserted_id:
            d.id = str(res.inserted_id)
            return Response(response=json.dumps(d.to_json()),
                            status=201,
                            mimetype="application/json")


@app.route("/professors", methods=["POST"])
def create_professor():
    data = request.json

    count = collection_professors.count_documents({
        "name": data["name"],
    })

    if count > 0:
        return Response(response=json.dumps(error("Professor já cadastrado.")),
                        status=500,
                        mimetype="application/json")
    else:
        professor = Professor(data["name"], datetime.now())

        res = collection_professors.insert_one(professor.to_dict())

        if res.inserted_id:
            professor.id = str(res.inserted_id)
            return Response(response=json.dumps(professor.to_json()),
                            status=201,
                            mimetype="application/json")


@app.route("/professor/disciplines", methods=["POST"])
def create_professor_discipline():
    data = request.json

    count = collection_professors_disc.count_documents({
        "course_id": data["course_id"],
        "professor_id": data["professor_id"],
        "discipline_id": data["discipline_id"],
    })

    if count > 0:
        return Response(response=json.dumps(error("Disciplina já cadastrada.")),
                        status=500,
                        mimetype="application/json")
    else:
        professor_disc = ProfessorDiscipline(
            data["course_id"], data["discipline_id"], data["professor_id"], datetime.now())

        res = collection_professors_disc.insert_one(professor_disc.to_dict())

        if res.inserted_id:
            professor_disc.id = str(res.inserted_id)
            return Response(response=json.dumps(professor_disc.to_json()),
                            status=201,
                            mimetype="application/json")


@app.route("/schedules", methods=["POST"])
def create_schedules():
    data = request.json

    count = collection_schedules.count_documents({
        "course_id": data["course_id"],
        "year": data["year"],
        "grade": data["grade"],
        "weekday": data["weekday"],
        "professor_discipline_id": data["professor_discipline_id"],
        "time": data["time"],
        "time_start": data["time_start"],
        "time_end": data["time_end"]
    })

    if count > 0:
        return Response(response=json.dumps(error("Horário já cadastrado.")),
                        status=500,
                        mimetype='application/json')
    else:
        sched = Schedule(data["course_id"],
                         data["year"],
                         data["grade"],
                         data["weekday"],
                         data["professor_discipline_id"],
                         data["time"],
                         data["time_start"],
                         data["time_end"],
                         datetime.now(),)

        res = collection_schedules.insert_one(sched.to_dict())

        if res.inserted_id:
            sched.id = str(res.inserted_id)
            return Response(response=json.dumps(sched.to_json()),
                            status=201,
                            mimetype="application/json")


if __name__ == "__main__":
    app.run()

from pymongo import MongoClient
from datetime import datetime
from flask import Flask, request, json, Response
from model.course import Course
from model.discipline import Discipline
from model.professor import Professor, ProfessorDiscipline
from model.schedule import Schedule
from bson.objectid import ObjectId
import redis

#redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Exemplo com usuario e senha
# uri = "mongodb://admin:admin@localhost:27017"

uri = "localhost"
db_name = "agenda"

client = MongoClient(uri, 27017)

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

@app.route("/courses", methods=["PUT"])
def upadate_course():
    data = request.json
    #verifica se existe o nome
    count = collection_courses.count_documents({"name": data["name"]})
    if count > 0:
        #verifica se existe o novo nome
        count = collection_courses.count_documents({"name": data["new_name"]})
        if count > 0:
            return Response(response=json.dumps(error("Curso " + data["new_name"] + " já cadastrado!")),
                            mimetype="application/json")
        else:
            collection_courses.update_one({"name": data["name"]}, {"$set": {"name": data["new_name"]}})
            return Response(response=json.dumps("Curso " + data["name"] + " alterado para " + data["new_name"]),
                            status=500,
                            mimetype="application/json")               
    else:               
        return Response(response=json.dumps(error("Curso não existe!")),
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


@app.route("/disciplines", methods=["PUT"])
def atualize_discipline():
    data = request.json

    if (not re.search(r'[a-f\d]{24}', data["id"])):
        return Response(response=json.dumps(error("Id invalido.")),
                                status=400 ,
                                mimetype="application/json")

    _id = ObjectId(data["id"])
    id_exist = collection_disciplines.count_documents({"_id": _id})
    data_allready_exist = collection_disciplines.count_documents({"$or": [{"initials": data["initials"]},
                                                {"description": data["description"]}] })
    
    if not id_exist:
       return Response(response=json.dumps(error("Disciplina não cadastrada.")),
                                status=404 ,
                                mimetype="application/json")
    elif data_allready_exist:
        return Response(response=json.dumps(error("Inicial ou nome de disciplina já existem.")),
                                status=400 ,
                                mimetype="application/json")

    else:        
        newvalues = { "$set": { 'initials': data["initials"], "description": data["description"] } }
        collection_disciplines.update_one({"_id":_id}, newvalues)          
        return Response(response=json.dumps(newvalues),
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

@app.route("/professors", methods=["PUT"])
def atualzie_professor():
    data = request.json

    _id = ObjectId(data["id"])
    id_exist = collection_professors.count_documents({"_id": _id})
    data_allready_exist = collection_professors.count_documents({"name": data["name"]})

    if not id_exist:
       return Response(response=json.dumps(error("Professor não existe!")),
                                status=404 ,
                                mimetype="application/json")
    elif data_allready_exist:#precisa?
        return Response(response=json.dumps(error("Nome já cadastrado.")),
                                status=400 ,
                                mimetype="application/json")

    else:
        newvalue = { "$set": { 'name': data["name"]} }
        collection_professors.update_one({"_id":_id}, newvalue)
        return Response(response=json.dumps(newvalue),
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

@app.route("/professor/disciplines", methods=["DELETE"])
def delete_professor_discipline():
    data = request.json

    count = collection_professors_disc.count_documents({
        "course_id": data["course_id"],
        "professor_id": data["professor_id"],
        "discipline_id": data["discipline_id"],
    })

    if count:
        deleted = collection_professors_disc.delete_one({
            #"course_id": data["course_id"], # Precisa?
            "professor_id": data["professor_id"],
            "discipline_id": data["discipline_id"],
        })
        return Response(response=json.dumps(data),
                            status=201,
                            mimetype="application/json")
    else:
        return Response(response=json.dumps(error("Professor ou disciplina invalidos")),
                            status=400,
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


@app.route("/schedules", methods=["DELETE"])
def delete_schedules():
    data = request.json
    _id = ObjectId(data["id"])
    id_exist = collection_schedules.count_documents({"_id": _id})


    if id_exist:
        deleted = collection_schedules.find_one({
            "_id": _id
        })
        deleted = collection_schedules.delete_one({
            "_id": _id
        })

        return Response(response=json.dumps(deleted),
                            status=201,
                            mimetype="application/json")
    else:
        return Response(response=json.dumps(error("Horario invalido")),
                            status=400,
                            mimetype="application/json")


@app.route("/schedules", methods=["PUT"])
def atualize_schedules():
    data = request.json

    _id = ObjectId(data["id"])
    id_exist = collection_schedules.count_documents({"_id": _id})

    if not id_exist:
       return Response(response=json.dumps(error("Horario não cadastrado.")),
                                status=404 ,
                                mimetype="application/json")
    else:
        sched = Schedule(data["course_id"],
                         data["year"],
                         data["grade"],
                         data.get("weekday"),
                         data["professor_discipline_id"],
                         data["time"],
                         data["time_start"],
                         data["time_end"],
                         ' ')
        new_values = sched.to_dict()

        new_values.pop('created_at') 

        new_values = { "$set":  new_values}
        collection_schedules.update_one({"_id":_id}, new_values)

        return Response(response=json.dumps(sched.to_json()),
                            status = 200,
                            mimetype="application/json")


@app.route("/schedules", methods=["GET"])
def show_schedules():
    _id_course = request.args.get('course_id')
    grade = request.args.get('grade')

    if r.exists(f'{_id_course}-{grade}'):
        print("Memoria armazenada no cache usada!")
        return Response(response=r.get(f'{_id_course}-{grade}'),
                        status=200,
                        mimetype="application/json")

    schedules = collection_schedules.find({"course_id": _id_course, "grade": grade})

    if not schedules:
        return Response(response=json.dumps(error("Horário não encontrado!")),
                                status=404,
                                mimetype="application/json")
    else:
        new_schedules = []
        for sched in schedules:
            schedule = {}

            schedule['professor_name'], schedule['discipline_initials'], schedule['discipline_description'] = find_discipline_professor(sched['professor_discipline_id'])

            schedule['course_name'] = collection_courses.find_one(ObjectId(_id_course))['name']

            schedule["year"] = sched["year"]
            schedule["grade"] = sched["grade"]
            schedule["weekday"] = sched["weekday"]
            schedule["time"] = sched["time"]
            schedule["time_start"] = sched["time_start"]
            schedule["time_end"] = sched["time_end"]

            new_schedules.append(schedule.copy()) 

        #para ser usado em pesquisas futuras
        r.set(f'{_id_course}-{grade}', json.dumps({"schedules_list": new_schedules}))

        return Response(response=json.dumps({"schedules_list": new_schedules}),
                        status=200,
                        mimetype="application/json")

#Funções Auxiliares 
def find_discipline_professor(id):
    _id = ObjectId(id)
    ids = collection_professors_disc.find_one(_id)

    p_id = ObjectId(ids['professor_id'])
    professor = collection_professors.find_one(p_id)
    del professor['_id']

    d_id = ObjectId(ids['discipline_id'])
    discipline = collection_disciplines.find_one(d_id)
    discipline_initials = discipline['initials']
    discipline_description = discipline['description']

    return (professor, discipline_initials, discipline_description)


if __name__ == "__main__":
    app.run(debug=True)

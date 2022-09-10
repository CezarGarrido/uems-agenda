from datetime import datetime
from model.course import Course
from model.discipline import Discipline


def load():
    si = Course("Sistemas de Informação", datetime.now())
    disciplines = [
        Discipline(si.id, "ASS", "Administração e Segurança de Sistemas", datetime.now()),
        Discipline(si.id, "TECII", "Tópicos Especias em Computação II", datetime.now()),
        Discipline(si.id, "IHC", "Interação Humano Computador", datetime.now()),
        Discipline(si.id, "RC", "Redes de Computadores", datetime.now()),
        Discipline(si.id, "TECI", "Tópicos Especias em Computação I", datetime.now()),
        Discipline(si.id, "TECI", "Tópicos Especias em Computação I", datetime.now()),
        Discipline(si.id, "IA", "Inteligência Artificial", datetime.now()),
        Discipline(si.id, "PD", "Programação Distríbuida", datetime.now()),
        Discipline(si.id, "SCII", "Seminários em Computação II", datetime.now())
    ]

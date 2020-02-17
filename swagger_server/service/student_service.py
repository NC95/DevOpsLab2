import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    # if not student.first_name:
    #     return 'unspecified first name', 405

    # if not student.last_name:
    #     return 'unspecified last name', 405

    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        print("POST: alreadt exists")
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    print("POST: last return statement.")
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        print("GET: student is None")
        return student

    studentDict = student
    student = Student.from_dict(student)
    if not subject:
        print("GET: subject is None")
        return student

    if subject not in studentDict["grades"]:
        print("GET: subject not in student dictionary")
        return 'wrong subject', 404

    print("GET: last return statement")
    return student


def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        print("DELETE: student is None")
        return 'not existing user', 404

    student_db.remove(doc_ids=[int(student_id)])
    print("DELETE: last return statement")
    return student_id

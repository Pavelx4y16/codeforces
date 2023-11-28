from flask import Blueprint, jsonify

import settings
from codeforces.src.database.data_base import DbClient


bp = Blueprint("api", __name__, url_prefix="/codeforces/api")
db_client = DbClient(url=settings.cities_path)


@bp.get("/students")
def get_students():
    return jsonify([
        student.dict() for student in db_client.students
    ])

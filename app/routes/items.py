
from flask import Blueprint

bp = Blueprint("items", __name__)

@bp.get("/")
def sample():
    return {"message":"sample entity here"}

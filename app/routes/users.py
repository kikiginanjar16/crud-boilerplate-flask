
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..schemas import user_schema, users_schema, ids_schema
from ..usecases import users as uc
from ..security import require_permissions

bp = Blueprint("users", __name__)

@bp.post("/")
@jwt_required()
@require_permissions("user.create")
def create_user():
    data=request.get_json() or {}
    obj=uc.create_user(data)
    return user_schema.dump(obj), 201

@bp.get("/")
@jwt_required()
@require_permissions("user.read")
def list_users():
    q=request.args.get("q"); sort=request.args.get("sort","id")
    page=int(request.args.get("page",1)); per_page=int(request.args.get("per_page",10))
    pg=uc.list_users(q=q, sort=sort, page=page, per_page=per_page)
    return jsonify(data=users_schema.dump(pg.items), page=pg.page, per_page=pg.per_page, total=pg.total, pages=pg.pages)

@bp.get("/<uuid:user_id>")
@jwt_required()
@require_permissions("user.read")
def get_user(user_id):
    obj=uc.get_user(user_id)
    if not obj: return {"error":"Not Found","message":"User not found"}, 404
    return user_schema.dump(obj)

@bp.patch("/<uuid:user_id>")
@jwt_required()
@require_permissions("user.update")
def update_user(user_id):
    obj=uc.update_user(user_id, request.get_json() or {})
    if not obj: return {"error":"Not Found","message":"User not found"}, 404
    return user_schema.dump(obj)

@bp.delete("/<uuid:user_id>")
@jwt_required()
@require_permissions("user.delete")
def delete_user(user_id):
    ok=uc.delete_user(user_id)
    if not ok: return {"error":"Not Found","message":"User not found"}, 404
    return {"message":"deleted"}

@bp.post("/<uuid:user_id>/roles")
@jwt_required()
@require_permissions("user.update")
def set_user_roles(user_id):
    data=ids_schema.load(request.get_json() or {})
    obj=uc.set_user_roles(user_id, data["ids"])
    if not obj: return {"error":"Not Found","message":"User not found"}, 404
    return user_schema.dump(obj)

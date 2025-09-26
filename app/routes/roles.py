
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..schemas import role_schema, roles_schema, ids_schema
from ..usecases import roles as uc
from ..security import require_permissions

bp = Blueprint("roles", __name__)

@bp.post("/")
@jwt_required()
@require_permissions("role.create")
def create_role():
    obj=uc.create_role(request.get_json() or {})
    return role_schema.dump(obj), 201

@bp.get("/")
@jwt_required()
@require_permissions("role.read")
def list_roles():
    q=request.args.get("q"); sort=request.args.get("sort","id")
    page=int(request.args.get("page",1)); per_page=int(request.args.get("per_page",10))
    pg=uc.list_roles(q=q, sort=sort, page=page, per_page=per_page)
    return jsonify(data=roles_schema.dump(pg.items), page=pg.page, per_page=pg.per_page, total=pg.total, pages=pg.pages)

@bp.get("/<uuid:role_id>")
@jwt_required()
@require_permissions("role.read")
def get_role(role_id):
    obj=uc.get_role(role_id)
    if not obj: return {"error":"Not Found","message":"Role not found"}, 404
    return role_schema.dump(obj)

@bp.patch("/<uuid:role_id>")
@jwt_required()
@require_permissions("role.update")
def update_role(role_id):
    obj=uc.update_role(role_id, request.get_json() or {})
    if not obj: return {"error":"Not Found","message":"Role not found"}, 404
    return role_schema.dump(obj)

@bp.delete("/<uuid:role_id>")
@jwt_required()
@require_permissions("role.delete")
def delete_role(role_id):
    ok=uc.delete_role(role_id)
    if not ok: return {"error":"Not Found","message":"Role not found"}, 404
    return {"message":"deleted"}

@bp.post("/<uuid:role_id>/permissions")
@jwt_required()
@require_permissions("role.update")
def set_role_permissions(role_id):
    data=ids_schema.load(request.get_json() or {})
    obj=uc.set_role_permissions(role_id, data["ids"])
    if not obj: return {"error":"Not Found","message":"Role not found"}, 404
    return role_schema.dump(obj)

@bp.post("/<uuid:role_id>/menus")
@jwt_required()
@require_permissions("role.update")
def set_role_menus(role_id):
    data=ids_schema.load(request.get_json() or {})
    obj=uc.set_role_menus(role_id, data["ids"])
    if not obj: return {"error":"Not Found","message":"Role not found"}, 404
    return role_schema.dump(obj)

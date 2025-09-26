
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..schemas import permission_schema, permissions_schema
from ..usecases import permissions as uc
from ..security import require_permissions

bp = Blueprint("permissions", __name__)

@bp.post("/")
@jwt_required()
@require_permissions("permission.create")
def create_permission():
    obj=uc.create_permission(request.get_json() or {})
    return permission_schema.dump(obj), 201

@bp.get("/")
@jwt_required()
@require_permissions("permission.read")
def list_permissions():
    q=request.args.get("q"); sort=request.args.get("sort","id")
    page=int(request.args.get("page",1)); per_page=int(request.args.get("per_page",10))
    pg=uc.list_permissions(q=q, sort=sort, page=page, per_page=per_page)
    return jsonify(data=permissions_schema.dump(pg.items), page=pg.page, per_page=pg.per_page, total=pg.total, pages=pg.pages)

@bp.get("/<uuid:permission_id>")
@jwt_required()
@require_permissions("permission.read")
def get_permission(permission_id):
    obj=uc.get_permission(permission_id)
    if not obj: return {"error":"Not Found","message":"Permission not found"}, 404
    return permission_schema.dump(obj)

@bp.patch("/<uuid:permission_id>")
@jwt_required()
@require_permissions("permission.update")
def update_permission(permission_id):
    obj=uc.update_permission(permission_id, request.get_json() or {})
    if not obj: return {"error":"Not Found","message":"Permission not found"}, 404
    return permission_schema.dump(obj)

@bp.delete("/<uuid:permission_id>")
@jwt_required()
@require_permissions("permission.delete")
def delete_permission(permission_id):
    ok=uc.delete_permission(permission_id)
    if not ok: return {"error":"Not Found","message":"Permission not found"}, 404
    return {"message":"deleted"}

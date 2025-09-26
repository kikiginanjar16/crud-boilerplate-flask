
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..schemas import menu_schema, menus_schema
from ..usecases import menus as uc
from ..security import require_permissions

bp = Blueprint("menus", __name__)

@bp.post("/")
@jwt_required()
@require_permissions("menu.create")
def create_menu():
    obj=uc.create_menu(request.get_json() or {})
    return menu_schema.dump(obj), 201

@bp.get("/")
@jwt_required()
@require_permissions("menu.read")
def list_menus():
    q=request.args.get("q"); sort=request.args.get("sort","sort_order,title")
    page=int(request.args.get("page",1)); per_page=int(request.args.get("per_page",50))
    pg=uc.list_menus(q=q, sort=sort, page=page, per_page=per_page)
    return jsonify(data=menus_schema.dump(pg.items), page=pg.page, per_page=pg.per_page, total=pg.total, pages=pg.pages)

@bp.get("/tree")
@jwt_required()
@require_permissions("menu.read")
def tree():
    roots = uc.roots()
    return menus_schema.dump(roots), 200

@bp.get("/<uuid:menu_id>")
@jwt_required()
@require_permissions("menu.read")
def get_menu(menu_id):
    obj=uc.get_menu(menu_id)
    if not obj: return {"error":"Not Found","message":"Menu not found"}, 404
    return menu_schema.dump(obj)

@bp.patch("/<uuid:menu_id>")
@jwt_required()
@require_permissions("menu.update")
def update_menu(menu_id):
    obj=uc.update_menu(menu_id, request.get_json() or {})
    if not obj: return {"error":"Not Found","message":"Menu not found"}, 404
    return menu_schema.dump(obj)

@bp.delete("/<uuid:menu_id>")
@jwt_required()
@require_permissions("menu.delete")
def delete_menu(menu_id):
    ok=uc.delete_menu(menu_id)
    if not ok: return {"error":"Not Found","message":"Menu not found"}, 404
    return {"message":"deleted"}

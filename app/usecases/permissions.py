
from ..extensions import db
from ..models import Permission
from .common import apply_filters_sort_pagination

def create_permission(data):
    p=Permission(code=data["code"], name=data["name"], description=data.get("description"))
    db.session.add(p); db.session.commit(); return p

def list_permissions(q=None, sort="id", page=1, per_page=10):
    return apply_filters_sort_pagination(Permission.query, Permission, q=q, search_cols=["code","name"],
                                         sort=sort, page=page, per_page=per_page)

def get_permission(perm_id): return db.session.get(Permission, perm_id)

def update_permission(perm_id, data):
    p=get_permission(perm_id)
    if not p: return None
    for k in ["code","name","description"]:
        if k in data: setattr(p,k,data[k])
    db.session.commit(); return p

def delete_permission(perm_id):
    p=get_permission(perm_id)
    if not p: return False
    db.session.delete(p); db.session.commit(); return True

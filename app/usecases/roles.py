
from ..extensions import db
from ..models import Role, Permission, Menu
from .common import apply_filters_sort_pagination

def create_role(data): 
    role=Role(name=data["name"], description=data.get("description"))
    db.session.add(role); db.session.commit(); return role

def list_roles(q=None, sort="id", page=1, per_page=10):
    return apply_filters_sort_pagination(Role.query, Role, q=q, search_cols=["name"],
                                         sort=sort, page=page, per_page=per_page)

def get_role(role_id): return db.session.get(Role, role_id)

def update_role(role_id, data):
    r=get_role(role_id); 
    if r is None: return None
    for k in ["name","description"]:
        if k in data: setattr(r,k,data[k])
    db.session.commit(); return r

def delete_role(role_id):
    r=get_role(role_id); 
    if not r: return False
    db.session.delete(r); db.session.commit(); return True

def set_role_permissions(role_id, perm_ids):
    r=get_role(role_id); 
    if not r: return None
    perms=Permission.query.filter(Permission.id.in_(perm_ids)).all()
    r.permissions=perms; db.session.commit(); return r

def set_role_menus(role_id, menu_ids):
    r=get_role(role_id); 
    if not r: return None
    menus=Menu.query.filter(Menu.id.in_(menu_ids)).all()
    r.menus=menus; db.session.commit(); return r


from ..extensions import db
from ..models import Menu
from .common import apply_filters_sort_pagination

def create_menu(data):
    m=Menu(title=data["title"], path=data.get("path"), icon=data.get("icon"),
           sort_order=data.get("sort_order",0), is_active=data.get("is_active",True),
           parent_id=data.get("parent_id"))
    db.session.add(m); db.session.commit(); return m

def list_menus(q=None, sort="sort_order,title", page=1, per_page=50):
    return apply_filters_sort_pagination(Menu.query, Menu, q=q, search_cols=["title","path","icon"],
                                         sort=sort, page=page, per_page=per_page)

def get_menu(menu_id): return db.session.get(Menu, menu_id)

def update_menu(menu_id, data):
    m=get_menu(menu_id)
    if not m: return None
    for k in ["title","path","icon","sort_order","is_active","parent_id"]:
        if k in data: setattr(m,k,data[k])
    db.session.commit(); return m

def delete_menu(menu_id):
    m=get_menu(menu_id)
    if not m: return False
    db.session.delete(m); db.session.commit(); return True

def roots():
    return Menu.query.filter_by(parent_id=None).order_by(Menu.sort_order.asc()).all()

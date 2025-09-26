
from ..extensions import db
from ..models import User, Role
from .common import apply_filters_sort_pagination

def create_user(data: dict) -> User:
    user = User(
        username=data["username"],
        email=data["email"],
        full_name=data.get("full_name"),
        avatar_url=data.get("avatar_url"),
    )
    user.set_password(data["password"])
    db.session.add(user); db.session.commit()
    return user

def list_users(q=None, sort="id", page=1, per_page=10):
    query = User.query
    pagination = apply_filters_sort_pagination(query, User, q=q, search_cols=["username","email","full_name"],
                                               sort=sort, page=page, per_page=per_page)
    return pagination

def get_user(user_id):
    return db.session.get(User, user_id)

def update_user(user_id, data: dict) -> User|None:
    user = get_user(user_id)
    if not user: return None
    for k in ["username","email","full_name","avatar_url","is_active"]:
        if k in data: setattr(user, k, data[k])
    if "password" in data and data["password"]:
        user.set_password(data["password"])
    db.session.commit(); return user

def delete_user(user_id) -> bool:
    user = get_user(user_id)
    if not user: return False
    db.session.delete(user); db.session.commit(); return True

def set_user_roles(user_id, role_ids):
    user = get_user(user_id)
    if not user: return None
    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    user.roles = roles
    db.session.commit(); return user

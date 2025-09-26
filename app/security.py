
from functools import wraps
from typing import Set
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from .extensions import db, jwt
from .models import User

def current_user():
    identity = get_jwt().get("sub")
    if identity is None: return None
    try:
        from uuid import UUID
        user_id = UUID(identity)
    except Exception:
        return None
    return db.session.get(User, user_id)

def _codes(user: User) -> Set[str]:
    codes=set()
    for r in user.roles:
        for p in r.permissions:
            codes.add(p.code)
    return codes

def require_permissions(*perm_codes: str):
    def deco(fn):
        @wraps(fn)
        def wrap(*a, **k):
            verify_jwt_in_request()
            user = current_user()
            if not user or not user.is_active:
                return {"error":"Forbidden","message":"Inactive or missing user"}, 403
            missing=[c for c in perm_codes if c not in _codes(user)]
            if missing:
                return {"error":"Forbidden","message":"Missing permissions: "+", ".join(missing)}, 403
            return fn(*a, **k)
        return wrap
    return deco

def register_security_hooks(app):
    @jwt.additional_claims_loader
    def add_claims(identity):
        try:
            from uuid import UUID
            user = db.session.get(User, UUID(identity))
            return {"username": user.username if user else None}
        except Exception:
            return {"username": None}

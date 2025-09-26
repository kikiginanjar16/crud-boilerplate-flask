
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User
from ..schemas import user_schema

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    """Register new user
    ---
    tags: [Auth]
    """
    data = request.get_json() or {}
    if not all(k in data for k in ["username","email","password"]):
        return {"error":"Bad Request","message":"username, email, password required"}, 400
    if User.query.filter((User.username==data["username"])|(User.email==data["email"])).first():
        return {"error":"Conflict","message":"Username or email already exists"}, 409
    user = User(username=data["username"], email=data["email"], full_name=data.get("full_name"))
    user.set_password(data["password"])
    db.session.add(user); db.session.commit()
    return user_schema.dump(user), 201

@bp.post("/login")
def login():
    """Login & issue JWT
    ---
    tags: [Auth]
    """
    data=request.get_json() or {}
    u = data.get("username"); p = data.get("password")
    if not u or not p: return {"error":"Bad Request","message":"username & password required"}, 400
    user = User.query.filter((User.username==u)|(User.email==u)).first()
    if not user or not user.check_password(p): return {"error":"Unauthorized","message":"Invalid credentials"}, 401
    if not user.is_active: return {"error":"Forbidden","message":"User inactive"}, 403
    identity=str(user.id)
    return {
        "access_token": create_access_token(identity=identity),
        "refresh_token": create_refresh_token(identity=identity),
        "user": user_schema.dump(user)
    }

@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Refresh access token
    ---
    tags: [Auth]
    security: [{ Bearer: [] }]
    """
    uid=get_jwt_identity()
    return {"access_token": create_access_token(identity=str(uid))}

@bp.get("/me")
@jwt_required()
def me():
    """Get current user
    ---
    tags: [Auth]
    security: [{ Bearer: [] }]
    """
    from uuid import UUID
    uid=get_jwt_identity()
    user=db.session.get(User, UUID(uid))
    if not user: return {"error":"Not Found","message":"User not found"}, 404
    return user_schema.dump(user)

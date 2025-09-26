
import os
from flask import Flask
from dotenv import load_dotenv
from flasgger import Swagger
from .extensions import db, ma, jwt
from .errors import register_error_handlers
from .security import register_security_hooks

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {"title": "Flask CRUD API", "description": "CRUD + JWT + RBAC (UUID) with Usecases", "version": "1.0.0"},
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header",
                   "description": "Masukkan: **Bearer <ACCESS_TOKEN>**"}
    }
}

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PORT"] = int(os.getenv("PORT", "5000"))
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000"))

    db.init_app(app); ma.init_app(app); jwt.init_app(app)
    Swagger(app, template=SWAGGER_TEMPLATE)

    # Blueprints
    from .routes.auth import bp as auth_bp
    from .routes.users import bp as users_bp
    from .routes.roles import bp as roles_bp
    from .routes.permissions import bp as perms_bp
    from .routes.menus import bp as menus_bp
    from .routes.items import bp as items_bp

    app.register_blueprint(auth_bp,  url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(roles_bp, url_prefix="/api/roles")
    app.register_blueprint(perms_bp, url_prefix="/api/permissions")
    app.register_blueprint(menus_bp, url_prefix="/api/menus")
    app.register_blueprint(items_bp, url_prefix="/api/items")

    register_error_handlers(app); register_security_hooks(app)

    @app.get("/health")
    def health():
        """Health check
        ---
        tags: [System]
        responses: {200: {description: OK}}
        """
        return {"status": "ok"}

    return app

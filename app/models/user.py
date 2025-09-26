
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from .base import TimestampMixin, user_roles

class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False, server_default="1")
    _password_hash = db.Column("password_hash", db.String(255), nullable=False)

    roles = db.relationship("Role", secondary=user_roles, back_populates="users")

    def set_password(self, raw: str):
        self._password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self._password_hash, raw)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"

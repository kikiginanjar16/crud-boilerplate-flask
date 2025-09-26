
import uuid
from sqlalchemy.dialects.postgresql import UUID
from ..extensions import db
from .base import TimestampMixin, user_roles, role_permissions, role_menus

class Role(db.Model, TimestampMixin):
    __tablename__ = "roles"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)

    users = db.relationship("User", secondary=user_roles, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")
    menus = db.relationship("Menu", secondary=role_menus, back_populates="roles")

    def __repr__(self):
        return f"<Role {self.id} {self.name}>"

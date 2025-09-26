
import uuid
from sqlalchemy.dialects.postgresql import UUID
from ..extensions import db
from .base import TimestampMixin, role_permissions

class Permission(db.Model, TimestampMixin):
    __tablename__ = "permissions"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    roles = db.relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission {self.id} {self.code}>"

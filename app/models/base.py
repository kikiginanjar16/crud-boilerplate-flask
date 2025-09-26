
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from ..extensions import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc), nullable=False)

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id"), primary_key=True),
)

role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", UUID(as_uuid=True), db.ForeignKey("permissions.id"), primary_key=True),
)

role_menus = db.Table(
    "role_menus",
    db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id"), primary_key=True),
    db.Column("menu_id", UUID(as_uuid=True), db.ForeignKey("menus.id"), primary_key=True),
)

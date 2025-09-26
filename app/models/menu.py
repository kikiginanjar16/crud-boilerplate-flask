
import uuid
from sqlalchemy.dialects.postgresql import UUID
from ..extensions import db
from .base import TimestampMixin, role_menus

class Menu(db.Model, TimestampMixin):
    __tablename__ = "menus"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(80), nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    is_active = db.Column(db.Boolean, default=True, nullable=False, server_default="1")

    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey("menus.id"), nullable=True)
    parent = db.relationship("Menu", remote_side=[id], backref=db.backref("children", lazy="select"))

    roles = db.relationship("Role", secondary=role_menus, back_populates="menus")

    def __repr__(self):
        return f"<Menu {self.id} {self.title}>"

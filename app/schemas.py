
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .extensions import db
from .models import User, Role, Permission, Menu

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta: model=Role; sqla_session=db.session; load_instance=True; include_fk=True
    id=fields.UUID(dump_only=True)
    name=fields.Str(required=True, validate=validate.Length(min=1,max=80))
    description=fields.Str(allow_none=True)

role_schema=RoleSchema(); roles_schema=RoleSchema(many=True)

class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta: model=Permission; sqla_session=db.session; load_instance=True; include_fk=True
    id=fields.UUID(dump_only=True); code=fields.Str(required=True); name=fields.Str(required=True)

permission_schema=PermissionSchema(); permissions_schema=PermissionSchema(many=True)

class MenuSchema(SQLAlchemyAutoSchema):
    class Meta: model=Menu; sqla_session=db.session; load_instance=True; include_fk=True
    id=fields.UUID(dump_only=True)
    children=fields.Nested(lambda: MenuSchema(exclude=("children",)), many=True, dump_only=True)

menu_schema=MenuSchema(); menus_schema=MenuSchema(many=True)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta: model=User; sqla_session=db.session; load_instance=True; include_fk=True
    id=fields.UUID(dump_only=True)
    username=fields.Str(required=True, validate=validate.Length(min=3,max=80))
    email=fields.Email(required=True)
    password=fields.Str(load_only=True, required=True)
    roles=fields.Nested(lambda: RoleSchema(only=("id","name")), many=True, dump_only=True)

user_schema=UserSchema(); users_schema=UserSchema(many=True)

class IdsSchema(SQLAlchemyAutoSchema):
    class Meta: model=None; load_instance=False
    ids=fields.List(fields.UUID(), required=True)

ids_schema=IdsSchema()


# Flask CRUD with Usecases (UUID + JWT + RBAC + Swagger)

This version separates **routing** (`app/routes`) from **business logic / usecases** (`app/usecases`).

## Structure
```
app/
  models/           # SQLAlchemy models (UUID)
  usecases/         # Business logic (CRUD, pagination, relations)
  routes/           # HTTP layer, marshmallow, auth guards
  schemas.py        # Marshmallow schemas
  security.py       # Permission decorator
  errors.py         # Error handlers
  extensions.py     # db, jwt
  __init__.py       # app factory + Swagger
```
## Run
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m flask --app manage db init
python -m flask --app manage db migrate -m "init"
python -m flask --app manage db upgrade
python wsgi.py
```
Open Swagger: http://localhost:5000/apidocs

# Flask CRUD Boilerplate

A comprehensive Flask boilerplate for building REST APIs with CRUD operations, JWT authentication, and Role-Based Access Control (RBAC). This project follows clean architecture principles with use cases and includes Swagger documentation.

## Features

- ✅ **CRUD Operations** - Complete Create, Read, Update, Delete functionality
- 🔐 **JWT Authentication** - Access and refresh token support
- 👥 **Role-Based Access Control (RBAC)** - User roles and permissions system
- 📚 **Clean Architecture** - Organized with models, routes, use cases, and schemas
- 📖 **API Documentation** - Swagger/OpenAPI documentation with Flasgger
- 🗄️ **Database Support** - SQLAlchemy with migration support
- 🆔 **UUID Primary Keys** - Using UUIDs for better security and scalability
- ⚡ **Environment Configuration** - Flexible configuration with .env files
- 🛡️ **Error Handling** - Centralized error handling and security hooks

## Tech Stack

- **Framework**: Flask 3.0.3
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **Serialization**: Marshmallow
- **Database Migration**: Flask-Migrate
- **API Documentation**: Flasgger (Swagger)
- **Environment Management**: python-dotenv

## Project Structure

```
crud-boilerplate-flask/
├── app/
│   ├── __init__.py              # Application factory
│   ├── errors.py                # Error handlers
│   ├── extensions.py            # Flask extensions
│   ├── schemas.py               # Marshmallow schemas
│   ├── security.py              # JWT security hooks
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── base.py              # Base model mixins
│   │   ├── user.py              # User model
│   │   ├── role.py              # Role model
│   │   ├── permission.py        # Permission model
│   │   └── menu.py              # Menu model
│   ├── routes/                  # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── users.py             # User CRUD endpoints
│   │   ├── roles.py             # Role management
│   │   ├── permissions.py       # Permission management
│   │   ├── menus.py             # Menu management
│   │   └── items.py             # Generic items CRUD
│   └── usecases/                # Business logic layer
│       ├── __init__.py
│       ├── common.py            # Common use cases
│       ├── users.py             # User business logic
│       ├── roles.py             # Role business logic
│       ├── permissions.py       # Permission business logic
│       └── menus.py             # Menu business logic
├── manage.py                    # Flask CLI and migration commands
├── wsgi.py                      # WSGI entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crud-boilerplate-flask
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///app.db
   JWT_SECRET_KEY=your-secret-key-here
   JWT_ACCESS_TOKEN_EXPIRES=3600
   JWT_REFRESH_TOKEN_EXPIRES=2592000
   PORT=5000
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python manage.py
   # or
   flask run
   ```

The API will be available at `http://localhost:5000`

## API Documentation

Once the application is running, you can access the Swagger documentation at:
- **Swagger UI**: `http://localhost:5000/apidocs/`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token

### User Management
- `GET /api/users` - List all users
- `GET /api/users/<id>` - Get user by ID
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Role Management
- `GET /api/roles` - List all roles
- `POST /api/roles` - Create new role
- `GET /api/roles/<id>` - Get role by ID
- `PUT /api/roles/<id>` - Update role
- `DELETE /api/roles/<id>` - Delete role

### Permission Management
- `GET /api/permissions` - List all permissions
- `POST /api/permissions` - Create new permission
- `GET /api/permissions/<id>` - Get permission by ID
- `PUT /api/permissions/<id>` - Update permission
- `DELETE /api/permissions/<id>` - Delete permission

### Menu Management
- `GET /api/menus` - List all menus
- `POST /api/menus` - Create new menu
- `GET /api/menus/<id>` - Get menu by ID
- `PUT /api/menus/<id>` - Update menu
- `DELETE /api/menus/<id>` - Delete menu

### Items (Generic CRUD)
- `GET /api/items` - List all items
- `POST /api/items` - Create new item
- `GET /api/items/<id>` - Get item by ID
- `PUT /api/items/<id>` - Update item
- `DELETE /api/items/<id>` - Delete item

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Example Login Flow

1. **Register a user**:
   ```bash
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword",
       "full_name": "John Doe"
     }'
   ```

2. **Login to get tokens**:
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "securepassword"
     }'
   ```

3. **Use the access token for authenticated requests**:
   ```bash
   curl -X GET http://localhost:5000/api/users \
     -H "Authorization: Bearer <access_token>"
   ```

## Database Models

### User
- `id` (UUID): Primary key
- `username` (String): Unique username
- `email` (String): Unique email address
- `full_name` (String): Full name (optional)
- `avatar_url` (String): Profile picture URL (optional)
- `is_active` (Boolean): Account status
- `password_hash` (String): Hashed password
- `created_at`, `updated_at` (DateTime): Timestamps

### Role
- `id` (UUID): Primary key
- `name` (String): Role name
- `description` (String): Role description
- Many-to-many relationship with Users and Permissions

### Permission
- `id` (UUID): Primary key
- `name` (String): Permission name
- `description` (String): Permission description
- Many-to-many relationship with Roles

## Development

### Database Migrations

When you modify models, create and apply migrations:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Running Tests

```bash
python -m pytest
```

### Code Structure Guidelines

- **Models**: Define database schema and relationships
- **Schemas**: Handle serialization/deserialization with Marshmallow
- **Routes**: Define API endpoints and handle HTTP requests
- **Use Cases**: Contain business logic and data processing
- **Extensions**: Initialize Flask extensions
- **Security**: Handle JWT authentication and authorization

## Configuration

The application supports the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///app.db` | Database connection string |
| `JWT_SECRET_KEY` | `change-me` | Secret key for JWT tokens |
| `JWT_ACCESS_TOKEN_EXPIRES` | `3600` | Access token expiration (seconds) |
| `JWT_REFRESH_TOKEN_EXPIRES` | `2592000` | Refresh token expiration (seconds) |
| `PORT` | `5000` | Server port |

## Deployment

### Using Gunicorn

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
   ```

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you have any questions or need help, please open an issue in the repository.
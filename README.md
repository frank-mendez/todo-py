# To-Do Application Project Requirements

## 1. Overview

This document outlines the requirements for a to-do application with separate repositories for the API backend, web frontend, and mobile application. The application will provide users with the ability to create, manage, and organize tasks across multiple platforms.

## 2. Core Features

### 2.1 Task Management

- Create new tasks with title, description, due date, and priority
- Mark tasks as complete/incomplete
- Edit existing task details
- Delete tasks
- Organize tasks into categories/lists
- Filter tasks by status, due date, and priority
- Search tasks by title or description
- Bulk actions (delete, mark complete, etc.)

### 2.2 User Management

- User registration and authentication
- Profile management
- Password reset functionality
- Account deletion

### 2.3 Data Synchronization

- Real-time updates across devices
- Offline capability for mobile app with sync on reconnection
- Data backup and restore

### 2.4 User Interface Requirements

- Responsive design for web application
- Platform-specific UI patterns for mobile application
- Consistent theming and branding across platforms
- Light/dark mode support

## 3. User Roles

### 3.1 Unauthenticated User

- View login/registration page
- Create a new account
- Reset password

### 3.2 Authenticated User

- Manage personal profile
- Create and manage tasks
- Organize tasks into categories
- View task statistics and summaries
- Change account settings
- Log out of the application

## 4. Technical Requirements

### 4.1 API Backend (Python)

- RESTful API design
- Authentication using JWT tokens
- Database for storing user and task data
- API documentation
- Unit and integration tests
- Rate limiting and security measures

### 4.2 Web Frontend (NextJS)

- Server-side rendering for improved SEO and performance
- Responsive design for desktop and mobile browsers
- State management
- Form validation
- Unit and integration tests

### 4.3 Mobile Application (React Native)

- Support for iOS and Android platforms
- Native-like user experience
- Offline data persistence
- Push notifications
- Unit and integration tests

### 4.4 DevOps

- CI/CD pipelines for each repository
- Automated testing
- Deployment strategies for each component
- Monitoring and error reporting

## 5. API Endpoints

### 5.1 Authentication Endpoints

- `POST /api/v1/auth/token` - Login and get access token
- `GET /api/v1/auth/me` - Get current user information

### 5.2 User Endpoints

- `POST /api/v1/users` - Register a new user
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `DELETE /api/v1/users/me` - Delete current user account

### 5.3 Task Endpoints

- `GET /api/v1/tasks` - List all tasks for current user
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get task details
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task
- `PATCH /api/v1/tasks/{task_id}/status` - Update task status

### 5.4 Category Endpoints

- `GET /api/v1/categories` - List all categories
- `POST /api/v1/categories` - Create a new category
- `GET /api/v1/categories/{category_id}` - Get category details
- `PUT /api/v1/categories/{category_id}` - Update a category
- `DELETE /api/v1/categories/{category_id}` - Delete a category
- `GET /api/v1/categories/{category_id}/tasks` - List tasks in category

All endpoints except authentication require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

Detailed API documentation is available at:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 6. Data Models

### 6.1 User Model

- id: UUID
- username: String (unique)
- email: String (unique)
- password: String (hashed)
- first_name: String (optional)
- last_name: String (optional)
- created_at: DateTime
- updated_at: DateTime

### 6.2 Task Model

- id: UUID
- user_id: UUID (foreign key)
- category_id: UUID (foreign key, optional)
- title: String
- description: Text (optional)
- status: Enum (todo, in_progress, completed)
- priority: Enum (low, medium, high)
- due_date: DateTime (optional)
- created_at: DateTime
- updated_at: DateTime

### 6.3 Category Model

- id: UUID
- user_id: UUID (foreign key)
- name: String
- color: String (hex color code)
- created_at: DateTime
- updated_at: DateTime

## 7. Non-Functional Requirements

### 7.1 Performance

- API response time under 200ms for 95% of requests
- Web app initial load under 2 seconds
- Mobile app startup under 3 seconds

### 7.2 Security

- HTTPS for all communications
- Secure password storage (bcrypt or similar)
- CSRF protection
- Input validation and sanitization
- Rate limiting to prevent abuse

### 7.3 Scalability

- Horizontal scaling capability for API
- CDN integration for web assets
- Database indexing for performance

### 7.4 Accessibility

- WCAG 2.1 AA compliance for web application
- Screen reader support for mobile application
- Keyboard navigation for web application

## 8. FastAPI + PostgreSQL API Folder Structure

```
todo_api/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── errors/
│   │   │   └── __init__.py
│   │   │
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── tasks.py
│   │       ├── categories.py
│   │       └── users.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── category.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── category.py
│   │   └── auth.py
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── category.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── stats.py
│   │
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_tasks.py
│   │   └── test_categories.py
│   │
│   └── test_services/
│       ├── __init__.py
│       └── test_auth.py
│
├── scripts/
│   ├── format.sh
│   ├── lint.sh
│   └── test.sh
│
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 9. Getting Started

### 9.1 Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- pip (Python package installer)

### 9.2 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/todo-py.git
cd todo-py
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file:

```bash
cp .env.example .env
```

5. Update `.env` with your database credentials:

```ini
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_DB=todo
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 9.3 Database Setup

1. Create PostgreSQL database:

```bash
createdb todo
```

2. Run database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 9.4 Running the Server

1. Start the development server:

```bash
uvicorn app.main:app --reload --port 8000
```

2. Access the API:

- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc
- API Base URL: http://localhost:8000/api/v1

### 9.5 Development Commands

```bash
# Run tests
pytest

# Check code style
flake8

# Format code
black .

# Generate API documentation
python scripts/generate_openapi.py
```

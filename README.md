# Event Management API

#### A RESTful API built with Django & Django REST Framework for managing and moderating user-submitted events.

## Features
- User registration and authentication with JWT
- Event creation by users
- Event approval by admin
- Role-based permissions (user, admin)
- Search and filtering by:
  - Title, description, location
  - Date range
  - Approval status (admin only)
  - Ordering by date and title (alphabet)
- Email notifications for:
  - Event creation
  - Event approval
  - Event deletion

## MVP Vision
To scale moderation and reduce manual workload for admins, an **AI-based approval system** could be introduced:
- **Content validation**
  - Automatically reject events containing offensive words or suspicious links
  - Prevent HTML/script injections

- **Spam and Safety Filtering**
  - Use a lightweight AI model or 3rd-party API to detect
    - Spam phrases
    - Blacklisted domains
    - Repetitive/unusual text patterns

- **Optional Manual Review**
  - Flag events for admin review (instead of full auto-approval)

## Tech Stack
- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL
- `uv` package manager (`pyproject.toml`, `uv.lock`)
- Docker + Docker Compose
- Celery + Redis (for async email)

## Build and start containers
1. Setup .env file (in general directory ./.env) (postgres variables is an optional)
    - POSTGRES_DB
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - POSTGRES_HOST
    - POSTGRES_PORT
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
2. Run the containers
    - `docker compose up --build`
3. Make a migrations, run next commands
    - `docker compose exec web python project/manage.py makemigrations`
    - `docker compose exec web python project/manage.py migrate`
4. Add superuser (optional)
    - `docker compose exec web python project/manage.py createsuperuser`

## API Endpoints
### Auth
| Method | Endpoint                    | Description                     | Payload |
| ------ | --------------------------- | ------------------------------- | ------- |
| POST   | `/api/users/token/`         | Get JWT access & refresh tokens | username: str, password: str |
| POST   | `/api/users/token/refresh/` | Refresh access token            | refresh: str |
| POST   | `/api/users/register/`      | Registration                    | username: str, email: str, password: str, password2: str |

### Events
| Method | Endpoint                   | Description                    | Payload |
| ------ | -------------------------- | ------------------------------ | ------- |
| GET    | `api/events/`              | List approved events (+search) | - |
| POST   | `api/events/`              | Create new event               | title: str(150), description: str, date: str (format: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]), location: str(150) |
| GET    | `api/events/<id>/`         | Get event by ID                | - |
| PATCH  | `api/events/<id>/`         | Update own event               | title: str(150), description: str, date: str (format: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]), location: str(150) |
| DELETE | `api/events/<id>/`         | Delete event                   | - |
| POST   | `api/events/<id>/approve/` | Approve event (admin only)     | - |
| GET    | `api/events/unapproved/`   | List of all unapproved events (admin only) | - |

## Filtering & Search
Available query params on `GET /api/events/`
| Param         | Example                              | Description                            |
| ------------- | ------------------------------------ | -------------------------------------- |
| `search`      | `?search=django`                     | Search by title, description, location |
| `location`    | `?location=Berlin`                   | Filter by location                     |
| `start_date`  | `?start_date=2025-06-01T00:00:00Z`   | Events from this date                  |
| `end_date`    | `?end_date=2025-06-30T00:00:00Z`     | Events until this date                 |
| `is_approved` | `?is_approved=false` (admin only)    | Filter by approval status              |
| `ordering`    | `?ordering=date`, `?ordering=-title` | Sort events                            |

## Permissions
| Role          | Action                             |
| ------------- | ---------------------------------- |
| Public        | View approved events               |
| Authenticated | Create, view own events            |
| Organizer     | Edit/delete own events             |
| Admin         | Approve/delete any event, view all |

## Author
Developed by Borodianskyi Mykhailo.

## Time spend
| Operation             | Time             |
| --------------------- | ---------------- |
| Recieve task          | 20 June 12:13 PM |
| Research (Tech stack) | 30m              |
| Coding session        | 5h               |
| Generating docs       | 1h               |
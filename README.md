# Workflow State Management Service API

A **FastAPI** service for managing workflow items with state transitions, versioning, and PostgreSQL persistence. Fully Dockerized for easy deployment.

---

## Features

* CRUD operations for workflow items
* Status-based workflow with allowed transitions
* Optimistic concurrency control (ETag / versioning)
* PostgreSQL backend
* Dockerized API + Database
* Optional frontend dashboard support

---

## Tech Stack

* **Backend:** FastAPI, SQLAlchemy, Pydantic
* **Database:** PostgreSQL
* **Docker:** API + Database containers
* **Frontend:** Optional dashboard (React / Tailwind)

---

## Getting Started

### Prerequisites

* [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
* Optional: Python 3.11+ (for local dev without Docker)

---

### Running with Docker

1. Clone the repository:

```bash
git clone <your-repo-url>
cd workflow-state-management-service
```

2. Build and start the containers:

```bash
docker-compose up --build
```

3. API will be available at:

```
http://localhost:8000
```

4. Swagger / OpenAPI docs:

```
http://localhost:8000/docs
```

---

### Running Locally (without Docker)

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Update `DATABASE_URL` in `.env` or `app/db.py` if needed.
4. Run migrations or create tables:

```bash
python -m app.main
```

5. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

| Method   | Endpoint               | Description                                         |
| -------- | ---------------------- | --------------------------------------------------- |
| `POST`   | `/workflow_items/`     | Create a workflow item                              |
| `GET`    | `/workflow_items/`     | List workflow items (optional filtering)            |
| `GET`    | `/workflow_items/{id}` | Get a workflow item by ID                           |
| `PUT`    | `/workflow_items/{id}` | Update a workflow item (requires `If-Match` header) |
| `DELETE` | `/workflow_items/{id}` | Delete a workflow item                              |

**Notes:**

* ETag header is used for optimistic concurrency control (`If-Match` required on updates).
* Allowed status transitions:

  * `CREATED → IN_PROGRESS / CANCELLED`
  * `IN_PROGRESS → COMPLETED / CANCELLED`
  * `COMPLETED` and `CANCELLED` are terminal states.

---

## Docker Compose Overview

```yaml
services:
  api:
    build: .
    container_name: workflow_api
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/workflow
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: >
      sh -c "sleep 3 && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
  db:
    image: postgres:15
    container_name: workflow_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: workflow
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

---

## Contributing

1. Fork the repository.
2. Create a branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Create a Pull Request.

---

## License

MIT License. See [LICENSE](LICENSE) file for details.


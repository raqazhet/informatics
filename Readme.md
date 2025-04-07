

```markdown
# 🧠 Informatics Learning Platform

A web application to support learning **informatics** for secondary school students, integrated with **DeepSeek** for enhanced AI capabilities.

This project is built using modern technologies like **Python**, **Django**, **Poetry**, **Docker**, and **Docker Compose**.

---

## 🚀 Features

- Course management system for informatics topics.
- AI-assisted content through DeepSeek.
- Admin panel for managing content and users.
- Redis integration for background tasks or caching.
- Built-in user management.

---

## 🛠 Tech Stack

- Python
- Django
- Poetry
- Docker & Docker Compose
- PostgreSQL
- Redis

---

## 📦 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/raqazhet/informatics.git
cd informatics
```

### 2. Set up the environment

#### Create a `.env` file in the project root:

```env
OPEN_AI_ROUTER_KEY=your_value_here
```

> Replace `your_value_here` with your actual DeepSeek or OpenAI integration key.

### 3. Start PostgreSQL and Redis

You can use Docker Compose or your own setup.

To use Docker Compose:

```bash
docker-compose up -d
```

This will start both PostgreSQL and Redis containers as defined in `docker-compose.yml`.

### 4. Install dependencies and set up the project

#### Install Poetry dependencies:

```bash
poetry install
```

#### Apply database migrations:

```bash
poetry run python manage.py migrate
```

#### Create a superuser account:

```bash
poetry run python manage.py createsuperuser
```

### 5. Run the development server

```bash
poetry run python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser to access the app.

---

## 📁 Project Structure

```bash
informatics/
├── course/               # App for courses
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│
├── users/                # App for user management
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│
├── static/               # Static files
├── templates/            # HTML templates
├── manage.py             # Django management script
├── docker-compose.yml    # Compose file for PostgreSQL and Redis
├── Makefile              # Optional: useful commands
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## 🧪 Testing

You can run tests using:

```bash
poetry run python manage.py test
```

---

## 📬 Contact

Maintained by [@raqazhet](https://github.com/raqazhet). Contributions are welcome!

---

## 📘 License

This project is licensed under the MIT License.
```

---

Let me know if you want to add badges, screenshots, API routes, or deployment instructions as well!
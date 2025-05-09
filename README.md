# KanMind - Kanban Board Project

## Description
KanMind is a modern Kanban board application built with Django and Django REST Framework. It helps teams organize their work visually, manage tasks efficiently, and improve workflow transparency.

### Features
- Create and manage multiple boards
- Drag & drop task management
- Task status tracking (To-Do, In Progress, Review, Done)
- Task priority levels
- User assignment and review system
- Comment system for tasks
- Real-time updates
- Token-based authentication

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment tool

### Setup Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/kanMind.git
cd kanMind
```

2. **Create and Activate Virtual Environment**
```bash
python -m venv env
.\env\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Variables**
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser (Admin)**
```bash
python manage.py createsuperuser
```

7. **Run Development Server**
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

# Django Note-Taking App

A simple note-taking application built with Django and Tailwind CSS. Users can create, view, edit, delete, and search notes.

## Features

- Create, read, update, and delete notes
- Search notes by title or content
- Mobile-responsive design with Tailwind CSS
- Admin interface for managing notes

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`
8. Visit `http://127.0.0.1:8000`

## Usage

- Visit the homepage to see all your notes
- Use the search bar to find specific notes
- Click on a note title to view details
- Use the "New Note" button to create a new note
- Edit or delete notes from their detail page

## Technologies

- Django
- Tailwind CSS
- SQLite (development) 
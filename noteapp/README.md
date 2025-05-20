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

## Running with Docker

To build and run this application using Docker, follow these steps:

1.  **Build the Docker image:**
    ```bash
    docker build -t noteapp .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 noteapp
    ```
    This will start the Django development server inside the container, accessible at `http://localhost:8000` on your host machine.

    To run the container in detached mode (in the background), use the `-d` flag:
    ```bash
    docker run -d -p 8000:8000 noteapp
    ```

## Technologies

- Django
- Tailwind CSS
- SQLite (development) 
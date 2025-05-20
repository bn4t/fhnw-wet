# Use an official Python 3.9 image as the base
FROM python:3.9

# Set up a working directory /app
WORKDIR /app

# Copy requirements.txt to /app/requirements.txt
COPY noteapp/requirements.txt /app/requirements.txt

# Install dependencies using pip install -r requirements.txt
RUN pip install -r requirements.txt

# Copy the noteapp directory to /app/noteapp
COPY noteapp /app/noteapp

# Expose port 8000
EXPOSE 8000

# Set the default command to python noteapp/manage.py runserver 0.0.0.0:8000
CMD ["python", "noteapp/manage.py", "runserver", "0.0.0.0:8000"]

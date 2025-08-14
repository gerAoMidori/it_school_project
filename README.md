# We have developped a Quizz website


# Django Application Setup Guide

## 1. Installing Django
Open a terminal and run the following command to install Django:

```bash
pip install django
```

## 2. Accessing the Project
Navigate to the directory containing the following files:
- `manage.py`
- `db.sqlite3`
- the folders `myapp` and `quiz`

## 3. Applying Database Migrations
In this directory, open a terminal and run the following command:

```bash
python manage.py migrate
```

## 4. Starting the Server
Then, start the Django development server with the command:

```bash
python manage.py runserver
```

## 5. Accessing the Application
Once the server is running, open a web browser and visit the following address to access the application:

```
http://127.0.0.1:8000
``` 
# Setting Up ONLINE STORE Project

This guide will walk you through setting up a Online Store project, including installing dependencies, setting up environment variables, and running the project in development mode.

## Prerequisites

Before getting started, ensure you have the following installed on your system:

- python

## Steps

### 1. Clone the project from Github repository

```bash
git clone https://github.com/YAYI68/online-store.git

```

### 2. Set up your virtual environment

```bash
python -m venv env

env\Scripts\activate 
```

### 3. Install Dependencies
Navigate into your project directory:

```bash
pip install -r requirements.txt 
```

### 3.  Set Up Environment Variables
Create a .env file in the root of your project. Add the necessary environment variables
```
SECRET_KEY = Django Secret Key
DEBUG = True
DB_NAME= your db name
DB_USER=postgres 
DB_PASSWORD= your password
DB_HOST= hostname
DB_PORT=5432
```

### 4. Run the Project in Development Mode
Finally, you can run the project in development mode:
```bash
python manage.py runserver
```
it will be accessible at http://127.0.0.1:8000.

## Testing the Rest Api 
You can use desktop postman or the live postman to test your queries,
here is the link to [**view the api**](https://documenter.getpostman.com/view/14724403/2sA3XS9fUj)

## Conclusion 
You have successfully setup the project


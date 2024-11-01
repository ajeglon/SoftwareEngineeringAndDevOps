# MATEXAPPLICATION
**Software Engineering Assignment**

An application to be used by NHSBSA employees to Create, Read, Update and Update Maternity Exemption Certificates

**Getting started**

**Admin User: Admin**

**Admin Password: MATEXADMIN**

**Requirements:**
- [python](https://www.python.org)

**Mac**
- setup a virtual environment: `python3 -m venv env`
- start the virtual environment: `source .venv/scripts/activate`
- install django: `pip install django`
- run the web app: `python manage.py runserver`

**Windows**
- create the virtual environment: `py -3 -m venv .venv`
- start the virtual environment: `.venv\scripts\activate`
- install django: `pip install django`
- install dependencies: `pip install -r requirements.txt`
- run the web app: `python3 manage.py runserver`

**Resources**
- [VSCode Guide to Django](https://code.visualstudio.com/docs/python/tutorial-django)

**Dependency management**
- perform the following steps while the virtual environment is active.
- whenever a new dependency is added generate a new dependency list using
`pip freeze > requirements.txt` and push changes.
- When a dependency has been added by another user, pull main and install
dependencies using `pip install -r requirements.txt`
- By doing this everyone's virtual environment will remain up to date.

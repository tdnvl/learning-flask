# Learning Flask
An API-centric project to learn how to bring Python to the Web through Flask, a micro webdevelopment framework.

## Course

This project is based on the Lynda.com course of the same name: [Learning Flask](https://www.lynda.com/Flask-tutorials/Learning-Flask/521231-2.html).

## virtualenv

This project relies on [virtualenv](https://virtualenv.pypa.io/en/stable/) to safely install and run Flask without compromising other libraries on my machine.

To create a virtualenv environment, type in the root folder:

`$ virtualenv ENV`

To activate it, navigate to the containing folder and type:

`source venv/bin/activate`

To stop working in the virtual environment, type:

`$ deactivate`

## Deploying to Heroku

A few things need to happen to deploy the app to Heroku:

### Install gunicorn

[Gunicorn](http://gunicorn.org/) 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.

`$ pip install gunicorn`

### requirements.txt

Create a file named requirements.txt that will list all of the Python libraries we have installed.

`$ pip freeze > requirements.txt`

### Create Procfile

This file will tell Heroku to run Flask using Gunicorn.

`$ touch Procfile`

Note the capital P.

Add this line to Procfile:

`web: gunicorn routes:app`

Note that there is no space between `routes:` and `app`. I had one and it broke the Heroku app!

### Install the Heroky CLI

Instructions can be found here: [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli). I ended up using the macOS installer—I don't have brew on my work machine.

### Create Heroku app

Type:

`heroku create`

Heroku will ask for credentials and return a custom URL. A git repo will be built, too.

## Postgres database

I've used [Postgres.app,](https://postgresapp.com/) a full-featured PostgreSQL installation packaged as a standard Mac app.

The command to create a new database is:

`user=# create database learningflask;`






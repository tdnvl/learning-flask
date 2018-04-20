# Learning Flask
An API-centric project to learn how to bring Python to the Web through Flask, a micro webdevelopment framework. This is based on the Lynda.com course taught by Lalith Polepeddi ([@polepeddi](https://github.com/lpolepeddi)).

## Course

This project is based on the Lynda.com course of the same name: [Learning Flask](https://www.lynda.com/Flask-tutorials/Learning-Flask/521231-2.html).

## virtualenv

This project relies on [virtualenv](https://virtualenv.pypa.io/en/stable/) to safely install and run Flask without compromising other libraries on my machine.

To create a virtualenv environment, type in the root folder:

`$ virtualenv venv`

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

Heroku will ask for credentials and return a custom URL.

Changes can be pushed directly to the Heroku app through:

`git push heroku master`

## Postgres database

I've used [Postgres.app,](https://postgresapp.com/) a full-featured PostgreSQL installation packaged as a standard Mac app.

### Create a new database

To launch postgres in the CLI, type:

`psql postgres`

The command to create a new database is:

`user=# create database learningflask;`

Connect to the database:

`user=# \c learningflask`

Postgres should return:

`You are now connected to database "learningflask" as user "user".`

### Create a table

```
CREATE TABLE users (
	uid serial PRIMARY KEY,
	firstname VARCHAR(100) not null,
	lastname VARCHAR(100) not null,
	email VARCHAR(120) not null unique,
	pwdhash VARCHAR(100) not null
	);
```


See that the table is created and empty:

`SELECT * from users;`

### Create a new user

`INSERT INTO users (firstname,lastname,email,pwdhash) VALUES ('Thomas','Deneuville','thomas@thomasdeneuville.com','learning-flask');`

### Salted passwords

The app uses the `generate_password_hash` and `check_password_hash` functions from `werkzeug`. See [this snippet page](http://flask.pocoo.org/snippets/54/) for more info.


### Connect the Postgres database to Flask

We will need to install [SQLAlchemy,](https://www.sqlalchemy.org/) a Flask extension for that.

`pip install Flask-Migrate`

Add a line of code in `routes.py`:

`app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'`

### Close psql utility

The command is:

`\q`

## User model

## Signing up

### Flask-WTF

Install Flask-WTF by getting back into the venv, then use:

`$ pip install flask-wtf`

### Form generation

We first insert a hidden tag to protect ourselves from CSRF attacks. In the `signup.html` template, in the body of the `<form>`:

`{{ form.hidden_tag() }}`

For each form group (field), we add the field label and the field box:

```
<div class="form-group">
	{{ form.first_name.label }}
	{{ form.first_name }}
</div>
```

### Form logic

The `signup.html` page can see two methods: GET when the page is accessed and POST when the form is submitted. We need to account for that logic or we'll otherwise get a method error upon submit:

```
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
    	return "Success!"

    elif request.method == 'GET':
    	return render_template("signup.html", form=form)
```
<div class="form-group">
	{{ form.first_name.label }}

	{% if form.first_name.errors %}
		{% for error in form.first_name.errors %}
			<p class="error-message">{{ error }}</p>
		{% endfor %}
	{% endif %}

	{{ form.first_name }}
</div>

`from wtforms.validators import DataRequired`

to `forms.py` to import the `DataRequired` WTForms validator. [Read more details on built-in validators.](http://wtforms.readthedocs.io/en/latest/validators.html#built-in-validators)

We then make sure that these validators are declared for each field. It is possible to add a custom message, too. For example, on the email field:

`email = StringField('Email', validators=[DataRequired("Please enter your email address."),Email("Please enter a valid email address.")])`

Note that for using the `Email` validator, I had to import it, too:

`from wtforms.validators import DataRequired, Email`

## Showing errors on the front-end

We'll also need to work on the template to loop through the errors that the validators return and display them. For each field in `signup.html`:

```
<div class="form-group">
	{{ form.first_name.label }}

	{% if form.first_name.errors %}
		{% for error in form.first_name.errors %}
			<p class="error-message">{{ error }}</p>
		{% endfor %}
	{% endif %}

	{{ form.first_name }}
</div>
```

### Saving a user to the database

Import the `user` class from `models` in `routes.py`. We already import `db`:

`from models import db, User`

Still in `routes.py`, under the success case for the POST method, create a new user and pass the data we get from the form, field by field, using the `.data` method:

`newuser = User(form.first_name.data,form.last_name.data,form.email.data,form.password.data)`

Next, we'll add the info to the database using `db.session.add` and `db.session.commit`:

```
db.session.add(newuser)
db.session.commit()
```

## Logging in and logging out

### Sessions

In `routes.py` import: `session, redirect,` and `url_for` from Flask.

When a new user signs up (`request.method == 'POST'` and `form.validate() == True`), create a new session passing the email address:

`session['email'] = newuser.email`

And redirect to the homepage:

`return redirect(url_for('home'))`

### Login

1. Create a new class called login form in `forms.py`
2. Create a new URL mapping for /login in `routes.py`
3. Create a web tempate in templates

Don't forget to import the LoginForm we created in `forms.py` in `routes.py` so we can use it in the new class we're creating.

### Sign out

Logging a user == creating a new session
Logging a user out == deleting that session

We delete a session by using the `session.pop()` method. In `routes.py`:

```
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
```

We don't need to create a template for `/logout`. When the page is requested, it simply deletes the cookie and redirects to the home page.

## Authorization

If a user is logged in, they shouldn't see the sign up or the log in form. They should be redirected to the home page.

If a user is logged out, they shouldn't have access to the home page (≠ from index). They should be redirected to the login page.

### Protecting the home page

Let's add some logic in `home()`:

`if 'email' not in session:
	return redirect(url_for('login'))
else:
	return render_template("home.html)`

### Protecting to the login and signup pages

Under `signup()`:

`if 'email' in session:
	return redirect(url_for('home))`

Add the same code under `login()`.

[Flask-Login](https://flask-login.readthedocs.io/en/latest/) does a really good job at that!

## Bookmarking places

### Create another form

In `forms.py`:

```
class AddressForm(Form):
	address = StringField('Address', validators=[DataRequired("Please enter an address.")])
	submit = SubmitField('Search')
```

Don't forget to import it to `routes.py`! The import statement now looks like:

`from forms import SignupForm, LoginForm, AddressForm`

Remember: A form has two states: a POST and a GET.

Make sure that the route for `home` has the two methods declared:

`@app.route("/home", methods=['GET', 'POST'])`

Since the page has a form.

## Finally, pushing the app to Heroku

We started by talking about Heroku, and thankfully, the author has published [a wiki explaining in detail how to deploy the app on Heroku!](https://github.com/lpolepeddi/learning-flask/wiki/Deploying-Flask-to-Heroku)


from flask import Flask, render_template, request
from models import db
from forms import SignupForm
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'

# Heroku database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ssksxhruuyeypf:d621f2ebfa613396f3f338a90c913b960dfb5b62f62eb38114887cc5c0fa7482@ec2-54-235-146-184.compute-1.amazonaws.com:5432/d561jjsn1du0hq'

db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
    	return "Success!"

    elif request.method == 'GET':
    	return render_template("signup.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)

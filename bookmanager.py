# Building a CRUD app with Flask and SQLALchemy
# Create, Read, Update and Delete


import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__)) # figure out where project path is
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db")) # set up db file. sqlite is the engine we are using

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file # tell the web app where the db will be stored

db = SQLAlchemy(app) # intialize the connection
class Book(db.Model): # create a class inheriting a basic db model
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True) # title is an attribute of the object we create

    def __repr__(self):
        return "<Title: {}>".format(self.title) # how to represent our book opject

'''Initializing our database:
Run the following commands in a Python shell in your project directory in order to create our database:
try python3 rather than typing pyhton

then in the console type:

>>> from bookmanager import db
>>> db.create_all()
>>> exit()

this wull cause a file 'bookdatabase.db' to appear in your folder
'''

# Note below: we can access the data that they submitted through the request.form

@app.route("/", methods=["GET","POST"]) # GET is default, this both GET and POST
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update",methods=["POST"])
def update():
    newtitle = request.form.get("newtitle") # Gets the old and updated title from the form
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first() # Fetches the book with the old title from the database
    book.title = newtitle # Updates that book's title to the new title
    db.session.commit() # Saves the book to the database
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")
    
    

if __name__ == "__main__":
    app.run(debug=True)


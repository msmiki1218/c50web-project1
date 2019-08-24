import os
import requests

from flask import Flask, session, render_template, request, url_for, redirect, g, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'ss-NSNs1A-lk8sMbfFFNEQ'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# functions
def addReview(revTuple):
    # adds user review to reviews table
    db.execute("INSERT INTO reviews (user_id, book_id, rating, opinion) VALUES (:user_id, :book_id, :rating, :opinion)",
        {"user_id": revTuple[0], "book_id": revTuple[1], "rating": revTuple[2], "opinion": revTuple[3]})
    db.commit()

def checkLoginInfo(username, password):
    # check if username, password is in database for login
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
        return False
    else:
        return True

def checkUsername(username):
    # check if username in database for registration
    if db.execute("SELECT * FROM users WHERE username = :username ", {"username": username}).rowcount == 0:
        return False
    else:
        return True

def checkReviews(book_id,user_id):
    # check if user had written a review for a given book 
    return db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": user_id, "book_id": book_id}).rowcount==0
     

def getBookbyISBN(isbn):
    # gets book information using isbn number
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    return book

def getReviews(book_id):
    # gets list of reviews for a given book
	review_list = []
	book_reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id})
	for book_review in book_reviews:
            user = getUsername(book_review.user_id)
            rating = book_review.rating
            opinion = book_review.opinion
            review_list.append({"user": user, "rating": rating, "opinion": opinion})
	return review_list
    
def getUserID(username):
    # get user id for a given userame
	user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
	return user.id

def getUsername(user_id):
    # get username given user id
	user = db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id}).fetchone()
	return user.username

def noReviews(book_id):
    #checks if a given book idea has any reviews
    return db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).rowcount==0

# routes

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route("/")
def index():
    users = db.execute("SELECT * FROM users").fetchall()
    books = db.execute("SELECT * FROM books").fetchall()
    reviews = db.execute("SELECT * FROM reviews").fetchall()
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template("index.html", title = "Home")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if not g.username:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if checkLoginInfo(username, password):
                session['username'] = request.form['username']
                session['id'] = getUserID(session['username'])
                return redirect(url_for('search'))
            else:
                error = "We can't find you... please try again or register."
    else:
        error = "You are already logged in."
    return render_template("login.html", title = "Login", error=error, alert='danger')

@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    if g.username:
        session.pop('username', None)
    return render_template("logout.html", title = "Logout")

@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if not g.username:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if checkUsername(username):
                error = "Please choose a different username."
            else:
                # check password fields
                if password == confirm_password:
                    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
                    db.commit()
                    return redirect(url_for('login')) 
                else:
                    error = "Passwords do not match.  Please try again."               
    return render_template("register.html", title="Register", error=error)

@app.route("/search", methods=['GET', 'POST'])
def search():
    # run only if logged in
    if g.username:
        books = None
        if request.method == 'POST':
            #search for book using provided information
            isbn = request.form['isbn']
            title = request.form['title']
            author = request.form['author']
            if isbn:
                books = db.execute("SELECT * FROM books WHERE isbn iLIKE '%"+isbn+"%' ").fetchall()
                if len(books) == 0:
                    return redirect(url_for('error404'))
            elif title:
                books = db.execute("SELECT * FROM books WHERE title iLIKE '%"+title+"%' ").fetchall()
            elif author:              
                books = db.execute("SELECT * FROM books WHERE author iLIKE '%"+author+"%' ").fetchall()
            else:
                return redirect(url_for('search'))              
            return render_template("results.html", title="Search Results", books=books)
        return render_template("search.html", title="Search")

@app.route("/404")
def error404():
    return render_template("404.html", title = "404 Error")

@app.route("/book", methods=['GET','POST'])
def book():
    error=None
    reviews=None
    goodread_info = None
    already_reviewed = False
    if g.username:
        if request.method == 'GET': 
            # get book id
            session["book_id"] = request.args.get('book_id')
            session["book"] = db.execute("SELECT * FROM books WHERE id = :id", {"id": session["book_id"]}).fetchone()
            # if there are no reviews for this book
            if noReviews(session["book_id"]):
                error = "No Reviews"   
            # if there are reviews for this book
            else:
                reviews = getReviews(session["book_id"])
                isbn = session["book"].isbn
                key = 'aDslZlEv6KMohQRN1wyig'
                res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn, "key": key})
                if res.status_code != 200:
                    raise Exception("ERROR: API request unsuccessful")
                data = res.json()
                goodread_info = {"average": data["books"][0]["average_rating"], "count": data["books"][0]["ratings_count"]}
        elif request.method == 'POST': 
            rating = request.form['rating']
            comment = request.form['comment']
            if checkReviews(session["book_id"], session["id"]):
                addReview((session["id"], session["book_id"], rating, comment))
                return redirect(url_for('search')) 
            else:
                already_reviewed = True          
    return render_template("book.html", title="Book Reviews", book=session["book"], reviews=reviews, error=error, goodread_info=goodread_info, already_reviewed=already_reviewed)

@app.route("/api/<isbn>", methods=['GET'])
def api(isbn):
    book = getBookbyISBN(isbn)
    key = 'aDslZlEv6KMohQRN1wyig'
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn, "key": key})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful")
    data = res.json()
    average = data["books"][0]["average_rating"]
    count = data["books"][0]["ratings_count"]
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": count,
        "average_score": average,
        })




import os

from flask import Flask, session, render_template, request, url_for, redirect, g
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
    return render_template("index.html", title="Home", username=username)

# check if username in database
def user_check_1(username, password):
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
        return False
    else:
        return True

# check if username in database
def user_check_2(username):
    if db.execute("SELECT * FROM users WHERE username = :username ", {"username": username}).rowcount == 0:
        return False
    else:
        return True


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if not g.username:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if user_check_1(username, password):
                session['username'] = request.form['username']
                return redirect(url_for('search'))
            else:
                error = "Invalid credentials."
    return render_template("login.html", title = "Login", error=error, alert='danger')

@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    if g.username:
        session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if not g.username:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if user_check_2(username):
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
        error = None
        if request.method == 'POST':
            isbn = request.form['isbn']
            title = request.form['title']
            author = request.form['author']
            if isbn:
                books = db.execute("SELECT * FROM books WHERE isbn iLIKE '%"+isbn+"%' ").fetchall()
            elif title:
                books = db.execute("SELECT * FROM books WHERE title iLIKE '%"+title+"%' ").fetchall()
            elif author:              
                books = db.execute("SELECT * FROM books WHERE author iLIKE '%"+author+"%' ").fetchall()
            else:
                error = 'You must provide isbn, title, or author.' 
                return redirect(url_for('search', error=error))              
            return render_template("results.html", title="Search Results", books=books)
        return render_template("search.html", title="Search")

def noReviews(book_id):
    return db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).rowcount==0

def getUsername(user_id):
	user = db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id}).fetchone()
	return user.username

def getReviews(book_id):
	review_list = []
	book_reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id})
	for book_review in book_reviews:
            user = getUsername(book_review.user_id)
            rating = book_review.rating
            opinion = book_review.opinion
            review_list.append({"user": user, "rating": rating, "opinion": opinion})
	return review_list

@app.route("/book", methods=['GET','POST'])
def book():
    # book=None
    error=None
    reviews=None
    if g.username:
        if request.method == 'GET':
            # get book id
            book_id = request.args.get('book_id')
            book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
            # if there are no reviews for this book
            if noReviews(book_id):
                error = "No Reviews"   
            # if there are reviews for this book
            else:
                reviews = getReviews(book_id)           
    return render_template("book.html", book=book, reviews=reviews, error=error)

@app.route("/response", methods=['GET'])
def response():
    return render_template("tester.html")

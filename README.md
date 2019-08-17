# Project 1

**Web Programming with Python and JavaScript**

Created routes for `/index`, `/login`, and `/logout` 

Wrote function called `user_check_1` that takes parameters of `username` and `password` to validate whether a user exists. The function checks both the username and password in the database and returns `True` or `False`. (I am currently not hashing passwords.)

Created base template `layout.html` and used template inheritance on all my HTML pages, leaving most of the styling until the end.

Created `/search` route and `search.html` page such that after users login successfully, they are taken to that page.

To add new registrants to my `users` table in my database added `user_check_2` function to determine whether the username exists in the `users` table. Included a password confirmation field and checked it before registering a new user.

The folder `books_import` includes the `books.csv` file and `import.py` - a python script that successfully imported the books data to the `books` table in my database.

The `search.html` page contains a form with four text boxes; if any of the boxes contain content when form is submitted, a `results` page is returned with results if there are any, else it returns an alert `No Results`.  It was tough figuring our how to enter my variable in the SQL Query statement.

When a book title is clicked on the `results` page, it takes you to the `book` page where it gives more detail about the book, shows previous reviews on this book, and provides a form for the current user to add a review.

### Lessons Learned
- use a virtual environment!  I started without one and ended up in a mess.
- a lot of Python tutorials involve using extensions like Flask-WTForms and Flask-Login; since we are not allowed to use ORMs, I found these difficult to use.  I ended up deleting them and using only the extensions originally given in `requirements.txt`
- the better my Google skills, the better off I was, though sometimes I didn't quite know what to ask
- take "baby steps".  Even though I thought I was breaking down my code in smaller pieces, I needed to break things down even smaller.
- GIT BASH worked so much better for me than PowerShell or Command Prompt.

### Recommendations
1.  Emphasize use of virtual environments
2.  Add APIs to the end of Lecture 3 or the beginning of Lecture 4

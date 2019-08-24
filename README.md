# Project 1

**Web Programming with Python and JavaScript**

### `application.py`

**Functions**: `addReview`, `checkLoginInfo`, `checkUsername`, `checkReviews`, `getBookbyISBN`, `getReviews`, `getUserID`, `getUsername`, `noReviews`

**Routes**:

- `/`: Home Page, welcomes user to app
- `/login`:  Login Page, allows users to log in.  If the username is not in the database or the password is incorrect, an error message is shown. Routed to the `search` page.
- `/logout`: Logout page displays when user clicks logout link.
- `/register`:  Register page with registration form is displayed.  For users that are not in the database. Routes to `login` page.
- `/search`:  Search page where user can search for a book by ISBN, title, and/or author.  If a bad ISBN is entered, a 404 error is thrown.  An error message is displayed if there is no user input.  Partial entries are allowed.  Routed to the `results` page.
- `/404`:  Displayed when user enters a bad ISBN in `search` form.
- `/results`: Displays the results of the search as a list. Users can get more information about a book by clicking its title, which routes to the `book` page.
- `/book`: Displays title, author, publication date, and ISBN for the selected book.  Displays the average rating and number of ratings from Goodreads API.  Displays any user reviews from the database.  Displays form for user to submit a review of the book.  If user has alreeady reviewed this title, an error message is displayed. If user has reviewed this title, the review is added to the database and user is routed to the `search` page with a message thanking them for their review.
- `/api/<isbn>`:  Displays JSON object for the book with the user provided ISBN.  Provides title, author, publication date, ISBN, number of reviews in Goodreads, and average rating from Goodreads.

**Templates:**  404.html, book.html, index.html, layout.html, login.html, logout.html, register.html, results.html, search.html

`books_import` folder contains 'books.csv' and `import.py` imported the csv information to the database.
Site was styled with bootstrap 4 and sass.
I did not add any Flask extensions.

### Lessons Learned

- use a virtual environment!  I started without one and ended up in a mess.
- a lot of Python tutorials involve using extensions like Flask-WTForms and Flask-Login; since we are not allowed to use ORMs, I found these difficult to use.  I ended up deleting them and using only the extensions originally given in `requirements.txt`
- the better my Google skills, the better off I was, though sometimes I didn't quite know what to ask
- take "baby steps".  Even though I thought I was breaking down my code in smaller pieces, I needed to break things down even smaller.
- GIT BASH worked so much better for me than PowerShell or Command Prompt.
- it is okay to walk away when needed to regroup and create a new strategy
- this project took me way too long to finish...

### Recommendations

1. Emphasize use of virtual environments
2. Add APIs to the end of Lecture 3 or the beginning of Lecture 4

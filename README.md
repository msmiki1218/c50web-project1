# Project 1

**Web Programming with Python and JavaScript**

I started by creating routes for `/index`, `/login`, and `/logout` so that I can control these functions within sessions.

Once I setup a skeleton of how login and logout would work, I wrote a function called `user_check_1` that takes parameters of username and password to validate whether a user exists. The function checks both the username and password in the database and returns True or False. (I am currently not hashing passwords.)

I created my base template `layout.html` and used template inheritance on all my HTML pages, leaving most of the styling until the end.

I created my `/search` route and html page such that after users login successfully, they are taken to that page.

But before I continue with that, I need to add new registrants to my `users` table in my database. Added a second `user_check_2` function to determine whether just the username exists in the users database. Included a password confirmation field and checked it before registering a new user.

The folder `books_import` includes the `books.csv` file and `import.py` - a python script that successfully imported the books data to the books table in my database.

My `search.html` page went through some changes but I settled on using a form with four text boxes. When the form is completed a `results` page is returned with results if there are any, else it returns an alert "No Results".  It was tough figuring our how to enter my variable in the SQL Query statement.

When a book title is clicked on the `results` page, it takes you to the `book` page where it gives more detail about the book, shows previous reviews on this book, and provides a form for the current user to add a review.

## Lessons Learned
- The importance of using a virtual environment
- Git Bash worked better for me than PowerShell or Command Prompt in Windows10.
- Break the work down into (even) smaller chunks
- It's OKAY to WALK AWAY
- avoid adding too many extensions to Flask; I installed and uninstalled too many

## Recommendations
1.  The information about APIs should be a the end of week 3 or the beginning of week 4.  Learning all that information about ORMs before then was not relevant to the project.
2.  I wish there were PDF versions of the lecture notes.  There were a few misspellings and issues with quotation marks.  I suppose I could have printed out the web page but I wanted a digital copy.  I ended up creating one myself.


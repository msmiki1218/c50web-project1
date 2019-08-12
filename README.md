# Project 1

Web Programming with Python and JavaScript

I started by creating routes for index, login, and logout so that I can control these functions within sessions.

Once I setup a skeleton of how login and logout would work, I wrote a function called 'user_check' that takes parameters of username and password to validate whether a user exists. The function checks both the username and password in the database and returns True or False. (I am currently not hashing passwords.)

I created my base template "layout.html" and used template inheritance on all my HTML pages, leaving most of the styling until the end.

I created my 'search' route and html page such that after users login successfully, they are taken to that page.

But before I continue with that, I need to add new registrants to my 'users' table in my database. Added a second 'user_check' function to determine whether just the username exists in the users database. Included a password confirmation field and checked it before registering a new user.

The folder 'books_import' includes the 'books.csv' file and 'import.py' - a python script that successfully imported the books data to the books table in my database.

My 'search.html' page went through some changes but I settled on using a form with four text boxes. When the form is completed a 'results' page is returned with results if there are any, else it returns an alert "No Results".  It was tough figuring our how to enter my variable in the SQL Query statement.


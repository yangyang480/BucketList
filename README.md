# BUCKETLIST
## Video Demo:  <https://youtu.be/wmNV4nG-i3U>
## Description:
### CS50
>This was my final project for conclude the CS50 Introduction to Computer Sciense course.

>CS, python, flask, flask web framework, web development, CS50

### Techs
I used Flask web framework based in Python and SQL for database

### Explaining the project
My final project is a website that allow the user register login and read, create, update, delete on the bucket lists. This website is for track bucket list that user created. And the user also able to delete their account if they want to.

### Explaining the database
I used sql sqlite3 for my database. The schema named bucketList.db. And I have two tables.

- One is users table, where I put id, username, hash (for password) and dob, notice that id must be a primary key here.

- Two is lists table, where I put id, user_id, title, date, location, description, status. notice that user_id is the FK here.

### Files I have:
In this project I have 3 main folders.

- One is static folder where contains the picture that I am using in the project and also the css file that appled for the whole project.

- Two is the python folder where contains two python file: app.py and helper.py. Then main function is in app file. The validation method is in helper file.

- Three is templates folder where contains 8 html files as showing below:
#### 1 index.html:
Index page is when people land on the application. Is the home page of this application.
#### 2 layout.html:
Layout page is the navigation bar show or hide depending on if user has logged in or not. 
#### 3 register.html: 
Register html file is a page that where user can register, which contains 4 inputs that user must fill up. 
#### 4 login.html:
Login page is where user can log in. It contain username and password input.
#### 5 create.html:
Create page is where user can create the bucket list with title, due date, location and detail.
#### 6 myLists.html:
Mylists page is where user can see all the bucket lists that they have created. User can also edit and delete the bucket list by clicking the button in create.html page. User can create another bucket list through here.
#### 7 profile.html:
Profile page is where user can see their personal info and how many lists they created, how many lists are in progress, how many lists that they completed. They can also delete their account in this page.
#### 8 apology.html:
When user register and login, they will be vaildation check, if the user failed the vaildation, then this page will show up. The porpuse of this page is to remind user what is the correct format. 

 



# CS50W Final Project - YourTalent

- [CS50W Final Project - YourTalent](#cs50w-final-project---yourtalent)
    - [introduction](#introduction)
    - [Distinctiveness and Complexity](#distinctiveness-and-complexity)
    - [Models](#models)
    - [Routes](#routes)
        - [Index](#index)
        - [Login](#login-login)
        - [Register](#register-register)
        - [Logout](#logout-logout)
        - [Home](#home-home)
        - [Authenticate](#authenticate-authenticate)
        - [Authenticate_api](#authenticateapi-authenticateapi)
        - [Viewcontent](#viewcontent-viewcontent)
        - [Mycontents](#mycontents-mycontents)
        - [Interest](#interest-interest)
        - [API_Interest](#apiinterest-apiinterest)
        - [API_Uninterest](#apiuninterest-apiinterest)
        - [API_Notif](#apinotif-apinotif)
        - [API_Delete](#apidelete-apidelete)
    - [Summary For The Created Files](#summary-for-the-created-files)
    - [How to run the application](#how-to-run-the-application)
    - [Important Note](#important-note)

## Introduction

My inspiration of this project based from a dancing film. And i have an idea from that to make a platform where there is a recruiter that can recruit a content creator.

The website can get a file on an image form or mp3 for music. And youtube unlisted or public url for the dancing and programming part of the talent.

My web project was built using Django, Javascript, Bootstrap, HTML, and CSS.

[Back to Index](#cs50w-final-project---yourtalent)

## Distinctiveness and Complexity

According to the specification, it should satisfy this requirement below:

> Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.

I believe that my final project has already satisfy the requirement because:

1. My project is based on original idea and it's distinct from the projects from CS50 itself.
2. The system will automatically send an email to the content creator and recruiter after being recruited. recruiter and content creator can't communicate within the app.
3. The website uses file processing that take a file from the user that choose content creator role. The content is free to look for the recruiter.
4. The registration uses authentication so that a new user have to input the authentication code before proceed more futher.
5. There is some simple notification after content creator being recruited by recruiter.

>Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.

My final project was built using Django. It has 7 models on the back-end and 6 JavaScript for the front-end.

>Your web application must be mobile-responsive.

My final project is mobile responsive in every page. It uses media query in CSS and Bootstrap to gain the responsiveness.

[Back to Index](#cs50w-final-project---yourtalent)

## Models

There are 7 models in YourTalent.

1. `User` - It uses `AbstractUser` to store all the user information.
2. `Authentication` - Store the authentication code and it's boolean value, the role of a user, and foreign key for the user.
3. `Novidpart` - Store the non-video content, it's necessary information, and a function to delete the file at the file directory.
4. `Vidpart` - Store the video content of youtube url, it's necessary information, and a function to delete the thumbnail at the file directory.
5. `Notifications` - Store the foreign key of recruiter and contentcreator, and it's content that recruited by recruiter.
6. `Interestnovidpart` - Store the category and foreign key of the content and the recruiter for the non-video part.
7. `Interestvidpart` - Store the category and foreign key of the content and the recruiter for the video part.

## Routes

### Index `/`

The page contains short description of YourTalent and to contact YourTalent.

### Login `/login`

Page that contain a form so that the user can log in to.

### Register `/register`

Page that contain a form of username, email, password, confirmation, and role so that user can register to yourtalent.

### Logout `/logout`

If the user click logout at the navbar user will be redirected to the index page.

### Home `/home`

Page that contain based on the user that role taken, if recruiter, user can see the content based on the category and if the content creator, user can see form to upload their content.

### Authenticate `/authenticate`

Page to authenticate user, user have to input the authentication code given to their registered gmail.

### Authenticate_api `/authenticate_api`

A route to regenerate a new authentication code if the user click to resend the authentication code after waiting 30 seconds.

### Viewcontent `/viewcontent`

Page so that the user can see their or others content. If user is recruiter, user can see the button to interest and recruit. If the user content creator, user can see delete button to delete the content.

### Mycontents `/mycontents`

Page to see the content creator own content and able to delete it from the mycontent if the content is music.

### Interest `/interest`

Page so that the recruiter can see the content that they have interest on.

### API_Interest `/API_Interest`

a route to add interest for the recruiter into the database.

### API_Uninterest `/API_Interest`

a route to remove interest for the recruiter at the database.

### API_Notif `/API_Notif`

a route to create a notif for the content creator if the recruiter recruit the content creator from the content.

### API_Delete `API_Delete`

a route to delete a content from the database that the content creator decided to delete.

[Back to Index](#cs50w-final-project---yourtalent)

## Summary For The Created Files

Summary for the files i created:

- `YourTalent` - Main directory for the final project.
    - `static/YourTalent` - Directory to store the static files.
        - `Authenticate.js` - Giving the information to resend the authentication code to the `authenticate_api`.
        - `home.js` - Dynamically create the form for the content creator, On change dropdown for the content based on the category for recruiter, generate the notification, interest and uninterest content and dynamically change the button.
        - `interest.js` - Interest and uninterest content and change the button dynamically.
        - `mycontents.js` - On change dropdown for the content based on the category for content creator, generate the notification, and giving the information to `API_Delete`.
        - `register.js` - After user submit data hide the form and show the loading GIF.
        - `view.js` - Interest and uniterest content for recruiter and give information to `API_Delete`.
        - `styles.css` - Consists of media query, 
    - `templates/YourTalent` - Directory to store the html files.
        - `Authenticate.html` - Template for authentication part.
        - `error.html` - Template to display some error message.
        - `home.html` - Template to display home consisting of contents for content creator and form for content creator.
        - `index.html` - Template to display short description and contact of YourTalent.
        - `interest.html` - Template to display content of interest from recruiter.
        - `layout.html` - Template consisting of basic that all the html used.
        - `login.html` - Template for user to login.
        - `mycontents.html` - Template for the content creator that consist of the content of content creator itself.
        - `register.html` - Template for user to register new account.
        - `success.html` - Template to notify that some user has successfully do some action.
        - `view.html` - Template to display all the content from the content creator except for the music. Music will be displayed at the `home.html`.
    - `admin.py` - Consists of the model that has been registered so that it can be used in the Admin page.
    - `models.py` - Consists of class to create a table in the database.
    - `urls.py` - Consists of the url in the web app.
    - `views.py` - Consists of the logic for the web app to work.
- `media` - Main directory to keep the uploaded file.
    - `Novidpart` - consisting of the media that doesn't use youtube URL.
    - `thumbnail` - consisiting of the media of image that uses youtue URL.
- `FinalProject` - Project directory.
    - `settings.py` - the setting that i add is for the location of media and configuration for the gmail.

[Back to Index](#cs50w-final-project---yourtalent)

## How to run the application

1. Copy or download the current final project.
2. Make sure that django has already been installed.
3. No requirement.txt because the imported library is already built-in.
4. Make sure the table is already migrated:
     ```python
   python manage.py makemigrations YourTalent
   python manage.py migrate
   ```
5. Run the server:
    ```python
   python manage.py runserver
   ``` 

[Back to Index](#cs50w-final-project---yourtalent)

## Important Note

The Web app has two role of content creator and recruiter but for now all the user can be recruiter. So, it's not that perfect yet and it will have some advance rule and user agreement so that not all the user can be recruiter but for now because it's not being deployed yet and the functionality is still the same so i will not add it yet.

[Back to Index](#cs50w-final-project---yourtalent)
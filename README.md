## FOODIE

- A web application where users can publish recipes
and favorite meals. Published content is called a foodie

## Sample screenshot

![Sample screenshot](https://github.com/KNehe/foodie/blob/develop/static/images/screenshot2.PNG?raw=true)

## Technologies used

- Python3
- Django
- HTML
- CSS
- Javascript

## Setting up

- Clone this repository
- `cd` to the project root directory
- Create and activate your `virtualenv`
- Run `pip install -r requirements.txt` in your shell
- Create `.env` in the same directory as `settings.py` . Add it to your `.gitignore`
- Add the following variables to `env`. The second to the last are for sending emails using [sendgrid](https://sendgrid.com/)(used in password reset and on registration). 
The first is your django secret key
```
SECRET_KEY=
SENDGRID_API_KEY=
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=
FROM_EMAIL=
```
- And finally `py manage.py runserver`

## Features

- User registration and login using an email and password
- Send email on registration
- Users can comment on a published foodie
- Upvote or downvote depending on the kind of content
- Editing one's profile
- Upload a profile picture
- View the most popular foodies
- Recent foodies of currently logged in users displayed
- Users can delete their accounts
- Users can delete a foodie they created
- view profile
- Logout
- View number of upvotes, downvotes and comments
- Delete comments


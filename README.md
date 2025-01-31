# Unnamed Python Chat Application
Yet another [Catppuccin](https://catppuccin.com/)-themed chat application (think Discord clone) made in Python, with Django and Websockets, supporting asynchronous connections to multiple users, private user created servers, and saving messages. This is a full rewrite of one of my old projects, which supported display names, channels, private servers, kicks, mutes, and more, so I hope that this has the same kind of potential without the horrible code.

## Features
+ User Authentication
+ Private servers
+ Users can make their own servers
+ Messages are saved local to servers
+ User registration page
+ New homepage

## Server commands
| Command     | Required Privilege Level | Action             |
|-------------|--------------------------|--------------------|
| `/transown` | Owner | Transfers ownership |
| `/promote`  | Administrator | Promote a user to one above their current privilege level. Does not work if that would result in being an owner. |
| `/demote`   | Administrator            | The opposite of above.|
| `/admin`    | Administrator | Set a user's privilege to Administrator. |
| `/mod`      | Administrator | Set a user's privilege to Moderator. |


## Running
To run, clone the repository, then set up a `venv` virtual environment and activate it. Next, you can install the dependencies with `pip install -r requirements.txt`, `cd` into `chatapp/`, run `python manage.py migrate` to create the database and run `python manage.py runserver` to run the local development server on [port 8000](http://localhost:8000).

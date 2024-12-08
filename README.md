# Unnamed Python Chat Application
Yet another [catppuccin](https://catppuccin.com/)-themed chat application made in Python, with Django and Websockets, supporting multiple users asynchronously. This is a full rewrite of one of my old projects, which supported display names, channels, private servers, kicks, mutes, and more, so I hope that this has the same kind of potential without the horrible code.

## Running
To run, clone the repository, then set up a `venv` virtual environment and activate it. Next, you can install the dependencies with `pip install -r requirements.txt`, `cd` into `chatapp/`, run `python manage.py migrate` to create the database and run `python manage.py runserver` to run the local development server on [port 8000](http://localhost:8000).

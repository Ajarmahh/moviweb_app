from flask import Flask
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)

#  Integrating DataManager in the Flask app
data_manager = SQLiteDataManager('moviwebapp.db')


@app.route('/')
def home():
    return 'Welcome to the MovieApp'


@app.route('/users')
def get_users():
    users = data_manager.get_all_users()
    return str(users)  # for now this will return string users, will be changed later on


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    return data_manager.get_user_movies(user_id)


@app.route('/add_user')
def add_user():
    # This route will present a form that enables the addition of a new user to our MovieWeb App.
    pass  # placeholder for now until i have the html file for adding a user


@app.route('/users/<user_id>/add_movie')
def add_movie():
    pass  # placeholder for now until i have the html file to add a movie


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie():
    pass  # waiting for the html file


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    pass  # waiting for the html file


if __name__ == '__main__':
    app.run(debug=True)

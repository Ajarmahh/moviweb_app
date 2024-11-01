from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from datetime import datetime

app = Flask(__name__)

#  Integrating DataManager in the Flask app
data_manager = SQLiteDataManager('moviwebapp.db')

CURRENT_YEAR = datetime.now().year


@app.route('/')
def home():
    current_year = CURRENT_YEAR
    return render_template('home.html', current_year=CURRENT_YEAR)


@app.route('/users')
def get_users():
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        app.logger.error(f"Error retrieving users: {e}")
        return render_template('error.html', error="Could not load users list."), 500


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    try:
        user_movies = data_manager.get_user_movies(user_id)
        user_name = data_manager.get_user_name(user_id)
        return render_template(
            'user_movies.html', user_movies=user_movies,
            user_name=user_name, user_id=user_id
        )
    except Exception as e:
        app.logger.error(f"Error fetching movies for user {user_id}: {e}")
        return render_template('error.html', error="Could not load user movies."), 500


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            name = request.form.get('name')
            data_manager.add_user(name, email)
            return redirect(url_for('get_users'))
        except Exception as e:
            app.logger.error(f"Error adding user: {e}")
            return render_template('error.html', error="Could not add user."), 500
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['POST', 'GET'])
def add_movie(user_id):
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            rating = request.form.get('rating')
            director = request.form.get('director')
            year = request.form.get('year')

            data_manager.add_movie(user_id=user_id, title=title, rating=rating, director=director, year=year)

            return redirect(url_for('get_user_movies', user_id=user_id))
        except Exception as e:
            app.logger.error(f"Error adding movie for user {user_id}: {e}")
            return render_template('error.html', error="Could not add movie."), 500

    return render_template('add_movie.html', user_id=user_id, current_year=CURRENT_YEAR)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['POST', 'GET'])
def update_movie(movie_id, user_id):
    try:
        movie = data_manager.get_movie(movie_id)
    except Exception as e:
        app.logger.error(f"Error fetching movie {movie_id} for update: {e}")
        return render_template('error.html', error="Movie not found."), 404

    if request.method == 'POST':
        try:
            title = request.form.get('title')
            rating = request.form.get('rating')
            director = request.form.get('director')
            year = request.form.get('year')

            # Call the update_movie method to save the changes
            data_manager.update_movie(movie_id, title, rating, director, year)

            return redirect(url_for('get_user_movies', user_id=user_id))
        except Exception as e:
            app.logger.error(f"Error updating movie {movie_id}: {e}")
            return render_template('error.html', error="Could not update movie."), 500

    return render_template('update_movie.html', movie=movie, user_id=user_id, current_year=CURRENT_YEAR)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)
        return redirect(url_for('get_user_movies', user_id=user_id))
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id} for user {user_id}: {e}")
        return render_template('error.html', error="Could not delete movie."), 500


# Catch 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', error=error), 404


# Catch server side errors
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', error=error), 500


# Catch all the other exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}")
    return render_template("errors/error.html", error="An unexpected error occurred.", exception=e), 500


if __name__ == '__main__':
    app.run(debug=True)

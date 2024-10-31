from flask import Flask, render_template, request, redirect, url_for
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
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name(user_id)
    return render_template(
        'user_movies.html', user_movies=user_movies,
        user_name=user_name, user_id=user_id
    )


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        data_manager.add_user(name, email)
        return redirect(url_for('get_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['POST', 'GET'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form.get('title')
        rating = request.form.get('rating')
        director = request.form.get('director')
        year = request.form.get('year')

        data_manager.add_movie(user_id=user_id, title=title, rating=rating, director=director, year=year)

        return redirect(url_for('get_user_movies', user_id=user_id))

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['POST', 'GET'])
def update_movie(movie_id, user_id):
    movie = data_manager.get_movie(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')

        try:
            rating = request.form.get('rating')
        except ValueError:
            return "Rating must be a number.", 400  # Handle error for invalid rating

        director = request.form.get('director')
        year = request.form.get('year')

        # Call the update_movie method to save the changes
        data_manager.update_movie(movie_id, title, rating, director, year)

        return redirect(url_for('get_user_movies', user_id=user_id))

    return render_template('update_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)

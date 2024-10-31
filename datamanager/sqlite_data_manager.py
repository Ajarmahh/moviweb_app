from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datamanager.data_manager_interface import DataManagerInterface
from .data_models import Base, Movie, User


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        # Initialize the SQLite database engine
        self.engine = create_engine(f'sqlite:///{db_file_name}')

        # Create a new session maker bound to the engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Create all tables defined in the Base class
        Base.metadata.create_all(self.engine)

    def get_all_users(self):
        return self.session.query(User.id, User.name).all()

    def get_user_name(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.name

    def get_user_movies(self, user_id):
        return self.session.query(Movie).filter_by(user_id=user_id).all()

    def add_user(self, name, email):
        #  Add a new user to the Database
        new_user = User(name=name, email=email)
        self.session.add(new_user)
        self.session.commit()

    def add_movie(self, title, rating, director, year, user_id):
        new_movie = Movie(title=title, rating=rating, director=director, year=year, user_id=user_id)
        self.session.add(new_movie)
        self.session.commit()

    def update_movie(self, movie_id, title, rating, director, year):
        existing_movie = self.session.query(Movie).get(movie_id)
        if existing_movie:
            existing_movie.title = title
            existing_movie.rating = rating
            existing_movie.director = director
            existing_movie.year = year
            self.session.commit()

    def get_movie(self, movie_id):
        return self.session.query(Movie).get(movie_id)

    def delete_movie(self, movie_id):
        movie = self.session.query(Movie).get(movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datamanager.data_manager_interface import DataManagerInterface
from data_models import Base, Movie, User


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
        return list(self.session.query(User.name).all())

    def get_user_movies(self, user_id):
        return list(self.session.query(Movie.title).filter(Movie.user_id == user_id).all())

    def add_user(self, user):
        #  Add a new user to the Database
        self.session.add(user)
        self.session.commit()

    def add_movie(self, movie):
        self.session.add(movie)
        self.session.commit()

    def update_movie(self, movie_id, updated_movie):
        existing_movie = self.session.query(Movie).get(movie_id)
        if existing_movie:
            existing_movie.title = updated_movie.title
            existing_movie.rating = updated_movie.rating
            existing_movie.director = updated_movie.director
            existing_movie.year = updated_movie.year
            self.session.commit()

    def delete_movie(self, movie_id):
        movie = self.session.query(Movie).get(movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()

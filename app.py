import os
from flask import Flask, jsonify, request
from models import setup_db, Actor, Movie
from flask_cors import CORS


def format_data(d):
    return [data.format() for data in d]


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors')
    def get_actors():
        query = Actor.query.all()

        return jsonify({
            'actors': format_data(query),
            'success': True
        })

    @app.route('/movies')
    def get_movies():
        query = Movie.query.all()

        return jsonify({
            'movies': format_data(query),
            'success': True
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        actor.delete()

        return jsonify({
            'id': actor.id,
            'success': True
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        movie.delete()

        return jsonify({
            'id': movie.id,
            'success': True
        })
    
    @app.route('/actors')
    def add_actor():
        req = request.get_json()
        actor = Actor(name=req['name'], age=req['age'], gender=req['gender'])
        actor.insert()

        return jsonify({
            'id': actor.id,
            'success': True
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

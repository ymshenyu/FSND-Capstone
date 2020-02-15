import os
from flask import Flask, jsonify, request, abort
from models import setup_db, Actor, Movie
from flask_cors import CORS
from auth import require_permission, AuthError


def format_data(d):
    return [data.format() for data in d]


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Actors endpoints
    @app.route('/actors')
    @require_permission('read:information')
    def get_actors(payload):
        query = Actor.query.all()

        return jsonify({
            'actors': format_data(query),
            'success': True
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @require_permission('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        try:
            actor.delete()
        except Exception:
            abort(404)

        return jsonify({
            'id': actor.id,
            'success': True
        })

    @app.route('/actors', methods=['POST'])
    @require_permission('create:actor')
    def add_actor(payload):
        req = request.get_json()
        actor = Actor(name=req['name'], age=req['age'], gender=req['gender'])
        try:
            actor.insert()
        except Exception:
            abort(422)

        return jsonify({
            'id': actor.id,
            'success': True
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @require_permission('update:actor')
    def update_actors(payload, actor_id):
        req = request.get_json()
        query = Actor.query.filter(Actor.id == actor_id).one_or_none()
        actor = query(name=req['name'], age=req['age'], gender=req['gender'])
        try:
            actor.update()
        except Exception:
            abort(422)

        return jsonify({
            'id': actor.id,
            'success': True
        })

    # Movies endpoints
    @app.route('/movies')
    @require_permission('read:information')
    def get_movies(payload):
        query = Movie.query.all()

        return jsonify({
            'movies': format_data(query),
            'success': True
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @require_permission('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        try:
            movie.delete()
        except Exception:
            abort(404)

        return jsonify({
            'id': movie.id,
            'success': True
        })

    @app.route('/movies', methods=['POST'])
    @require_permission('create:movie')
    def add_movie(payload):
        req = request.get_json()
        movie = Movie(title=req['title'], release_date=req['release_date'])
        try:
            movie.insert()
        except Exception:
            abort(422)

        return jsonify({
            'id': movie.id,
            'success': True
        })

    @app.route('/movies/int:movie_id', methods=['PATCH'])
    @require_permission('update:movie')
    def update_movie(payload, movie_id):
        req = request.get_json()
        query = Movie.query.filter(Movie.id == movie_id).one_or_none()
        movie = query(title=req['title'], release_date=req['release_date'])
        try:
            movie.update()
        except Exception:
            abort(422)

        return jsonify({
            'id': movie.id,
            'success': True
        })

    # Error handler
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'code': 404,
            'description': 'resource not found',
            'success': False
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'code': 422,
            'description': 'unprocessable',
            'success': False
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'code': 500,
            'description': 'Internal Server Error',
            'success': False
        }), 500
    
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code
    return app


app = create_app()

if __name__ == '__main__':
    app.run()

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

# Casting Agency test case


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432',
            self.database_name
        )
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Begin actors endpoints test

    # Get actors information without token

    def test1_get_actors_without_valid_authorization_token(self):
        res = self.client.get('/actors')
        self.assertEqual(res.status_code, 401)

    # Get actors information with casting assistant token

    def test2_get_actors_with_valid_authorization_token(self):
        res = self.client.get(
            '/actors',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    # Add actor without permission

    def test3_add_a_actor_without_valid_authorization_token(self):
        res = self.client.post(
            '/actors',
            json={
                "name": "Alice",
                "age": 25,
                "gender": "Female"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 403)

    # Add actor with permission

    def test4_add_a_actor_with_valid_authorization_token(self):
        res = self.client.post(
            '/actors',
            json={
                "name": "Alice",
                "age": 25,
                "gender": "Female"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Unprocessable entity

    def test5_unprocessable(self):
        res = self.client.post(
            '/actors',
            json={
                "name": "Alice",
                "age": "string",
                "gender": 1
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    # Update actor information without permission

    def test6_update_a_actor_without_valid_authorization_token(self):
        res = self.client.patch(
            '/actors/1',
            json={
                "age": 26,
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 403)

    # Update actor with permission

    def test7_update_a_actor_with_valid_authorization_token(self):
        res = self.client.patch(
            '/actors/1',
            json={
                "age": 26,
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Delete actor without permission

    def test8_delete_a_actor_without_valid_authorization_token(self):
        res = self.client.delete(
            '/actors/1',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 403)

    # Delete actor with permission

    def test9_delete_a_actor_with_valid_authorization_token(self):
        res = self.client.delete(
            '/actors/1',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Begin movies endpoints test

    # Get movies information without permission

    def test10_get_movies_without_valid_authorization_token(self):
        res = self.client.get('/movies')
        self.assertEqual(res.status_code, 401)

    # Get movies information with permission

    def test11_get_movies_with_valid_authorization_token(self):
        res = self.client.get(
            '/movies',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    # Add movies without permission

    def test12_add_a_movie_without_valid_authorization_token(self):
        res = self.client.post(
            '/movies',
            json={
                "title": "Avengers: Endgame",
                "release_date": "2019-04-23"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    # Add movies with permission

    def test13_add_a_movie_with_valid_authorization_token(self):
        res = self.client.post(
            '/movies',
            json={
                "title": "Avengers: Endgame",
                "release_date": "2019-04-23"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('EXECUTIVE_PRODUCER')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Update movies information without permission

    def test14_update_a_movie_without_valid_authorization_token(self):
        res = self.client.patch(
            '/movies/1',
            json={
                "release_date": "2019-04-24"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 403)

    # Update movies with permisson

    def test15_update_a_movie_with_valid_authorization_token(self):
        res = self.client.patch(
            '/movies/1',
            json={
                "release_date": "2019-04-24"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    # Delete movies without permission

    def test16_delete_a_movie_without_valid_authorization_token(self):
        res = self.client.delete(
            '/movies/1',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}"
            }
        )
        self.assertEqual(res.status_code, 403)

    # Delete movies with permission

    def test17_delete_a_movie_with_valid_authorization_token(self):
        res = self.client.delete(
            '/movies/1',
            headers={
                "Authorization": f"Bearer {os.getenv('EXECUTIVE_PRODUCER')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()

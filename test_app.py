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
        self.database_name = "capstone_test"
        self.database_path = f"postgresql://localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Begin actors endpoints test

    # Get actors information without token

    def test_get_actors_without_token(self):
        res = self.client.get('/actors')
        self.assertEqual(res.status_code, 401)

    # Get actors information with casting assistant token

    def test_get_actors_with_token(self):
        res = self.client.get(
            '/actors',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    # Add actor without permission

    def test_add_actor_without_permission(self):
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

    def test_add_actor_with_permission(self):
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

    def test_unprocessable_entity(self):
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

    # Delete actor with with casting assistant token

    def test_delete_actor_without_permission(self):
        res = self.client.delete(
            '/actors/1',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT')}"
            }
        )
        self.assertEqual(res.status_code, 403)

    # Delete actor with casting director token

    def test_delete_actor_with_permission(self):
        res = self.client.delete(
            '/actors/1',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()

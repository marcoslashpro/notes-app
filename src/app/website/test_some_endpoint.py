import unittest

from app.main import create_app


class TestEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_endpoint(client):
        response = client.post('/testing-endpoint', json={'Needed': 'Data'})
        return response

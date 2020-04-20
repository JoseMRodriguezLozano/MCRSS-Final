import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data

class TestCreateVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_create_pbp_valid_event(self):
        response = self.client.delete('/pbp',data=json.dumps(data["valid_id"]),content_type='application/json', follow_redirects=True)
        expected_msg = "PBP Sequence removed."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

if __name__ == "__main__":
    unittest.main()
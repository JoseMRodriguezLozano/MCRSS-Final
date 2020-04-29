import unittest
import json
from main import app
from tests.pbp_tests.opp_roster.opp_roster_data import data


class TestAddOppRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_opp_roster_add_valid1(self):
        response = self.client.post('/pbp/Voleibol/roster', data=json.dumps(
            data["valid_data1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: La información mas reciente del atleta se agregado al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

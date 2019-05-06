import json
import unittest

import psycopg2 as sql

import app

get_place_url = "http://localhost:5000/get_place"
post_loc_url = "http://localhost:5000/post_location"


class BasicUnitTests(unittest.TestCase):
    def setUp(self):
        app.app.config["TESTING"] = True
        self.conn = sql.connect(host="localhost", database="test_db",
                                user="arun", password="root", port="5432")
        self.c = self.conn.cursor()
        self.app = app.app.test_client()

    def test_get_place(self):
        """
        ** Enter Coordinates to test if it lies inside polygon given in
            database
        :return:
        """
        with app.app.app_context():
            req_data = json.dumps({})
            res = self.app.post(post_loc_url, json=req_data)

            self.assertEqual(400, res.status_code)

    def tearDown(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    unittest.main()

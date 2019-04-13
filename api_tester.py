import json
import unittest as tester
from json import dumps as jsonify

import requests as req

post_loc_url = "http://localhost:5000/post_location"
get_postgres_url = "http://localhost:5000/get_using_postgres"
get_self_url = "http://localhost:5000/get_using_self"
get_place_url = "http://localhost:5000/get_place"


class Test(tester.TestCase):

    def test_if_posted(self):
        """
        ** Can be run only once as data is added after running once
        ** which makes it fail next time

        :return:
        """
        reqdata = {"lat": 17.726675,
                   "long": 83.312320,
                   "address": "CBM Compound",
                   "state": "Andhra Pradesh",
                   "pin": 530003
                   }

        res = req.post(post_loc_url, json=jsonify(reqdata))
        print("RES", res.text)
        self.assertEqual("200", json.loads(res.text)["Status"])

    def test_bad_request(self):
        """
        ** Bad Request Detection
        :return:
        """
        req_data = {}
        res = req.post(post_loc_url, json=req_data)
        print("RES", res.text)
        self.assertEqual("400", json.loads(res.text)["Status"])

    def test_get_postgres(self):
        """
        ** Error in the two functions
        :return:
        """
        reqdata = jsonify({"lat": 28.55,
                           "long": 77.2667
                           })
        res1 = req.post(get_postgres_url, json=reqdata)
        res2 = req.post(get_self_url, json=reqdata)
        # self.assertEqual(res1["Status"], res2["Status"])
        print("RESULTS!!", res1.text, res2.text)
        self.assertEqual(json.loads(res1.text)["Nearby Locations"], json.loads(res2.text)["Nearby Locations"])

    def test_get_place(self):
        """
        ** Enter Coordinates to test if it lies inside polygon given in
            database
        :return:
        """
        req_data = jsonify({"lat": 28.615551,
                            "long": 77.224091})
        res = req.post(get_place_url, json=req_data)
        self.assertEqual("200", json.loads(res.text)["Status"])


if __name__ == '__main__':
    tester.main()

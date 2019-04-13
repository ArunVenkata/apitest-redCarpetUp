import json

import psycopg2 as sql
from flask import Flask, jsonify, request

from earthdist import earth_distance

app = Flask(__name__)
conn = sql.connect(host="localhost", database="in-data",
                   user="postgres", password="root", port="5555")

c = conn.cursor()

bad_req = {"Status": "400", "Msg": "Check request data Properly!"}
frbd_req = {"Status": "403", "Msg": "Forbidden"}


@app.route('/post_location', methods=["POST"])
def post_loc():
    if request.json:

        req_data = json.loads(request.json)
        try:
            # check if "address" exists
            print(req_data["address"])

            # check if "pin" exists
            print(req_data["pin"])

            # check if "lat" exists
            print(req_data["lat"])

            # check if "long" exists
            print(req_data["long"])

            # check if "pin" exists
            print(req_data["state"])

        except KeyError:
            return jsonify(bad_req)

        # get all latitudes and longitudes
        c.execute("SELECT latitude,longitude from indata WHERE latitude!='' or longitude!='';")
        ll = list(set(c.fetchall()))
        close_locs = []

        # check if given ones are close enough to any
        for lat1, long1 in ll:

            dist = earth_distance(float(lat1), float(long1), float(req_data["lat"]), float(req_data["long"]))

            # Assumption - If distance is less than 500 meters
            # If close, Get location of close vals
            if dist <= 0.5:
                c.execute("select place_name,admin_name1 from indata where latitude=%s and longitude=%s",
                          (lat1, long1,))
                close_locs = c.fetchall()

        c.execute("SELECT ID,key FROM indata ORDER BY ID DESC LIMIT 2")
        res = c.fetchall()

        # get next Id
        next_num = int(res[0][0]) + 1

        # get next key
        next_key = "IN/" + str(req_data["pin"])

        # if the same pin code exists then dont allow to add
        if next_key == res[0][1]:
            return jsonify(frbd_req)

        # Add to db
        c.execute("INSERT INTO indata VALUES(%s, %s, %s, %s, %s, %s, %s)",
                  (next_num, next_key, req_data["address"], req_data["state"],
                   req_data["lat"], req_data["long"], ""))

        conn.commit()

        return jsonify({"Status": "200",
                        "Locations": close_locs}) if close_locs else jsonify({"Status": "200"})

    else:
        return jsonify(bad_req)


@app.route('/<path:dummy>')
def fallback(dummy):
    return jsonify({"Error 404": dummy + " is an INVALID URL"})


if __name__ == '__main__':
    app.run()

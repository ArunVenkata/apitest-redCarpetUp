import math as math_stl

import psycopg2 as sql


def earth_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float
    """
    if not (-90.0 <= lat1 <= 90):
        raise ValueError('lat1={:2.2f}, but must be in [-90,+90]'.format(lat1))
    if not (-90.0 <= lat2 <= 90):
        raise ValueError('lat2={:2.2f}, but must be in [-90,+90]'.format(lat1))
    if not (-180.0 <= lon1 <= 180):
        raise ValueError('lon1={:2.2f}, but must be in [-180,+180]'
                         .format(lat1))
    if not (-180.0 <= lon2 <= 180):
        raise ValueError('lon1={:2.2f}, but must be in [-180,+180]'
                         .format(lat1))
    radius = 6371  # km

    dlat = math_stl.radians(lat2 - lat1)
    dlon = math_stl.radians(lon2 - lon1)
    a = (math_stl.sin(dlat / 2) * math_stl.sin(dlat / 2) +
         math_stl.cos(math_stl.radians(lat1)) *
         math_stl.cos(math_stl.radians(lat2)) *
         math_stl.sin(dlon / 2) * math_stl.sin(dlon / 2))
    c = 2 * math_stl.atan2(math_stl.sqrt(a), math_stl.sqrt(1 - a))
    d = radius * c

    return d


if __name__ == '__main__':
    conn = sql.connect(host="localhost", database="in-data",
                       user="postgres", password="root", port="5555")

    c = conn.cursor()

    c.execute("CREATE EXTENSION IF NOT EXISTS cube CASCADE;")
    c.execute("CREATE EXTENSION  IF NOT EXISTS earthdistance CASCADE;")

    # c.execute("""SELECT (point(17.726675,83.312320) <@> point(17.727365, 83.314305))""")

    # c.execute("""CREATE FUNCTION dist(lat1 float, lon1 float, lat2 float, lon2 float) RETURNS integer AS $$
    # BEGIN
    # RETURN point(lat1,lon1) <@> point(lat2, lon2);
    # END; $$
    # LANGUAGE PLPGSQL;
    # """)
    # conn.commit()
    # c.execute("SELECT key, latitude, longitude from indata WHERE dist(1,2,45.12, 71.12)<=5;")
    print(c.fetchall()[0][0])

    conn.close()

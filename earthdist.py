import math as math_stl


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

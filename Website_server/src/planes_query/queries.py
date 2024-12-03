from django.db import connection


def fetch_planes_in_bbox(sw_lat, sw_lng, ne_lat, ne_lng):
    """
    Query the database for planes within the bounding box.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT latitude, longitude, geo_altitude, call_sign
            FROM plane
            WHERE latitude BETWEEN %s AND %s
              AND longitude BETWEEN %s AND %s
        """, [sw_lat, ne_lat, sw_lng, ne_lng])

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        planes = [
            {'lat': row[0], 'lon': row[1], 'altitude': row[2], 'call_sign': row[3]}
            for row in rows
        ]
        print(planes)
    return planes

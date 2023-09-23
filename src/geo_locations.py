from geopy.geocoders import Nominatim


def get_location_coordinates(city: str, country: str, state: str = ""):
    """
    Retrieve location with coordinates.
    :param city:
    :param country:
    :param state:
    :return: location object
    """
    geolocator = Nominatim(user_agent="my-personal-application")
    address = ""
    if city:
        address = city
    if state:
        address = f"{address}, {state}"
    address = f"{address}, {country}"

    location = geolocator.geocode(
        address,
        addressdetails=True,
        exactly_one=True,
        language="en",
        timeout=30,
    )
    if location and location.raw:
        return {
            "latitude": float(location.raw["lat"]),
            "longitude": float(location.raw["lon"]),
            "address": location.raw["address"],
        }

import requests

# Photon API endpoint
PHOTON_URL = "https://photon.komoot.io/api/"

# OpenStreetMap Overpass API endpoint
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

# Function to fetch geocoding data using Photon
def get_lat_lon(destination):
    """
    Convert a destination (e.g., "New York") into latitude and longitude using Photon.
    """
    params = {
        "q": destination,
        "limit": 1  # Limit to 1 result
    }
    try:
        response = requests.get(PHOTON_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        if data.get("features"):
            # Extract latitude, longitude, and display name from the first result
            first_result = data["features"][0]
            latitude = first_result["geometry"]["coordinates"][1]
            longitude = first_result["geometry"]["coordinates"][0]
            return float(latitude), float(longitude)
        else:
            print(f"No results found for destination: {destination}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geocoding data: {e}")
        return None, None

# Function to fetch restaurants using Overpass API
def get_restaurants(latitude, longitude, radius=1000):
    """
    Fetch restaurants near a given location using Overpass API.
    """
    # Overpass QL query to find restaurants
    query = f"""
    [out:json];
    node["amenity"="restaurant"](around:{radius},{latitude},{longitude});
    out body;
    >;
    out skel qt;
    """
    
    try:
        # Send request to Overpass API
        response = requests.get(OVERPASS_API_URL, params={"data": query}, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        results = response.json().get("elements", [])
        restaurants = []
        for element in results:
            restaurant = {
                "name": element["tags"].get("name"),
                "address": f"{element['tags'].get('addr:street', '')}, {element['tags'].get('addr:city', '')}".strip(", "),
                "cuisine": element["tags"].get("cuisine"),
                "website": element["tags"].get("website")
            }
            # Only add the restaurant if it has a name
            if restaurant["name"]:
                restaurants.append(restaurant)
        return restaurants[:5]  # Return top 5 restaurants
    except requests.exceptions.RequestException as e:
        print(f"Error fetching restaurants: {e}")
        return []

# Function to fetch tourist attractions using Overpass API
def get_attractions(latitude, longitude, radius=1000):
    """
    Fetch tourist attractions near a given location using Overpass API.
    """
    # Overpass QL query to find tourist attractions
    query = f"""
    [out:json];
    node["tourism"](around:{radius},{latitude},{longitude});
    out body;
    >;
    out skel qt;
    """
    
    try:
        # Send request to Overpass API
        response = requests.get(OVERPASS_API_URL, params={"data": query}, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        results = response.json().get("elements", [])
        attractions = []
        for element in results:
            attraction = {
                "name": element["tags"].get("name"),
                "address": f"{element['tags'].get('addr:street', '')}, {element['tags'].get('addr:city', '')}".strip(", "),
                "description": element["tags"].get("description")
            }
            # Only add the attraction if it has a name
            if attraction["name"]:
                attractions.append(attraction)
        return attractions[:5]  # Return top 5 attractions
    except requests.exceptions.RequestException as e:
        print(f"Error fetching attractions: {e}")
        return []

# Function to fetch hotels using Overpass API
def get_hotels(latitude, longitude, radius=1000):
    """
    Fetch hotels near a given location using Overpass API.
    """
    # Overpass QL query to find hotels
    query = f"""
    [out:json];
    node["tourism"="hotel"](around:{radius},{latitude},{longitude});
    out body;
    >;
    out skel qt;
    """
    
    try:
        # Send request to Overpass API
        response = requests.get(OVERPASS_API_URL, params={"data": query}, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        results = response.json().get("elements", [])
        hotels = []
        for element in results:
            hotel = {
                "name": element["tags"].get("name"),
                "address": f"{element['tags'].get('addr:street', '')}, {element['tags'].get('addr:city', '')}".strip(", "),
                "stars": element["tags"].get("stars"),
                "website": element["tags"].get("website")
            }
            # Only add the hotel if it has a name
            if hotel["name"]:
                hotels.append(hotel)
        return hotels[:5]  # Return top 5 hotels
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hotels: {e}")
        return []
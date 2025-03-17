import streamlit as st
from utils import get_lat_lon, get_attractions, get_restaurants, get_hotels

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "input_form"  # Default page is the input form

# Function to display the input form
def show_input_form():
    st.title("AI-Powered Travel Planner")

    # User Inputs
    destination = st.text_input("Enter your destination:")
    travel_dates = st.date_input("Select travel dates:", [])
    budget = st.slider("Select your budget (USD):", 0, 10000, 500)
    interests = st.multiselect("Select your interests:", ["Adventure", "Relaxation", "Food", "Culture"])
    check_in = st.date_input("Check-in date:")
    check_out = st.date_input("Check-out date:")

    # Generate Itinerary and Fetch Data
    if st.button("Generate Itinerary and Search"):
        if destination and travel_dates and budget and interests and check_in and check_out:
            # Fetch latitude and longitude for the destination
            latitude, longitude = get_lat_lon(destination)

            if latitude is not None and longitude is not None:
                # Fetch Data from APIs
                st.session_state["attractions"] = get_attractions(latitude, longitude)
                st.session_state["restaurants"] = get_restaurants(latitude, longitude)
                st.session_state["hotels"] = get_hotels(latitude, longitude)
                st.session_state["destination"] = destination
                st.session_state["travel_dates"] = travel_dates
                st.session_state["budget"] = budget
                st.session_state["interests"] = interests
                st.session_state["check_in"] = check_in
                st.session_state["check_out"] = check_out
                st.session_state["page"] = "results_page"  # Navigate to the results page
            else:
                st.error("Could not find coordinates for the destination. Please try again.")
        else:
            st.error("Please fill in all fields.")

# Function to display the results page
def show_results_page():
    st.title("Your Travel Itinerary")
    st.write(f"**Destination:** {st.session_state['destination']}")
    st.write(f"**Travel Dates:** {st.session_state['travel_dates'][0]} to {st.session_state['travel_dates'][1]}")
    st.write(f"**Budget:** ${st.session_state['budget']}")
    st.write(f"**Interests:** {', '.join(st.session_state['interests'])}")
    st.write(f"**Check-in:** {st.session_state['check_in']} | **Check-out:** {st.session_state['check_out']}")

    # Attractions
    st.header("Top Attractions")
    attractions = st.session_state["attractions"]
    if attractions:
        for attraction in attractions:
            with st.container():
                st.subheader(attraction["name"])
                if attraction["address"]:
                    st.write(f"📍 **Address:** {attraction['address']}")
                if attraction.get("description"):
                    st.write(f"📝 **Description:** {attraction['description']}")
                st.markdown("---")
    else:
        st.write("No attractions found.")

    # Restaurants
    st.header("Top Restaurants")
    restaurants = st.session_state["restaurants"]
    if restaurants:
        for restaurant in restaurants:
            with st.container():
                st.subheader(restaurant["name"])
                if restaurant["address"]:
                    st.write(f"📍 **Address:** {restaurant['address']}")
                if restaurant.get("cuisine"):
                    st.write(f"🍽️ **Cuisine:** {restaurant['cuisine']}")
                if restaurant.get("website"):
                    st.write(f"🌐 **Website:** [{restaurant['website']}]({restaurant['website']})")
                st.markdown("---")
    else:
        st.write("No restaurants found.")

    # Hotels
    st.header("Top Hotels")
    hotels = st.session_state["hotels"]
    if hotels:
        for hotel in hotels:
            with st.container():
                st.subheader(hotel["name"])
                if hotel["address"]:
                    st.write(f"📍 **Address:** {hotel['address']}")
                if hotel.get("stars"):
                    st.write(f"⭐ **Stars:** {hotel['stars']}")
                if hotel.get("website"):
                    st.write(f"🌐 **Website:** [{hotel['website']}]({hotel['website']})")
                st.markdown("---")
    else:
        st.write("No hotels found.")

    # Button to go back to the input form
    if st.button("Back to Input Form"):
        st.session_state["page"] = "input_form"  # Navigate back to the input form

# Main App Logic
if st.session_state["page"] == "input_form":
    show_input_form()
elif st.session_state["page"] == "results_page":
    show_results_page()
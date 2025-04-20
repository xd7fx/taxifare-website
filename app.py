
import streamlit as st
import datetime
import requests

st.set_page_config(page_title="Taxi Fare Predictor", layout="centered")

st.title("🚖 Predict the fare of a taxi ride in NYC.")

# ---------- Helper Function ----------
def safe_float(val):
    try:
        return float(str(val).replace("٫", ".").replace(",", ".").replace("’", "."))
    except:
        return 0.0

# ---------- Default Demo Values ----------
demo_values = {
    "pickup_longitude": -73.985428,
    "pickup_latitude": 40.758896,
    "dropoff_longitude": -73.973057,
    "dropoff_latitude": 40.764356,
    "passenger_count": 2,
    "pickup_date": datetime.date(2023, 8, 15),
    "pickup_time": datetime.time(14, 30)
}

# ---------- User Input ----------
col1, col2 = st.columns(2)
with col1:
    pickup_date = st.date_input("Pickup Date", value=datetime.date.today())
with col2:
    pickup_time = st.time_input("Pickup Time", value=datetime.datetime.now().time())

pickup_longitude = st.text_input("Pickup Longitude", value="-73.985428")
pickup_latitude = st.text_input("Pickup Latitude", value="40.758896")
dropoff_longitude = st.text_input("Dropoff Longitude", value="-73.973057")
dropoff_latitude = st.text_input("Dropoff Latitude", value="40.764356")
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)

# ---------- Auto-fill Button ----------
if st.button("🔁 Auto-fill demo values"):
    pickup_longitude = str(demo_values["pickup_longitude"])
    pickup_latitude = str(demo_values["pickup_latitude"])
    dropoff_longitude = str(demo_values["dropoff_longitude"])
    dropoff_latitude = str(demo_values["dropoff_latitude"])
    passenger_count = demo_values["passenger_count"]
    pickup_date = demo_values["pickup_date"]
    pickup_time = demo_values["pickup_time"]

# ---------- Predict Button ----------
if st.button("🚕 Predict Fare"):
    pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
    formatted_datetime = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

    url = "https://taxifare.lewagon.ai/predict"

    params = {
        "pickup_datetime": formatted_datetime,
        "pickup_longitude": safe_float(pickup_longitude),
        "pickup_latitude": safe_float(pickup_latitude),
        "dropoff_longitude": safe_float(dropoff_longitude),
        "dropoff_latitude": safe_float(dropoff_latitude),
        "passenger_count": int(passenger_count)
    }

    response = requests.get(url, params=params)
    prediction = response.json()

    st.write("🔍 Raw API Response:", prediction)

    if "fare" in prediction:
        fare = prediction["fare"]
        if fare < 0:
            st.error("❌ Predicted fare is negative. Please check your inputs.")
        else:
            st.success(f"💰 Predicted Fare: ${fare:.2f}")
    else:
        st.error(f"❌ Prediction failed: {prediction.get('error', 'Unknown error')}")

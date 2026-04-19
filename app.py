import streamlit as st
import pandas as pd
import numpy as np
import pickle

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open('model.pkl', 'rb'))
features = pickle.load(open('features.pkl', 'rb'))

# =========================
# UI CONFIG
# =========================
st.set_page_config(page_title="Prediksi Pengiriman", layout="centered")

st.title("🚚 Prediksi Waktu Pengiriman")
st.info("Prediksi berdasarkan jarak (km), kendaraan, lalu lintas, cuaca, dan waktu persiapan.")

st.markdown("---")

# =========================
# DATA KURIR
# =========================
st.subheader("👤 Data Kurir")
age = st.number_input("Umur Kurir", 18, 60, 30)
rating = st.number_input("Rating Kurir", 1.0, 5.0, 4.5)

st.markdown("---")

# =========================
# DETAIL (TANPA LOKASI)
# =========================
st.subheader("📦 Detail Pengiriman")

distance = st.number_input("Jarak Pengiriman (KM)", 0.0, 50.0, 5.0)
prep_time = st.number_input("Waktu Persiapan (menit)", 0.0, 60.0, 10.0)

st.caption("Masukkan jarak dalam kilometer (contoh: 5 = 5 km)")

st.markdown("---")

# =========================
# KONDISI KENDARAAN
# =========================
st.subheader("🚗 Kondisi Kendaraan")

vehicle_map = {
    "Buruk": 0,
    "Sedang": 1,
    "Baik": 2
}

vehicle_choice = st.selectbox("Kondisi Kendaraan", list(vehicle_map.keys()))
vehicle_condition = vehicle_map[vehicle_choice]

# =========================
# JENIS KENDARAAN (SUDAH MOBIL)
# =========================
st.subheader("🛵 Jenis Kendaraan")

vehicle_type_map = {
    "Mobil": "car",
    "Motor": "motorcycle",
    "Sepeda": "bicycle"
}

vehicle_type_choice = st.selectbox("Jenis Kendaraan", list(vehicle_type_map.keys()))
vehicle_type = vehicle_type_map[vehicle_type_choice]

st.markdown("---")

# =========================
# TRAFFIC
# =========================
st.subheader("🚦 Lalu Lintas")

traffic_map = {
    "Lancar": "Low",
    "Sedang": "Medium",
    "Padat": "High",
    "Macet": "Jam"
}

traffic_choice = st.selectbox("Kondisi Lalu Lintas", list(traffic_map.keys()))
traffic = traffic_map[traffic_choice]

# =========================
# CUACA
# =========================
st.subheader("🌦️ Cuaca")

weather_map = {
    "Cerah": "Sunny",
    "Berawan": "Cloudy",
    "Hujan": "Rainy",
    "Badai": "Stormy",
    "Berdebu": "Sandstorms",
    "Berkabut": "Fog"
}

weather_choice = st.selectbox("Kondisi Cuaca", list(weather_map.keys()))
weather = weather_map[weather_choice]

st.markdown("---")

# =========================
# PREDIKSI
# =========================
if st.button("🔮 Prediksi"):

    input_data = pd.DataFrame(np.zeros((1, len(features))), columns=features)

    # fitur utama
    if 'Delivery_person_Age' in input_data.columns:
        input_data['Delivery_person_Age'] = age

    if 'Delivery_person_Ratings' in input_data.columns:
        input_data['Delivery_person_Ratings'] = rating

    if 'distance' in input_data.columns:
        input_data['distance'] = distance

    if 'Vehicle_condition' in input_data.columns:
        input_data['Vehicle_condition'] = vehicle_condition

    if 'prep_time' in input_data.columns:
        input_data['prep_time'] = prep_time

    # =========================
    # VEHICLE TYPE (AMAN)
    # =========================
    for col in input_data.columns:
        if "Type_of_vehicle" in col:
            input_data[col] = 0

    vt_col = f"Type_of_vehicle_{vehicle_type}"
    if vt_col in input_data.columns:
        input_data[vt_col] = 1

    # =========================
    # TRAFFIC
    # =========================
    for col in input_data.columns:
        if "Road_traffic_density" in col:
            input_data[col] = 0

    tr_col = f"Road_traffic_density_{traffic}"
    if tr_col in input_data.columns:
        input_data[tr_col] = 1

    # =========================
    # WEATHER
    # =========================
    for col in input_data.columns:
        if "Weatherconditions" in col:
            input_data[col] = 0

    wc_col = f"Weatherconditions_{weather}"
    if wc_col in input_data.columns:
        input_data[wc_col] = 1

    # =========================
    # PREDIKSI
    # =========================
    prediction = model.predict(input_data)

    st.success(f"⏱️ Estimasi Waktu Pengiriman: {prediction[0]:.2f} menit")
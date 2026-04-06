import pandas as pd
import pickle as pk
import streamlit as st

model = pk.load(open('C:/Users/Poojani Danulya/Desktop/Jupyter Notebook/House Price Prediction/House_Price_Prediction_Model.pkl', 'rb'))

st.header('California House Price Predictor')
data = pd.read_csv('C:/Users/Poojani Danulya/Desktop/Jupyter Notebook/House Price Prediction/cleaned_data.csv')

# ---------------- USER INPUT ---------------- #

st.subheader("Enter Block Details")

housing_median_age = st.number_input("Median age of a house within block")
total_rooms = st.number_input("Total rooms within block")
total_bedrooms = st.number_input("Total bedrooms within block")
population = st.number_input("Population within block")
households = st.number_input("Households within block")
median_income = st.number_input("Median Income within block(in tens of thousands, e.g., 5 = $50,000)")
ocean_proximity = st.selectbox(
    "Ocean Proximity",
    ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
)

# ---------------- PROCESS INPUT ---------------- #

# One-hot encoding
ocean_dict = {
    "<1H OCEAN": 0,
    "INLAND": 0,
    "ISLAND": 0,
    "NEAR BAY": 0,
    "NEAR OCEAN": 0
}
ocean_dict[ocean_proximity] = 1

# Create DataFrame
input_data = pd.DataFrame([{
    'housing_median_age': housing_median_age,
    'total_rooms': total_rooms,
    'total_bedrooms': total_bedrooms,
    'population': population,
    'households': households,
    'median_income': median_income,
    '<1H OCEAN': ocean_dict["<1H OCEAN"],
    'INLAND': ocean_dict["INLAND"],
    'ISLAND': ocean_dict["ISLAND"],
    'NEAR BAY': ocean_dict["NEAR BAY"],
    'NEAR OCEAN': ocean_dict["NEAR OCEAN"],
}])

# Feature Engineering
input_data['bedrooms_per_house'] = input_data['total_bedrooms'] / input_data['households']
input_data['rooms_per_house'] = input_data['total_rooms'] / input_data['households']
input_data['population_per_house'] = input_data['population'] / input_data['households']

# ---------------- PREDICT ---------------- #

if st.button("Predict Price "):
    prediction = model.predict(input_data)
    st.success(f"Estimated House Price: ${prediction[0]:,.2f}")

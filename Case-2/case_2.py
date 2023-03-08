import streamlit as st
import kaggle
import zipfile
import os
import pandas as pd
import plotly.express as pe

api = kaggle.api
datasets = api.datasets_list(search='Airplane Crashes and Fatalities')
ref = datasets[0]['ref']

kaggle.api.dataset_download_files(ref,path='data')

files = os.listdir("data")
for file in files:
    if ".zip" in file:
        with zipfile.ZipFile(f"data/{file}","r") as zip_ref:
            zip_ref.extractall("data")


api = kaggle.api
datasets = api.datasets_list(search='Air Traffic Passenger Statistics')
ref = datasets[0]['ref']

kaggle.api.dataset_download_files(ref,path='data')

files = os.listdir("data")
for file in files:
    if ".zip" in file:
        with zipfile.ZipFile(f"data/{file}","r") as zip_ref:
            zip_ref.extractall("data")

st.title('HI :)')


option = st.selectbox(
    'Select yearly statistic',
    ('Passengers', 'Flights'))

st.write('You selected:', option)

Air_Traffic = pd.read_csv("data/Air_Traffic_Passenger_Statistics.csv")

if option == 'Passengers':
    fig = pe.histogram(Air_Traffic,x='Year',y='Passenger Count')
    st.plotly_chart(fig)
elif option == 'Flights':
    fig = pe.histogram(Air_Traffic,x='Year')
    st.plotly_chart(fig)


from matplotlib import figure
from matplotlib.backend_bases import FigureCanvasBase
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as pe
import plotly.express as px
from sklearn.linear_model import LinearRegression
from matplotlib.widgets import Slider


import kaggle
import zipfile
import os

#Sara
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
            

st.title('Dataset: Air Traffic Passenger Statistics)')
st.markdown("De luchtvaart is wereldwijd een van de populairste vormen van vervoer. Miljoenen mensen reizen elke dag met het vliegtuig voor hun werk, vakantie en persoonlijke redenen. De statistieken over vliegtuigpassagiers bieden een waardevol inzicht in trends in het luchtverkeer en helpen belanghebbenden geïnformeerde beslissingen te nemen over de luchtvaartindustrie. De Air Traffic Passenger Statistics dataset bevat maandelijkse gegevens over het aantal passagiers dat wereldwijd via de vliegvelden reizen. De dataset omvat gegevens van meer dan 15000 luchtvaartmaatschappijen van aantal landen.De Air Traffic Passenger Statistics dataset oplevert waardevolle inzichten in het luchtverkeer en de prestaties van de luchtvaartindustrie. De gegevens kunnen worden gebruikt door beleidsmakers, luchthavenautoriteiten en luchtvaartmaatschappijen om met kennis van zaken beslissen over de sector. Het is echter belangrijk op te merken dat de dataset mogelijk niet alle aspecten van het luchtverkeer omvat en dat aanvullende gegevensbronnen nodig kunnen zijn om een volledig inzicht in de sector te krijgen.")


st.subheader('Een overzicht over aantal passengers per top luchtvaartmaatschappij')
st.markdown("In deze visualisatie wordt de passagiers per aantal luchtvaartmaatschappij getoond. Op basis van deze visualisatie wordt duidelijk dat de aantal passagiers per luchtvaartmaatschappijen enorm verschillen van elkaar. United Airline Pre heeft bijvoorbeeld de meeste passagiers in vergelijking met andere luchtvaartmaatschappijen.")
Air_Traffic = pd.read_csv('data/Air_Traffic_Passenger_Statistics.csv')



import streamlit as st


busiest_airports = Air_Traffic.groupby('Operating Airline').sum()['Passenger Count'].sort_values(ascending=False)[:10]
fig,ax = plt.subplots()
ax.bar(busiest_airports.index, busiest_airports.values)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ax.set_xticklabels(['United Airelines Pre', 'United Airelines', 'SkyWest Aireline', 'American Airelines', 'Virgin America', 'Delta Aire lines', 'Southwest Airelines', 'US Airelines', 'Alaska Aireline', 'JetBlue Aireways'], rotation=45, ha='right')
ax.set_xlabel('Luchtvaartmaatschappij')
ax.set_ylabel('Passagiers')
ax.set_title('Aantal Passagiers per luchtvaartmaatschappij')

st.pyplot(fig)



# Variabelen die ik nodig heb
JAAR = Air_Traffic['Year']
PASSENGER= Air_Traffic['Passenger Count']
LANDEN = Air_Traffic['GEO Region']
SOORT_VLIEGTUIG = Air_Traffic['GEO Summary']

st.subheader("Een overzicht over de luchtvaartmaatschappijen per land")
st.markdown("Met behulp van deze visualisatie laat de aantal passagiers per luchtvaartmaatschaappij zien. Op basis van jaartal wortd er een slider toegevoegd, daarnaast is er nog een dropdown beschikbaar gesteld zodat alleen de relevante data kunnen gekozen worden.")


LANDEN = st.selectbox(
    'Landen',
    ('US', 'Central America', 'Canada', 'Asia', 'Europe', 'Mexico', 'Australia / OceaniaAustralia'))

st.write('U hebt gekozen voor', LANDEN, 'gekozen')



Air_Traffic_filtered = Air_Traffic[(Air_Traffic['GEO Region'] == LANDEN) & (Air_Traffic['Year'] == JAAR)]

fig = px.bar(
    data_frame=Air_Traffic_filtered,
    x='Operating Airline',
    y='Passenger Count',
    animation_frame='Month',
    title='De luchtvaartmaatschappijen per land'
)
st.plotly_chart(fig)
JAAR = st.slider('Welke jaar?', 2006, 2016)
st.write('In', JAAR)




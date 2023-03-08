from matplotlib import figure
from matplotlib.backend_bases import FigureCanvasBase
import streamlit
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
            

streamlit.title('Dataset: Air Traffic Passenger Statistics)')

Air_Traffic = pd.read_csv('data/Air_Traffic_Passenger_Statistics.csv')



import streamlit as st

# fig, ax = plt.subplots()
# colors = np.where(Air_Traffic["Operating Airline"] == 1, "blue", "red")
# ax.scatter(Air_Traffic["Operating Aireline"], Air_Traffic["Passenger Count"], color=colors, alpha=0.5)
# ax.plot(Air_Traffic["Year"], y_pred, color="green")

# ax.set_xlabel("Year")
# ax.set_ylabel("Passenger Count")
# ax.set_title("Air Traffic Passenger Statistics")

# st.pyplot(fig)

busiest_airports = Air_Traffic.groupby('Operating Airline').sum()['Passenger Count'].sort_values(ascending=False)[:10]

fig,ax = plt.subplots()
ax.bar(busiest_airports.index, busiest_airports.values)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ax.set_xticklabels(['United Airelines Pre', 'United Airelines', 'SkyWest Aireline', 'American Airelines', 'Virgin America', 'Delta Aire lines', 'Southwest Airelines', 'US Airelines', 'Alaska Aireline', 'JetBlue Aireways'], rotation=45, ha='right')
ax.set_xlabel('Airline')
ax.set_ylabel('Passengers')
ax.set_title('Busiest Airports')

st.pyplot(fig)


# -----

X = Air_Traffic[["Year", "Price Category Code"]]
y = Air_Traffic["Passenger Count"].values.reshape(-1, 1)


X = pd.get_dummies(X, columns=["Price Category Code"])

regressor = LinearRegression()
regressor.fit(X, y)
y_pred = regressor.predict(X)

fig, ax = plt.subplots()
colors = np.where(Air_Traffic["Price Category Code"] == 2, "blue", "red")
ax.scatter(Air_Traffic["Year"], Air_Traffic["Passenger Count"], color=colors, alpha=0.5)
ax.plot(Air_Traffic["Year"], y_pred, color="green")

ax.set_xlabel("Year")
ax.set_ylabel("Passenger Count")
ax.set_title("Air Traffic Passenger Statistics")

st.pyplot(fig)

# Create a subplot
JAAR = Air_Traffic['Year']
PASSENGER= Air_Traffic['Passenger Count']
LANDEN = Air_Traffic['GEO Region']


LANDEN = st.selectbox(
    'Landen',
    ('US', 'Central America', 'Canada', 'Asia', 'Europe', 'Mexico', 'Australia / OceaniaAustralia'))

st.write('You selected:', LANDEN)


JAAR = st.slider('Welke jaar?', 2006, 2016)
st.write('In', JAAR)

#fig = pe.bar(Air_Traffic, x= 'GEO Region', y='Passenger Count')
#st.plotly_chart(fig)





Air_Traffic_filtered = Air_Traffic[(Air_Traffic['GEO Region'] == LANDEN) & (Air_Traffic['Year'] == JAAR)]

fig = px.bar(
    data_frame=Air_Traffic_filtered,
    x='Operating Airline',
    y='Passenger Count',
    animation_frame='Month',
    title='Aantal passengers per vliegtveld'
)

st.plotly_chart(fig)



#st.markdown()

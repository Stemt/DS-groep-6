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

# assign date
def period_to_date(var):
    period = str(var)
    year = period[0:4]
    month = period[4:]
    return f"{year}-{month}"

Air_Traffic['Date'] = pd.to_datetime(Air_Traffic['Activity Period'].apply(period_to_date))

# passenger trends
passenger_per_year = Air_Traffic.groupby(['Date','GEO Region']).sum()['Passenger Count']

passenger_flights = {
    'date':[],
    'region':[],
    'passengers':[],
}
for key in passenger_per_year.keys():
    passenger_flights['date'].append(key[0])
    passenger_flights['region'].append(key[1])
    passenger_flights['passengers'].append(passenger_per_year[key])


passenger_flights_df = pd.DataFrame(passenger_flights)


fig = pe.line(passenger_flights_df,x='date',y='passengers',color='region',markers=True,symbol='region')
fig.update_traces(marker={'size': 10})
st.plotly_chart(fig)
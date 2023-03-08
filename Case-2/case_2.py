import streamlit

streamlit.title('Testing')


import pandas as pd
import zipfile 

zf = zipfile.ZipFile("./airplane-crashes-and-fatalities.zip")
acf_df = pd.read_csv(zf.open("Airplane_Crashes_and_Fatalities_Since_1908.csv"))
acf_df.head()

import seaborn as sns 
import matplotlib as plt
import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots

# total fatilities of each year 
acf_df['Date'] = pd.to_datetime(acf_df['Date'])

# jaarlijkse slachtoffers 
yearly_fatalities = acf_df.groupby(acf_df.Date.dt.year).agg({'Fatalities': 'sum', 'Aboard': 'sum'}).reset_index()

aircraft_counts = acf_df.groupby([acf_df.Date.dt.year, 'Type']).size().reset_index(name = "aantal") # Aantal vliegtuigen per type
max_ac_per_year = aircraft_counts.groupby('Date')['aantal'].idxmax() # Meest voorkomend vliegtuig per jaar op basis van index
most_common_aircraft = aircraft_counts.loc[max_ac_per_year] # Laat het type vliegtuig zien dat het vaakst voorkomt per jaar. 

yearly_fatalities_aircraft = yearly_fatalities.merge(most_common_aircraft[["Date", "Type"]], on = "Date")
print(yearly_fatalities_aircraft)

# creeëren van slider
rangeselector=dict(
    buttons=list([
        dict(count=10, label = "10j", step = "year", stepmode = "backward"),
        dict(count=20, label = "20j", step = "year", stepmode = "backward"),
        dict(count=30, label = "30j", step = "year", stepmode = "backward"),
        dict(count=40, label = "40j", step = "year", stepmode = "backward"),
        dict(count=50, label = "50j", step = "year", stepmode = "backward"),
        dict(count=60, label = "60j", step = "year", stepmode = "backward"),
        dict(count=70, label = "70j", step = "year", stepmode = "backward"),
        dict(count=80, label = "80j", step = "year", stepmode = "backward"),
        dict(count=90, label = "90j", step = "year", stepmode = "backward"),
        dict(count=100, label = "100j", step = "year", stepmode = "backward"),
        dict(step = "all")]))
#grafiek van slachtoffers en passagiers aanboord door de jaren heen
fig = go.Figure()

fig.add_trace(go.Scatter(x = yearly_fatalities_aircraft["Date"], y = yearly_fatalities_aircraft["Fatalities"], name = "Slachtoffers"))
fig.add_trace(go.Scatter(x = yearly_fatalities_aircraft["Date"], y = yearly_fatalities_aircraft["Aboard"], name = "Totaal passagiers"))

fig.update_layout(title = "Totaal aantal passagiers en slachtoffers", xaxis_title = "Jaren", yaxis_title = "Aantal passagiers en slachtoffers",
                 xaxis_rangeslider_visible=True, xaxis=dict(rangeselector=rangeselector),
                  updatemenus = [{"type":'dropdown',"showactive" : True, "active":0
                               }]
                 )
                  
streamlit.header("Slachtoffers door de jaren heen ")
streamlit.markdown("De grafiek geeft het totale aantal slachtoffers en passagiers door de jaren heen weer. De lijnen volgen logischerwijs hetzelfde patroon. Aan de grafiek is te zien dat voornamelijk aan het begin van luchtvaart geen overlevenden waren bij ongelukken. Daarnaast geeft de grafiek weer dat het aantal slachtoffers stijgt na de tweede wereldoorlog, omdat na de tweede wereldoorlog het aantal vluchten stijgt. In de laatste jaren is een daling van het aantal slachtoffers en ongelukken te zien sinds de veiligheid van vliegen een steeds belangrijker thema werd. ")
streamlit.plotly_chart(fig)                 


# grafiek met slachtoffers en aantal passagiers 2005-2009
zf1 = zipfile.ZipFile("./airlines-traffic-passenger-statistics.zip")
atps_df = pd.read_csv(zf1.open("Air_Traffic_Passenger_Statistics.csv"))
atps_df.head()

atps_df["Date"] = atps_df["Year"].copy()
print(atps_df["Date"])

yearly_passenger_count = atps_df.groupby('Date')['Passenger Count'].sum().reset_index()
print(yearly_passenger_count)

fatalities_05_09 = yearly_fatalities_aircraft[yearly_fatalities["Date"] >= 2005]
print(fatalities_05_09)

passengercount_05_09 = yearly_passenger_count[ (yearly_passenger_count["Date"] >= 2005) & (yearly_passenger_count["Date"] <= 2009)]
print(passengercount_05_09)

passenger_fatalities = passengercount_05_09.merge(fatalities_05_09, on = "Date")
print(passenger_fatalities)

fig2 = make_subplots(rows = 2, cols = 1, subplot_titles=("Aantal passagiers", "Aantal slachtoffers"))


fig2.append_trace(go.Bar(x = passenger_fatalities["Date"], y = passenger_fatalities["Passenger Count"], name = "Aantal passagiers"), row = 1, col = 1)
fig2.append_trace(go.Bar(x = passenger_fatalities["Date"], y = passenger_fatalities["Fatalities"], name = "Aantal slachtoffers", offsetgroup=1), row = 2, col = 1)



fig2.update_layout(title_text="Aantal passagiers en slachtoffers 2005-2009")
fig2.update_xaxes(title_text="Jaren")
   
streamlit.header("Slachtoffers ten opzichte van passagiers aantallen")
streamlit.markdown("Om een beeld te krijgen van het aantal dodelijke slachtoffers ten opzichte van de totale aantal passagiers, zijn de twee datasets samengevoegd. Voor de vergelijking zijn de jaren 2005-2009 gebruikt. De bovenste staafdiagram laat het aantal passagiers zien van dat jaar. Te zien is dat na 2005 het aantal passagiers stijgt tot ongeveer 30 miljoen passagiers in 2006. Na 2006 is de stijging aanzienlijk minder, tot in 2009 tot ongeveer 37 miljoen passagiers.  De onderste staafdiagram geeft het aantal dodelijk slachtoffers over dezelfde jaar weer. Goed te zien is dat het aantal dodelijk slachtoffers blijft dalen door de jaren heen terwijl het aantal passagiers stijgt. Dit laat zien dat er nog steeds veel geïnvesteerd wordt in de vliegveiligheid en het percentage van dodelijke slachtoffers onder de 1% zit. ")
streamlit.plotly_chart(fig2)



# Top 10 aircraft tabel
streamlit.header("Top 10 vliegtuigen")
streamlit.markdown("De tabel laat de 10 meest voorkomende vliegtuigen in de dataset zien.")
top_10_ac = acf_df["Type"].value_counts().iloc[0:10]
streamlit.write(top_10_ac)


import streamlit as st
import zipfile
import os
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots
import datetime
import matplotlib.dates as mdates


app_dir = os.path.dirname(__file__)

Air_Traffic = pd.read_csv(f"{app_dir}/data/Air_Traffic_Passenger_Statistics.csv")
atps_df = Air_Traffic
acf_df = pd.read_csv(f"{app_dir}/data/Airplane_Crashes_and_Fatalities_Since_1908.csv")
print(acf_df.head())


# matthijs

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
                  
st.header("Slachtoffers door de jaren heen ")
st.text("Bronnon: https://www.agcs.allianz.com/news-and-insights/expert-risk-articles/how-aviation-safety-has-improved.html")
st.markdown("De grafiek geeft het totale aantal slachtoffers en passagiers door de jaren heen weer. De lijnen volgen logischerwijs hetzelfde patroon. Aan de grafiek is te zien dat voornamelijk aan het begin van luchtvaart geen overlevenden waren bij ongelukken. De hoge aantallen vliegtuigongelukken en sterfgevallen in 1970 werden veroorzaakt door meerdere factoren, waaronder toegenomen luchtverkeer, weersgerelateerde problemen, menselijke fouten, apparatuurstoringen en veiligheidskwesties zoals kapingen en pogingen tot kaping. De afname van vliegtuigongelukken en sterfgevallen vanaf de jaren 2000 was te danken aan betere vliegtuigontwerpen, veiligheidstechnologieën, opleiding en certificeringsnormen voor piloten, luchtverkeersleidingssystemen, regelgeving en toezicht door luchtvaartautoriteiten, strengere veiligheidsprocedures van luchtvaartmaatschappijen (zoals onderhoudsinspecties, pre-flight checks en bemanningsnseheerpraktijken) en vooruitgang in weersvoorspellingen en communicatietechnologie.(How aviation safety has improved, z.d.)")
st.plotly_chart(fig)                 

st.header("Regressie model van de slachtoffers vanaf 1950 tot 2009")
# regressie 
#Data cleaning REGRESSION

date_fatalities = acf_df.groupby(acf_df['Date'])['Fatalities'].sum().reset_index()
date_fatalities['Date'] = pd.to_datetime(date_fatalities['Date'], unit='ns')
print(date_fatalities)

#Data verkenning REGRESSION + visualisatie 


st.subheader("Regressie model")

st.markdown("Uit de visualisatie is er te zien dat er meerdere uitschieters zijn op verschillende jaren. Ook is er te zien dat er vanaf 1970-2008 er een afname is in slachtoffers. Een voorspellende reggresie model zou in dit geval niet betrouwbaar zijn, want de vliegtuigen in de dataset zullen verouderd zijn.")

#Regressie

show_regression = st.checkbox("Toon regressielijn")

subset = date_fatalities[(date_fatalities['Date'] >= datetime.datetime(1950, 1, 1)) & (date_fatalities['Fatalities'] > 150)].copy()

subset.loc[:, 'Date'] = subset['Date'].apply(mdates.date2num)

fig = plt.figure()

ax = sns.regplot(data=subset, x='Date', y='Fatalities', fit_reg=show_regression, dropna=True, marker='*', scatter_kws={"color": "blue"}, line_kws={"color": "red"})
date_format = mdates.DateFormatter('%m/%d/%Y')
ax.xaxis.set_major_formatter(date_format)
ax.xaxis.set_tick_params(rotation=45)

ax.set_title("Regressie slachtoffers door de jaren heen")
ax.set(xlabel="Jaren", ylabel="Slachtoffers")

st.pyplot(fig)

# grafiek met slachtoffers en aantal passagiers 2005-2009
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
   
st.header("Slachtoffers ten opzichte van passagiers aantallen")
st.markdown("Om een beeld te krijgen van het aantal dodelijke slachtoffers ten opzichte van de totale aantal passagiers, zijn de twee datasets samengevoegd. Voor de vergelijking zijn de jaren 2005-2009 gebruikt. De bovenste staafdiagram laat het aantal passagiers zien van dat jaar. Te zien is dat na 2005 het aantal passagiers stijgt tot ongeveer 30 miljoen passagiers in 2006. Na 2006 is de stijging aanzienlijk minder, tot in 2009 tot ongeveer 37 miljoen passagiers.  De onderste staafdiagram geeft het aantal dodelijk slachtoffers over dezelfde jaar weer. Goed te zien is dat het aantal dodelijk slachtoffers blijft dalen door de jaren heen terwijl het aantal passagiers stijgt. Dit laat zien dat er nog steeds veel geïnvesteerd wordt in de vliegveiligheid en het percentage van dodelijke slachtoffers onder de 1% zit. ")
st.plotly_chart(fig2)

st.header('Hoogste aantal slachtoffers per type vliegtuig en operators')

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


#Data Cleaning TYPE
type_fatalities = acf_df.groupby(acf_df['Type'])['Fatalities'].sum().reset_index()
print(type_fatalities)

#Data verkenning TYPE + visualisatie

#Interactieve weergave van het type en fatalities
import plotly.express as px

st.subheader("Type vliegtuig")
#barplot van top 10 aircraft
top_10_ac = acf_df["Type"].value_counts().iloc[0:10]
top_10_ac_df = pd.DataFrame(top_10_ac)

bar_top_10 = px.bar(top_10_ac, y = "Type")
bar_top_10.update_layout(title = "Aantal toestellen betrokken bij ongelukken", xaxis_title = "Toestel", yaxis_title = "Aantal")
st.markdown("De barplot geeft weer het aantal toestellen weer dat betrokken is bij ongelukken sinds 1908. Te zien is dat voornamelijk toestellen die ook voor militaire doeleinden gebruikt worden vaak betrokken zijn bij ongelukken.")
st.plotly_chart(bar_top_10)
st.markdown("Er is te zien dat het type Douglas DC-3 de meeste slachtoffers had, in totaal waren dat 4793 personen. Als er gekeken wordt naar de top 4 type vliegtuifen, met de meeste slachtoffers boven 1000 personen, is er te zien dat alle vliegtuigen commerciele en militairen zijn. De vliegtuigen zijn voornamelijk voor militairen operaties gebruikt. Wat opvalt uit de visualisatie is dat er drie verschillende type vliegtuigen, met de meeste fatalities, van dezelfde vliegtuigbouwer zijn; Douglas. Dit zijn absolute waarden dus er is alleen naar de aantal slachtoffers gekeken en niet naar b.v. hoeveel vluchten ieder type vliegtuigen heeft uitgevoerd.")

fig = px.bar(type_fatalities.query('Fatalities > 1000'),
             y="Fatalities",
             x="Type",
             animation_frame="Type", animation_group="Type",
             color="Fatalities", 
             log_y=True,
             title="Aantal slachtoffers per type vliegtuig (slachtoffers > 1000)", range_y=[1,10000], range_x=[-0.5,3.3], labels={"Fatalities": "Slachtoffers"})

fig.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig)

#Data Cleaning OPERATOR
operator_fatalities = acf_df.groupby(acf_df['Operator'])['Fatalities'].sum().reset_index()
print(operator_fatalities)

st.subheader("Operators")

#Data verkenning OPERATOR + visualisatie

# Nu kijken we naar de meeste doden per operator
# Top 7 operators met de meeste doden
import plotly.graph_objs as go

st.markdown("Uit de data is te zien dat de operator Aeroflot de meeste slachtoffers heeft, in totaal zijn er 7156 personen gestorven. Wanneer er naar de gehele visualisatie wordt gekeken is er te zien dat er 5 commerciele operators zijn; Aeroflot, Air France, American Airlines, Pan American World Airways en United Air Lines. Daarnaast zijn er twee militairen operators met de meeste fatalities; U.S. Air Force en U.S. Army Air Forces.")

operator_data = operator_fatalities.query('Fatalities > 1000')

colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'pink', 'gray', 'brown']

data = []
for i, operator in enumerate(operator_data['Operator'].unique()):
    operator_subset = operator_data[operator_data['Operator'] == operator]
    trace = go.Bar(
        x=operator_subset['Operator'], 
        y=operator_subset['Fatalities'], 
        name=operator, 
        visible=True,
        marker=dict(color=colors[i])
    )
    data.append(trace)

buttons = []
for operator in operator_data['Operator'].unique():
    button = dict(
        label=operator,
        method="update",
        args=[{"visible": [operator == trace.name for trace in data]}, {'title': operator}]
    )
    buttons.append(button)

updatemenus = list([
    dict(
        buttons=list(buttons),
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=1.2,
        xanchor="left",
        y=1.2,
        yanchor="top"
    ),
])

layout = go.Layout(
    title="Aantal slachtoffers per operator (slachtoffers > 1000)",
    xaxis={'title': 'Operator'},
    yaxis={'title': 'Slachtoffers', 'range': [0, 10000]},
    updatemenus=updatemenus,
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)

st.plotly_chart(fig)

# alaric
option = st.selectbox(
    'Select yearly statistic',
    ('Passengers', 'Flights'))

st.write('You selected:', option)


if option == 'Passengers':
    fig = px.histogram(Air_Traffic,x='Year',y='Passenger Count')
    st.plotly_chart(fig)
elif option == 'Flights':
    fig = px.histogram(Air_Traffic,x='Year')
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


fig = px.line(passenger_flights_df,x='date',y='passengers',color='region',markers=True,symbol='region')
fig.update_traces(marker={'size': 10})
st.plotly_chart(fig)
import streamlit

streamlit.header('Hoogste aantal slachtoffers per type vliegtuig en operators')

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

acf_df = pd.read_csv("data/Airplane_Crashes_and_Fatalities_Since_1908.csv")
acf_df.head()

#Data Cleaning TYPE
type_fatalities = acf_df.groupby(acf_df['Type'])['Fatalities'].sum().reset_index()
print(type_fatalities)

#Data verkenning TYPE + visualisatie

#Interactieve weergave van het type en fatalities
import plotly.express as px

streamlit.subheader("Type vliegtuig")

streamlit.markdown("Er is te zien dat het type Douglas DC-3 de meeste slachtoffers had, in totaal waren dat 4793 personen. Als er gekeken wordt naar de top 4 type vliegtuifen, met de meeste slachtoffers boven 1000 personen, is er te zien dat alle vliegtuigen commerciele en militairen zijn. De vliegtuigen zijn voornamelijk voor militairen operaties gebruikt. Wat opvalt uit de visualisatie is dat er drie verschillende type vliegtuigen, met de meeste fatalities, van dezelfde vliegtuigbouwer zijn; Douglas. Dit zijn absolute waarden dus er is alleen naar de aantal slachtoffers gekeken en niet naar b.v. hoeveel vluchten ieder type vliegtuigen heeft uitgevoerd.")

fig = px.bar(type_fatalities.query('Fatalities > 1000'),
             y="Fatalities",
             x="Type",
             animation_frame="Type", animation_group="Type",
             color="Fatalities", 
             log_y=True,
             title="Aantal slachtoffers per type vliegtuig (slachtoffers > 1000)", range_y=[1,10000], range_x=[-0.5,3.3], labels={"Fatalities": "Slachtoffers"})

fig.update_layout(yaxis={'categoryorder':'total ascending'})

streamlit.plotly_chart(fig)

#Data Cleaning OPERATOR
operator_fatalities = acf_df.groupby(acf_df['Operator'])['Fatalities'].sum().reset_index()
print(operator_fatalities)

streamlit.subheader("Operators")

#Data verkenning OPERATOR + visualisatie

# Nu kijken we naar de meeste doden per operator
# Top 7 operators met de meeste doden
import plotly.graph_objs as go

streamlit.markdown("Uit de data is te zien dat de operator Aeroflot de meeste slachtoffers heeft, in totaal zijn er 7156 personen gestorven. Wanneer er naar de gehele visualisatie wordt gekeken is er te zien dat er 5 commerciele operators zijn; Aeroflot, Air France, American Airlines, Pan American World Airways en United Air Lines. Daarnaast zijn er twee militairen operators met de meeste fatalities; U.S. Air Force en U.S. Army Air Forces.")

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

streamlit.plotly_chart(fig)

streamlit.header("Regressie model van de slachtoffers vanaf 1950 tot 2009")

#Data cleaning REGRESSION

date_fatalities = acf_df.groupby(acf_df['Date'])['Fatalities'].sum().reset_index()
date_fatalities['Date'] = pd.to_datetime(date_fatalities['Date'], unit='ns')
print(date_fatalities)

#Data verkenning REGRESSION + visualisatie 

#Hier nog een checkbox toevoegen, zodat het de regressielijn weergeeft met een 'Ja' of 'Nee' 
import datetime
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

streamlit.subheader("Regressie model")

streamlit.markdown("Uit de visualisatie is er te zien dat er meerdere uitschieters zijn op verschillende jaren. Ook is er te zien dat er vanaf 1970-2008 er een afname is in slachtoffers. Een voorspellende reggresie model zou in dit geval niet betrouwbaar zijn, want de vliegtuigen in de dataset zullen verouderd zijn.")

#Regressie
import streamlit as st

show_regression = st.checkbox("Toon regressielijn")

subset = date_fatalities[(date_fatalities['Date'] >= datetime.datetime(1950, 1, 1)) & (date_fatalities['Fatalities'] > 150)].copy()

subset.loc[:, 'Date'] = subset['Date'].apply(mdates.date2num)

fig = plt.figure()

ax = sb.regplot(data=subset, x='Date', y='Fatalities', fit_reg=show_regression, dropna=True, marker='*', scatter_kws={"color": "blue"}, line_kws={"color": "red"})
date_format = mdates.DateFormatter('%m/%d/%Y')
ax.xaxis.set_major_formatter(date_format)
ax.xaxis.set_tick_params(rotation=45)

ax.set_title("Regressie slachtoffers door de jaren heen")
ax.set(xlabel="Jaren", ylabel="Slachtoffers")

streamlit.pyplot(fig)

streamlit.header("Totaal aantal slachtoffers per jaar")
streamlit.text("Bronnon: https://www.agcs.allianz.com/news-and-insights/expert-risk-articles/how-aviation-safety-has-improved.html")
streamlit.markdown("De hoge aantallen vliegtuigongelukken en sterfgevallen in 1970 werden veroorzaakt door meerdere factoren, waaronder toegenomen luchtverkeer, weersgerelateerde problemen, menselijke fouten, apparatuurstoringen en veiligheidskwesties zoals kapingen en pogingen tot kaping. De afname van vliegtuigongelukken en sterfgevallen vanaf de jaren 2000 was te danken aan betere vliegtuigontwerpen, veiligheidstechnologieën, opleiding en certificeringsnormen voor piloten, luchtverkeersleidingssystemen, regelgeving en toezicht door luchtvaartautoriteiten, strengere veiligheidsprocedures van luchtvaartmaatschappijen (zoals onderhoudsinspecties, pre-flight checks en bemanningsbeheerpraktijken) en vooruitgang in weersvoorspellingen en communicatietechnologie.(How aviation safety has improved, z.d.)")
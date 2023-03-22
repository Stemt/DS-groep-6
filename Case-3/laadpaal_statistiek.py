import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

def laadpaal_stats():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title("Laadpaaldata inzichten van elektrische auto's")

    #FlowChart Data Cleaning laadpaaldata

    #st.image()

    #DATA CLEANING - HANNA
    laadpaal = pd.read_csv("data/laadpaaldata.csv")
    print(laadpaal)

    # Geen ontbrekende data
    laadpaal.isna().sum() 

    laadpaal.drop_duplicates()

    # Foute data wordt gefiltered

    def dropinvalid_leap(Datum):
        try:
            pd.to_datetime(Datum)
            return False
        except:
            print(Datum)
            return True

    laadpaal_cleaned = laadpaal[~laadpaal['Started'].apply(dropinvalid_leap)]
    laadpaal_cleaned = laadpaal_cleaned[~laadpaal_cleaned['Ended'].apply(dropinvalid_leap)]

    laadpaal_cleaned['Started'] = pd.to_datetime(laadpaal_cleaned['Started'])
    laadpaal_cleaned['Ended'] = pd.to_datetime(laadpaal_cleaned['Ended'])

    # Tijdverschil tussen 'Started' en 'Ended'
    laadpaal_cleaned['TotalTime'] = (laadpaal_cleaned['Ended'] - laadpaal_cleaned['Started']) / pd.Timedelta(hours=1)

    # Toevoegen kolom AvgEnergy (W)
    laadpaal_cleaned['AvgEnergy'] = (laadpaal_cleaned['TotalEnergy'] / laadpaal_cleaned['ChargeTime']) 

    # Filteren op laadsessies waarbij ChargeTime > 0 uur is en  <= 40
    laadpaal_cleaned = laadpaal_cleaned[(laadpaal_cleaned["ChargeTime"] > 0) & (laadpaal_cleaned["ChargeTime"] <= 48) & (laadpaal_cleaned["ConnectedTime"] <= 40)]



    #Bij presentatie laten zien
    st.header('Inzichten ophalen')
    st.markdown("Uit de scatterplot kan worden afgeleid dat er een duidelijk verband bestaat tussen de laadsnelheid van elektrische auto's en het bijbehorende vermogen. Bij een snelle laadtijd wordt over het algemeen een hoog vermogen gebruikt, terwijl er bij een langere laadtijd juist sprake is van een lager vermogen. Deze bevindingen zijn gemakkelijk af te lezen uit de grafiek en bieden waardevolle inzichten in de relatie tussen laadsnelheid en vermogen van elektrische auto's.")

    #max_power = laadpaal_cleaned["MaxPower"]
    #charge_time = laadpaal_cleaned["ChargeTime"]

    #plt.scatter(max_power, charge_time, color='pink')
    #plt.title("Relatie tussen laadtijd en vermogen")
    #plt.xlabel("Max vermogen (Watt)")
    #plt.ylabel("Laadtijd (Uren)")
    #st.pyplot()

    fig = px.scatter(laadpaal_cleaned, x="MaxPower", y="ChargeTime", labels={"MaxPower": "Max vermogen (Watt)", "ChargeTime": "Laadtijd (Uren)"}, trendline="ols", trendline_scope="overall")

    fig.update_traces(marker=dict(color='purple'), line=dict(color='black'))

    st.plotly_chart(fig)



    #HISTOGRAM - HANNA

    st.header('Verdeling laadtijden')
    st.markdown("Het histogram toont de verdeling van laadtijden van elektrische auto's op basis van gegevens verzameld van laadpalen. Laadtijd wordt hierbij gedefinieerd als de tijd waarin er effectief stroom wordt geladen. Met behulp van deze visualisatie is er inzicht verkregen in hoe de laadtijden van elektrische auto's over deze dataset verdeeld zijn.")

    #Berekenen mean en mediaan
    mean_charge_time = np.mean(laadpaal_cleaned["ChargeTime"])
    median_charge_time = np.median(laadpaal_cleaned["ChargeTime"])
    print("Mean charge time:", mean_charge_time)
    print("Median charge time:", median_charge_time)

    x = [laadpaal_cleaned["ChargeTime"]]
    group_labels = ['Laadtijd']
    colors = ['mediumvioletred']

    fig = ff.create_distplot(x, group_labels, colors=colors, show_rug=False, bin_size=0.2)

    #Annotaties en lijntjes van de mean en median
    fig.add_vline(x=mean_charge_time, line_color="black", line_dash="dash")
    fig.add_annotation(x=mean_charge_time, y=0.3, text="<b>Gemiddelde laadtijd 2.49 uur</b>", 
                    showarrow=True, arrowhead=1, arrowcolor='black', ax=240, ay=0)

    fig.add_vline(x=median_charge_time, line_color="black", line_dash="dot")
    fig.add_annotation(x=median_charge_time, y=0.4, text="<b>Mediaan laadtijd 2.23 uur</b>", 
                    showarrow=True, arrowhead=1, arrowcolor='black', ax=220, ay=0)

    fig.update_layout(
        title="Histogram van laadtijden elektrische auto's met benadering kansdichtheidsfunctie",
        autosize=False,
        width=800,
        height=700,
        xaxis_title= "Laadtijd (Uren)",
        yaxis_title= "Dichtheid",
        xaxis=dict(
            range=[min(laadpaal_cleaned["ChargeTime"]), max(laadpaal_cleaned["ChargeTime"])],
            rangemode='normal', rangeselector=dict(
                buttons=list([
                    dict(count=0, label='0', step='hour', stepmode='backward'),
                    dict(count=10, label='10', step='hour', stepmode='backward'),
                    dict(count=20, label='20', step='hour', stepmode='backward'),
                    dict(count=30, label='30', step='hour', stepmode='backward'),
                    dict(count=40, label='40', step='hour', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )

    st.plotly_chart(fig)
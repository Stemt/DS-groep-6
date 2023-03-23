import pandas as pd
from sodapy import Socrata
import case_3_api as c3api
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from statsmodels.formula.api import ols
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objects as go 

def merken_grafiek():
    st.title("Merk Statistieken")
    st.markdown("## Datacleaning Proces")
    st.image("flowchart.png")
    #inladen brandstof dataset
    brandstof_elektrisch = c3api.get_RDW_brandstof(limit=3000000,offset=0, where="brandstof_omschrijving='Elektriciteit'")
    #filteren brandstof dataset
    filtered_brandstof_elektrisch = brandstof_elektrisch[["kenteken", "brandstof_volgnummer", "brandstof_omschrijving", "emissiecode_omschrijving",
                                                      "klasse_hybride_elektrisch_voertuig", "uitlaatemissieniveau", "geluidsniveau_rijdend",
                                                       "nominaal_continu_maximumvermogen", "netto_max_vermogen_elektrisch", "max_vermogen_60_minuten", 
                                                       "milieuklasse_eg_goedkeuring_licht", "elektrisch_verbruik_enkel_elektrisch_wltp", "actie_radius_enkel_elektrisch_wltp",
                                                       "actie_radius_enkel_elektrisch_stad_wltp"
                                                      ]]
    filtered_brandstof_elektrisch.shape

    #selectie van kolommen voor importeren RDW kenteken dataset
    kenteken_columns = 'kenteken, voertuigsoort, merk, handelsbenaming,datum_tenaamstelling,inrichting, massa_ledig_voertuig, datum_eerste_toelating, datum_eerste_tenaamstelling_in_nederland, wam_verzekerd,europese_voertuigcategorie, vermogen_massarijklaar, export_indicator, tenaamstellen_mogelijk'
    kenteken_df = c3api.get_RDW_kenteken_df(limit = 2000000, select = kenteken_columns, where ="voertuigsoort='Personenauto'", order = "datum_eerste_toelating DESC")
    #filteren kenteken dataset
    kenteken_filtered = kenteken_df.copy()
    #mergen van datasets
    kenteken_brandstof = pd.merge(kenteken_filtered, filtered_brandstof_elektrisch, how = "inner", on = "kenteken")

    kenteken_brandstof[["datum_tenaamstelling", "datum_eerste_toelating", "datum_eerste_tenaamstelling_in_nederland"]] = kenteken_brandstof[["datum_tenaamstelling", "datum_eerste_toelating", "datum_eerste_tenaamstelling_in_nederland"]].apply(pd.to_datetime, format = "%Y%m%d")

    # nieuwe dataset met alleen bedrijfsauto's en personenauto's 
    new_kenteken_brandstof = kenteken_brandstof[(kenteken_brandstof["voertuigsoort"] == "Bedrijfsauto") | (kenteken_brandstof["voertuigsoort"] == "Personenauto")]

    top5 = new_kenteken_brandstof.groupby("merk").size().sort_values(ascending = False).head(5).index.tolist()
    top5_df = new_kenteken_brandstof[new_kenteken_brandstof["merk"].isin(top5)].reset_index()
    top5_df.dropna(subset = ["datum_eerste_toelating"], inplace = True)

    top5_df["jaar"] = pd.to_datetime(top5_df["datum_eerste_toelating"]).dt.year
    top5_df["maand"] = pd.to_datetime(top5_df["datum_eerste_toelating"]).dt.month

    filtered_top5_df = top5_df[(top5_df["jaar"] >= 2000) & (top5_df["jaar"] <= 2022)]

    aantal_merk = filtered_top5_df.groupby(["merk","jaar", "maand"]).size().reset_index(name = "aantallen")
    def year_month_to_date(row):
        return f"{row['jaar']}-{row['maand']}"

    aantal_merk["datum"] = pd.to_datetime(aantal_merk.apply(year_month_to_date,axis=1),format='%Y-%m')

    df = aantal_merk


    color_map = {'AUDI': 'red', 'HYUNDAI': 'blue', 'KIA': 'green', 'TESLA': 'orange', 'TOYOTA': 'purple'}
    # traces
    traces = []
    for brand in df['merk'].unique():
        brand_data = df[df['merk'] == brand]
        trace = go.Scatter(x=brand_data['datum'], y=brand_data['aantallen'],
                            mode='lines', name=brand, line=dict(color=color_map[brand]))
        traces.append(trace)

    #layout
    layout = go.Layout(title='Voertuig aantallen per merk per jaar',
                   xaxis=dict(title='Datum'),
                   yaxis=dict(title='Aantal voertuigen'),
                   xaxis_rangeslider_visible=True)

    # object
    fig = go.Figure(data=traces, layout=layout)

    # figure
    st.header("Aantal voertuigen per merk")
    st.markdown("De datums waarin de voertuigen voorkomen in de dataset zijn gebaseerd op de eerste toelating, waarbij het voertuig voor het eerst op kenteken is gezet. De grafiek laat zien dat er voornamelijk een steiging in 2019 was. Vooral Tesla zag heeft een aanzienelijke stijging in 2019. Verder is de impact van corona en het chiptekort te zien door middel van de daling richting 2020. In 2021 stijgt het aantal voertuigen lichtelijk en in 2022, waar er nog steeds een chiptekort is, blijven het aantal voertuigen gelijk aan 2021.")
    st.plotly_chart(fig)
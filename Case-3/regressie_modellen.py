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

def regressie_modellen():
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

    regressie_df = top5_df[(top5_df["jaar"] >= 2018) & (top5_df["jaar"] <= 2022)]
    vermogen_geluid = regressie_df.copy()
    vermogen_geluid.dropna(subset = "geluidsniveau_rijdend", inplace = True)
    vermogen_geluid.dropna(subset = "elektrisch_verbruik_enkel_elektrisch_wltp", inplace = True)

    data = vermogen_geluid[['vermogen_massarijklaar', 'geluidsniveau_rijdend', 'massa_ledig_voertuig', 'elektrisch_verbruik_enkel_elektrisch_wltp']]

    data = data.astype(float) # convert columns to float data type

    X = sm.add_constant(data[['vermogen_massarijklaar', 'massa_ledig_voertuig']])

    y = data['elektrisch_verbruik_enkel_elektrisch_wltp']

    model = sm.OLS(y, X).fit()


    data = data[data.elektrisch_verbruik_enkel_elektrisch_wltp != 525]

    fig2 = px.scatter(data, x= "vermogen_massarijklaar", y="elektrisch_verbruik_enkel_elektrisch_wltp", trendline="ols", title = "Lineare regressie van vermogen en bereik")
    fig2.update_traces(line_color='#0000ff', line_width=2)
    fig2.update_traces(marker=dict(color='red'))
    fig2.update_layout(xaxis=dict(title='Vermogen massarijklaar (Kw)'),
                   yaxis=dict(title='Bereik (km)'))
    st.header("Regressiemodellen")
    st.markdown("De grafieken laten de voorspelling met de onafhankelijke variablen vermogen en massa van het voertuig en de afhankelijke variabelen bereik van het voertuig. Te zien is dat het vermogen en het gewicht toenemen, het bereik ook hoger wordt. Een mogelijke verklaring hiervoor zou zijn dat zwaardere voertuigen en voertuigen met meer vermogen een krachtigere accu hebben. De model summary laat zien dat het vermogen de meeste invloed heeft. Als laatste heeft het model een R-waarde van 0.872.")
    st.plotly_chart(fig2)

    fig3 = px.scatter(data, x= "massa_ledig_voertuig", y="elektrisch_verbruik_enkel_elektrisch_wltp", trendline="ols", title = "Lineare regressie van massa en bereik")

    fig3.update_traces(line_color='#0000ff', line_width=2)
    fig3.update_traces(marker=dict(color='red'))
    fig3.update_layout(xaxis=dict(title='Massa ledig voertuig (kg)'),
                   yaxis=dict(title='Bereik (km)'))
    st.plotly_chart(fig3)
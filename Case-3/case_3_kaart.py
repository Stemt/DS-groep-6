import case_3_api as c3api
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def kaart():
    ocm_json = c3api.get_OCM_json(10000)
    # ocm_json
    ocm_df = pd.json_normalize(ocm_json)
    ocm_fix = ocm_df.copy()
    ocm_fix = ocm_fix.dropna(subset='AddressInfo.Town')


    st.title("Town based map")
    towns = ocm_fix.groupby("AddressInfo.Town").count().sort_values('ID',ascending=False)[:100].index.tolist()

    # towns = ocm_df['AddressInfo.Town'].dropna()
    # st.write(towns)


    towns.insert(1,'All')
    selected_town = st.selectbox('select town',towns)

    avg_lat = 52.232385
    avg_lng =  5.270822
    if selected_town != 'All':
        town_chargers = ocm_fix[ocm_fix['AddressInfo.Town'] == selected_town]
        avg_lat = town_chargers['AddressInfo.Latitude'].sum() / town_chargers['AddressInfo.Latitude'].count()
        avg_lng = town_chargers['AddressInfo.Longitude'].sum() / town_chargers['AddressInfo.Longitude'].count()
        

    map = folium.Map(location=[avg_lat, avg_lng],tiles="Stamen Toner")


    ocm_fix['NumberOfPoints'] = ocm_fix['NumberOfPoints'].fillna(1)

    charger_level_color_map = ['grey','blue','orange','red']
    charger_level_groups = [None,folium.FeatureGroup('Level 1: Low (Under 2kW)'),folium.FeatureGroup('Level 2 : Medium (Over 2kW)'),folium.FeatureGroup('Level 3:  High (Over 40kW)')]


    for row in ocm_fix.iloc:
        if row['AddressInfo.Town'] != selected_town and selected_town != 'All':
            continue
        charger_table = pd.json_normalize(row['Connections'])
        if "Level.ID" in charger_table.columns:
            charger_level_count = charger_table.groupby('Level.ID').count()['ID']
            for level in charger_level_count.keys():
                folium.Circle(
                    location=[row['AddressInfo.Latitude'],row['AddressInfo.Longitude']],
                    radius=int(charger_level_count[level])*10,
                    color=charger_level_color_map[int(level)],
                    tooltip=charger_table,
                    fill=True,
                ).add_to(charger_level_groups[int(level)])

    for group in charger_level_groups:
        if group:
            group.add_to(map)

    folium.map.LayerControl('topleft',collapsed=False).add_to(map)

    folium_static(map,width=800)


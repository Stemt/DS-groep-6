import case_3_api as c3api
import case_3_kaart
import laadpaal_statistiek
import streamlit as st
import os

os.chdir(os.path.dirname(__file__))


with st.sidebar:
    st.title('Dashboard Populariteit Elektrische Auto\'s')
    page = st.radio(
    "Inhoudsopgave",
    ('Merk Statistieken', 'Geografische spreiding van laadstations', 'Laadpaal Statistieken','Trends'))

if page == 'Merk Statistieken':
    st.write("place holder")
elif page == 'Geografische Spreiding van Laadstations':
    case_3_kaart.kaart()
elif page == 'Laadpaal Statistieken':
    laadpaal_statistiek.laadpaal_stats()
elif page == 'Trends':
    st.write("place holder")


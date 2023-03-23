import case_3_api as c3api
import case_3_kaart
import streamlit as st



with st.sidebar:
    page = st.radio(
    "What\'s your favorite movie genre",
    ('Merk Statistieken', 'Geografische spreiding van laadstations', 'Laadpaal Statistieken','Trends'))

if page == 'Merk Statistieken':
    st.write("place holder")
elif page == 'Geografische spreiding van laadstations':
    case_3_kaart.kaart()
elif page == 'Laadpaal Statistieken':
    st.write("place holder")
elif page == 'Trends':
    st.write("place holder")


import case_3_api as c3api
import case_3_kaart
import laadpaal_statistiek
import os

st.write(os.listdir('.'))
st.write(os.listdir('./data'))


laadpaal_statistiek.laadpaal_stats()

case_3_kaart.kaart()


print(c3api.get_RDW_brandstof(100).head())
print(c3api.get_RDW_kenteken_df(100).head())
print(c3api.get_OCM_df(100).head())

import case_3_api as c3api
import case_3_kaart


case_3_kaart.kaart()

import laadpaal_statistiek

print(c3api.get_RDW_brandstof(100).head())
print(c3api.get_RDW_kenteken_df(100).head())
print(c3api.get_OCM_df(100).head())

import requests
import pandas as pd
from sodapy import Socrata


# oldkey: 93b912b5-9d70-4b1f-960b-fb80a4c9c017

def get_OCM_json(maxresults,key = "acd9617c-3a34-4421-a5d8-6e1edd278a16"):
    resp = requests.get(f"https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults={maxresults}&compact=true&verbose=false&key={key}")
    return resp.json()

def get_OCM_df(limit):
    responsejson  = get_OCM_json(1000)


    ###Dataframe bevat kolom die een list zijn. 
    #Met json_normalize zet je de eerste kolom om naar losse kolommen
    Laadpalen = pd.json_normalize(responsejson)
    #Daarna nog handmatig kijken welke kolommen over zijn in dit geval Connections
    #Kijken naar eerst laadpaal op de locatie
    #Kan je uitpakken middels:
    df4 = pd.json_normalize(Laadpalen.Connections)
    df5 = pd.json_normalize(df4[0])
    df5.head()
    ###Bestanden samenvoegen
    Laadpalen = pd.concat([Laadpalen, df5], axis=1)
    return Laadpalen

# https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen/m9d7-ebf2
def get_RDW_kenteken_df(limit,offset=0,where="",select="",order=""):
    try:
        results_df = pd.read_csv("rdw_kenteken.csv")
    except:
        client = Socrata("opendata.rdw.nl", None)
        results = client.get("m9d7-ebf2", limit=limit,offset=offset,where=where,select=select,order=order)
        results_df = pd.DataFrame.from_records(results)
        results_df.to_csv("rdw_kenteken.csv")
    return results_df

# https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen_brandstof/8ys7-d773
def get_RDW_brandstof(limit,offset=0,where="", select=""):
    try:
        results_df = pd.read_csv("rdw_brandstof.csv")
    except:
        client = Socrata("opendata.rdw.nl", None)
        results = client.get("8ys7-d773", limit=limit,offset=offset,where=where,select=select)
        results_df = pd.DataFrame.from_records(results)
        results_df.to_csv("rdw_brandstof.csv")
    return results_df


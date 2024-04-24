# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import geoplot as gplt
from mpl_toolkits.basemap import Basemap
import geoplot.crs as gcrs
import plotly.graph_objects as go

# Auxiliar variables
pop = {"COLOMBIA": 50000000, "META": 1115000, "VILLAVICENCIO": 570000, "ACACIAS": 100000, "PUERTO GAITAN": 45000}
years = range(2013,2022)
cases = {"Gases":412, "Medicamentos":370, "Metales Pesados":390, "Metanol":380, "Otras Sustancias químicas":410, 
        "Plaguicidas":360, "Solventes":400, "Sustancias Psicoactivas":414}
vars = ["FEC_NOT","COD_EVE","SEMANA", "EDAD", "nombre_nacionalidad", "SEXO", "Departamento_ocurrencia", "Municipio_ocurrencia", "CON_FIN" ]

# Auxiliar functions
# Data reshaper functions
def reshape_fin(x):
    return x-1

def reshape_nationality(x):
    if "COLOMBIA" in x:
        return "COLOMBIA"
    else:
        return x.rstrip()

def calculate_center(df):
    """
    Calculate the centre of a geometry
    This method first converts to a planar crs, gets the centroid
    then converts back to the original crs. This gives a more
    accurate centre point for the geometry.
    """
    original_crs = df.crs
    planar_crs = 'EPSG:3857'
    return df['geometry'].to_crs(planar_crs).centroid.to_crs(original_crs)
    
  

# Data cleaning function
def clean_db(df):
    df = df.loc[:,vars]
    df.fillna(0, inplace=True)
    newFin = df["CON_FIN"].apply(reshape_fin)
    df["CON_FIN"] = newFin
    newNac= df["nombre_nacionalidad"].apply(reshape_nationality)
    df["nombre_nacionalidad"] = newNac
    df["FEC_NOT"] = pd.to_datetime(df["FEC_NOT"], format='%Y-%m-%d', errors='coerce')
    return df

# Data filter function
def onlyMeta(df):
    df = df[df["Departamento_ocurrencia"].str.contains("META")]
    df = df[df["Municipio_ocurrencia"].str.contains("VILLAVICENCIO|ACACIAS|PUERTO GAITAN") == False]
    return df

def onlyMetaMap(df):
    df = df[df["nombre_dpt"].str.contains("META")]
    return df

def onlyPlag(df):
    df = df[df["COD_EVE"] == 360]
    return df

# Read the data of 2022 for national and departmental context in chemical security
contextN = pd.DataFrame()
contextD = pd.DataFrame()
for case in cases:
    name = "Datos_2022_"+str(cases[case]) + '.xls'
    df = pd.read_excel('./DB/'+ str(cases[case]) + '/' + name )
    df = pd.DataFrame(df)
    df = clean_db(df)
    contextN = pd.concat([contextN, df], ignore_index=True)

contextD = onlyMeta(contextN)
plaN = onlyPlag(contextN)
plaD = onlyPlag(contextD)

# Save the data
contextN.to_csv('./DB/2022.csv', index=False)
contextD.to_csv('./DB/2022_Meta.csv', index=False)

plaN.to_csv('./DB/2022_Plag.csv', index=False)
plaD.to_csv('./DB/2022_Plag_Meta.csv', index=False)

print(plaD.info())

#Map from the Meta Department
mapData = gpd.read_file("./maps/shapes.geojson")
mapData = onlyMetaMap(mapData)
print(mapData.info())
mapData["center"] = calculate_center(mapData)
mapData["Longitude"] = [val.x for val in mapData.center]
mapData["Latitude"] = [val.y for val in mapData.center]

print(mapData["center"])

#create a map using geoplot
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
map = gplt.polyplot(mapData, ax=ax)

#add markers to the map for each municipality
for i in range(len(mapData)):
    ax.plot(mapData["Longitude"],mapData["Latitude"] , marker='o', color='red', linewidth=0, markersize=5)



plt.show()



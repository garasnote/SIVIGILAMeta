# Imports
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from reshape import calculate_center
import matplotlib.colors as mcolors
import geoplot as gplt
import imageio as iio
import numpy as np


def onlyMetaMap (df)-> pd.DataFrame:
    df = df[df["nombre_dpt"].str.contains("META")]
    return df


def draw(df: pd.DataFrame, pop: pd.DataFrame, years:range) -> None:
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    plt.rcParams["savefig.dpi"] = 300
    
    #Map from the Meta Department
    mapData = gpd.read_file("./maps/shapes.geojson")
    mapData = onlyMetaMap(mapData)
    mapData["center"] = calculate_center(mapData)
    mapData["Longitude"] = [val.x for val in mapData.center]
    mapData["Latitude"] = [val.y for val in mapData.center]
    mapData.at[1043, "nombre_cab"] = "CUBARRAL"
    mun = mapData["nombre_cab"].to_list()
    mun = [x.upper() for x in mun]
    mapData.set_index(['nombre_cab'], inplace=True)
    
    #Morbility rate maps
    for year in years:
        for m in mun:
            popMun = pop.loc[pop["TERRITORIO"].str.contains(m)]
            popYear =popMun.loc[popMun["ANO"]==year]
            popEstudio = popYear.iloc[0,2]
            count = df.loc[(df["Municipio_ocurrencia"].str.contains(m)) &(df["ANO"]==year)].value_counts().sum()
            rate = count/popEstudio*100000
            mapData.at[m, str(year)] = rate
        plt.figure( num=year)
        mapData.plot(column=str(year), cmap="GnBu", edgecolor="black", legend=True, legend_kwds={'label': "Tasa de morbilidad por cada 100.000 habitantes", 'orientation': "horizontal"})
        plt.title("Morbilidad de EIS con Plaguicidas en los municipios del Meta en el año " + str(year))
        plt.axis('off')
        plt.savefig("./maps/morb/Meta_" + str(year) + ".png")
        plt.close()
    mapData.to_csv("./maps/mapDataMorb.csv")
    frames = np.stack([iio.imread("./maps/morb/Meta_" + str(year) + ".png") for year in years], axis=0)
    iio.mimsave("./maps/morb/Meta.gif", frames, fps=1, loop=0)
    
    #Mortality rate maps
    for year in years:
        for m in mun:
            popMun = pop.loc[pop["TERRITORIO"].str.contains(m)]
            popYear =popMun.loc[popMun["ANO"]==year]
            popEstudio = popYear.iloc[0,2]
            count = df.loc[(df["Municipio_ocurrencia"].str.contains(m)) &(df["ANO"]==year) & df["CON_FIN"]==1].value_counts().sum()
            rate = count*100000/popEstudio
            mapData.at[m, str(year)] = rate
        plt.figure( num=year)
        mapData.plot(column=str(year), cmap="OrRd", edgecolor="black", legend=True, legend_kwds={'label': "Tasa de mortalidad por cada 100.000 habitantes", 'orientation': "horizontal"})
        plt.title("Mortalidad de EIS con Plaguicidas en los municipios del Meta en el año " + str(year))
        plt.axis('off')
        plt.savefig("./maps/mort/Meta_" + str(year) + ".png")
        plt.close()
    mapData.to_csv("./maps/mapDataMort.csv")
    frames = np.stack([iio.imread("./maps/mort/Meta_" + str(year) + ".png") for year in years], axis=0)
    iio.mimsave("./maps/mort/Meta.gif", frames, fps=1, loop=0)

        
    
if __name__ == "__main__":
        draw()
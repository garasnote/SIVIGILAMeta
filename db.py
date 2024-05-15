# Imports
import pandas as pd
from reshape import reshape_fin, reshape_bool
# Variables of interest
RIPS = ["Departamento", "Municipio", "Año","Diagnostico", "NumeroAtenciones"]
ICEinterest = ["X4", "X6", "X85","X86", "X87", "X88" "X89", "X90", "Y1", "T60"]
SIVIGILA = ["COD_EVE","ANO", "EDAD", "SEXO", "Departamento_ocurrencia", "Municipio_ocurrencia", "CON_FIN",
            "AREA", "OCUPACION", "TIP_SS"  , "PER_ETN" ,"GP_DISCAPA" ,"GP_DESPLAZ" , "GP_MIGRANT" , "GP_GESTAN" , "GP_DESMOVI",
            "GP_VIC_VIO","PAC_HOS","CBMTE"
            ]
SIVIGILA_bool = ["GP_DISCAPA" ,"GP_DESPLAZ" , "GP_GESTAN" , "GP_DESMOVI", "GP_VIC_VIO", "PAC_HOS", "GP_MIGRANT"]
years_SIVIGILA = range(2013,2022+1)

# Data cleaning function
def clean_SIVIGILA(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(df)
    #Only study the variables of interest
    df = df.loc[:,SIVIGILA]
    
    #Mortality variable
    newFin = df["CON_FIN"].apply(reshape_fin)
    df["CON_FIN"] = newFin
    
    #Boolean variables
    for var in SIVIGILA_bool:
        newVar = df[var].apply(reshape_bool)
        df[var] = newVar
    
    #Fill the NaN values with 0
    df.fillna(0, inplace=True)
    
    #Variable with the explanation (based on numeric or categoric variables)
    df["CASE"] = df["COD_EVE"].apply(lambda x: "Gases" if x == 412 else "Medicamentos" if x == 370 else "Metales Pesados" if x == 390 else "Metanol" if x == 380 else "Plaguicidas" if x == 360 else "Solventes" if x == 400 else "Sustancias Psicoactivas" if x == 414 else "Otras Sustancias químicas" if x == 410 else "Otros")
    df["AREA_txt"] = df["AREA"].apply(lambda x: "Cabecera Municipal" if x == 1 else "Centro Poblado" if x == 2 else "Rural Disperso" if x == 3 else "ZZZDesconocido")
    df["Regimen_Salud"] = df["TIP_SS"].apply(lambda x: "Contributivo" if x == "C" else "Subsidiado" if x == "S" else "Excepcion" if x == "P" else "Especial" if x == "E" else "No Asegurado" if x == "N" else  "Indeterminado/Pendiente" if x == "I" else "ZZZDesconocido")
    df["Pertenece"] = df["PER_ETN"].apply(lambda x: "Indígena" if x == 1 else "ROM" if x == 2 else "Raizal" if x==3 else "Palenquero" if x == 4 else "Afrocolombiano" if x == 5 else "Otro" if x == 6 else "ZZZDesconocido")
    
    #Drop the rows with unknown municipality (4 in the plaguicidas case)
    df.drop(df[df['Municipio_ocurrencia'] == "* META. MUNICIPIO DESCONOCIDO"].index, inplace = True)
    
    return df

def RIPS_Meta(df: pd.DataFrame, dptoInterest:str) -> pd.DataFrame:
    df = df.loc[df["Departamento"].str.contains(dptoInterest)]
    ans = df.loc[:,RIPS]
    ans.rename(columns={"Departamento":"Dpto", "Año":"ANO"}, inplace=True)
    return ans

def RIPS_Interest(df: pd.DataFrame, ICEinterest: list) -> pd.DataFrame:
    ans = pd.DataFrame()
    for inter in ICEinterest:
        ans = pd.concat([ans, df.loc[df["Diagnostico"].str.contains(inter)]])
    ans = ans.loc[:,RIPS]
    ans.rename(columns={"Departamento":"Dpto", "Año":"ANO"}, inplace=True)
    return ans

def RIPS_Meta_Interest(df: pd.DataFrame, ICEinterest: list) -> pd.DataFrame:
    ans = pd.DataFrame()
    RIPS = ["Dpto", "Municipio", "ANO","Diagnostico", "NumeroAtenciones"]
    for inter in ICEinterest:
        ans = pd.concat([ans, df.loc[df["Diagnostico"].str.contains(inter)]])
    ans = ans.loc[:,RIPS]
    return ans

def RIPS_FirstTri(df: pd.DataFrame) ->pd.DataFrame:
    print(df.columns)
    mustInt = ["DEP", "MUN", "TIPO_SS", "EDAD", "MED_EDAD", "CON_FIN"]
    df = df.fillna("0")
    for i in mustInt:
        df[i] = pd.to_numeric(df[i], errors='coerce')
        df[i] = df[i].astype(int)
    return df

# Data filter function
def onlyMeta(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["Departamento_ocurrencia"].str.contains("META")]
    return df
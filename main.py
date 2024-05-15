# Imports
import pandas as pd
from read_db import *
from graph import *
from map import *
# Auxiliar variables
DptoInterest = "50"
ICEinterest = ["X4", "X6", "X85","X86", "X87", "X88", "X89", "X90", "Y1", "T60"]
ICEinterest_Plag = ["X48","X68", "X87", "Y18", "T60"]
SIVIGILA = ["COD_EVE","ANO", "EDAD", "SEXO", "Departamento_ocurrencia", "Municipio_ocurrencia", "CON_FIN",
            "AREA", "OCUPACION", "TIP_SS"  , "PER_ETN" ,"GP_DISCAPA" ,"GP_DESPLAZ" , "GP_MIGRANT" , "GP_GESTAN" , "GP_DESMOVI",
            "GP_VIC_VIO","PAC_HOS","CBMTE"
            ]
RIPS = ["Departamento", "Municipio", "Año","Diagnostico", "NumeroAtenciones"]
cases = {"Plaguicidas":360}
years = range(2013,2022+1)
pop = {"COLOMBIA": {2013:45434942,2014:45866010,2015:46313898,2016:46830116, 2017:47419200, 2018:48258494, 2019:49395678, 
       2020:50407647, 2021:51117378, 2022:51682692}, "META": {2013:952101,2014:969808,2015:987232,2016:1004633, 2017:1021943, 2018:1039722, 2019:1052125, 
       2020:1082032, 2021:1098104, 2022:1113810}}

mun = ["Villavicencio","Calvario","San Juanito","Restrepo","Cumaral",
            "Acacias","Guamal","Cubarral","Dorado","Castilla","San Carlos",
            "Barranca","Cabuyaro","Puerto Lopez","Puerto Gaitan",
            "Puerto Rico", "Puerto Concordia", "Mapiripan",
            "Castillo","Lejanias","San Juan de Arama","Granada","Fuente De Oro",
            "San Martin","Puerto Lleras",
            "Uribe","Mesetas","VistaHermosa","Macarena"]

# Read the databases or write them in the case they are not saved already
# RIPS database 
# 

# SIVIGILA database National + Meta

def unused(contextN:pd.DataFrame, contextD: pd.DataFrame)->None:
       # Read SIVIGILA
       years = range(2013,2022+1)
       [contextN, contextD]=read_SIVIGILA(cases, years)
       morbilityEvolution(contextN, contextD,years,cases, pop)
       mortalityEvolution(contextN, contextD,years,cases, pop)
       # Read Pop for rate calculation
       pop = pd.read_csv('./DB/original/Pop.csv', dtype={'TERRITORIO':str, 'ANO':int, 'POBLACION':int})
       demographic(contextD, years, pop)
       
       #Read RIPS
       years = range(2009,2021+1)
       RIPSNacional = pd.read_csv('./DB/cleaned/RIPS/RIPSNacional.csv')
       RIPSDepartamental = pd.read_csv('./DB/cleaned/RIPS/RIPSDepartamental_Interest.csv')
       RIPS_evolution(RIPSNacional, years)
       RIPS_evolution(RIPSDepartamental, years)

       # Demographic generation
       years = range(2013,2022+1)
       [contextN, contextD]=read_SIVIGILA(cases, years)
       pop = pd.read_csv('./DB/original/Pop.csv', dtype={'TERRITORIO':str, 'ANO':int, 'POBLACION':int})
       demographic(contextD, years, pop)

       # Searching specific variables 
       pendientes = ["OCUPACION", "CBMTE"]
       for pen in pendientes:
              saver = contextD[pen].value_counts()
              saver.to_csv("./DB/cleaned/SIVIGILA/interest/" + pen + ".csv")

       demographic(contextD, years, pop)
       
       pop = {"COLOMBIA": {2013:45434942,2014:45866010,2015:46313898,2016:46830116, 2017:47419200, 2018:48258494, 2019:49395678, 
       2020:50407647, 2021:51117378, 2022:51682692}, "META": {2013:952101,2014:969808,2015:987232,2016:1004633, 2017:1021943, 2018:1039722, 2019:1052125, 
       2020:1082032, 2021:1098104, 2022:1113810}}
       morbilityEvolution(contextN,contextD,years,cases,pop)
       mortalityEvolution(contextN,contextD,years,cases,pop)

       

       total = Read_RIPS_trim(ICEinterest_Plag)
       RIPS_trim_graph(total)
       columns = total.columns
       columnsInterest = [x for x in columns if "ICE" in x]      
       ICEs = total[columnsInterest].value_counts()
       ICEs.to_csv("./DB/cleaned/RIPS/T1/ICEsCount.csv")
       


       

def main()->None:

       # Read SIVIGILA
       years = range(2013,2022+1)
       [contextN, contextD]=read_SIVIGILA(cases, years)
       pop = pd.read_csv('./DB/original/Pop.csv', dtype={'TERRITORIO':str, 'ANO':int, 'POBLACION':int})
       draw(contextD, pop, years)
       

       

       
       
if __name__ == "__main__":
       main()
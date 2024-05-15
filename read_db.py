# Imports
from typing import Union
import pandas as pd
import os
from db import *

############################################################################################################
                                                    #SIVIGILA
############################################################################################################

# Read the data for national and departmental context in chemical security, only if it hasn't been saved before
def read_SIVIGILA(cases: Union[int,dict], years: Union[int, range],) -> list[pd.DataFrame, pd.DataFrame]:
    Years = type(years)
    Cases = type(cases)
    contextSaver = []
    if Years == int and Cases == int:
        contextSaver = SIVIGILA_1(cases, years)
    if Years == int and Cases == dict:
        contextSaver = SIVIGILA_2(cases, years)
    if Years == range and Cases == int:
        contextSaver = SIVIGILA_3(cases, years)
    else:
        contextSaver = SIVIGILA_4(cases, years)
    return contextSaver        
#Possible variable types:
def SIVIGILA_1(cases: int, years: int) -> list[pd.DataFrame, pd.DataFrame]:
    contextN = pd.DataFrame()
    contextD = pd.DataFrame()
    name = f'./DB/original/SIVIGILA/{cases}/Datos_{years}_{cases}.xls'
    data = pd.read_excel(name)
    data = clean_SIVIGILA(data)
    contextN = pd.concat([contextN, data], ignore_index=True)
    contextD = onlyMeta(contextN)
    contextSaver = [contextN, contextD]
    contextN.to_csv(f'./DB/cleaned/SIVIGILA/{years}/{cases}.csv', index=False)
    contextD.to_csv(f'./DB/cleaned/SIVIGILA/{years}/{cases}_Meta.csv', index=False)
    return contextSaver

def SIVIGILA_2(cases: dict, years: int) -> list[pd.DataFrame, pd.DataFrame]:
    contextN = pd.DataFrame()
    contextD = pd.DataFrame()
    for case in cases:
        name = './DB/original/SIVIGILA/' + str(cases[case]) + f'/Datos_{years}_' + str(cases[case]) + '.xls'
        data = pd.read_excel(name)
        data = clean_SIVIGILA(data)
        print(f'{years} - {case}')
        contextN = pd.concat([contextN, data], ignore_index=True)
        contextD = onlyMeta(contextN)
        contextSaver = [contextN, contextD]
        contextN.to_csv(f'./DB/cleaned/SIVIGILA/{years}/interest.csv', index=False)
        contextD.to_csv(f'./DB/cleaned/SIVIGILA/{years}/interest_Meta.csv', index=False)
        return contextSaver
    
def SIVIGILA_3(cases:int,years:range)-> list[pd.DataFrame, pd.DataFrame]:
    contextN = pd.DataFrame()
    contextD = pd.DataFrame()
    for year in years:
        name = f'./DB/original/SIVIGILA/{cases}/Datos_{year}_{cases}.xls'
        data = pd.read_excel(name)
        print(f'{year} - {cases}')
        data = clean_SIVIGILA(data)
        contextN = pd.concat([contextN, data], ignore_index=True)
        contextD = onlyMeta(contextN)
        contextSaver = [contextN, contextD]    
        directory = f'./DB/cleaned/SIVIGILA/{years[0]} - {years[-1]}'
        try:
            os.mkdir(directory)
        except:
            directory = directory
        contextN.to_csv(f'{directory}/{cases}.csv', index=False)
        contextD.to_csv(f'{directory}/{cases}_Meta.csv', index=False)
    return contextSaver    
            
def SIVIGILA_4(cases:dict,years:range)-> list[pd.DataFrame, pd.DataFrame]:
    contextN = pd.DataFrame()
    contextD = pd.DataFrame()
    for year in years:
        for case in cases:
            name = './DB/original/SIVIGILA/' + str(cases[case]) + f'/Datos_{year}_' + str(cases[case]) + '.xls'
            data = pd.read_excel(name)
            data = clean_SIVIGILA(data)
            contextN = pd.concat([contextN, data], ignore_index=True)
            print(f'{year} - {case}')
    contextD= onlyMeta(contextN)
    contextN.to_csv(f'./DB/cleaned/SIVIGILA/interest/interest.csv', index=False)
    contextD.to_csv(f'./DB/cleaned/SIVIGILA/interest/interest_Meta.csv', index=False) 
    contextSaver = [contextN, contextD]
    return contextSaver    

# Read the data for the RIPS database, only if it hasn't been saved before

def read_RIPS(DptoInterest: str, ICEinterest: list[str])-> pd.DataFrame:
    RIPS = pd.read_csv('./DB/original/RIPS/RIPS.csv', sep=',', encoding='UTF-8')
    RIPSNacional = RIPS_Interest(RIPS, ICEinterest)
    print("Created RIPSNacional_Interest")
    RIPSNacional.to_csv("./DB/cleaned/RIPS/RIPSNacional.csv", index=False)
    RIPSDepartamental = RIPS_Meta(RIPS, DptoInterest)
    RIPSDepartamental.to_csv("./DB/cleaned/RIPS/RIPSDepartamental.csv", index=False)
    print("Created RIPSDepartamental")
    RIPS = pd.DataFrame()
    RIPSID = RIPS_Meta_Interest(RIPSDepartamental, ICEinterest)
    RIPSID.to_csv("./DB/cleaned/RIPS/RIPSDepartamental_Interest.csv", index=False)
    print("Created RIPSDepartamental_Interest")


def Read_RIPS_trim(ICEinterest:list) ->pd.DataFrame:
    US = pd.read_csv("./DB/cleaned/RIPS/T1/US5000015_INS.csv")
    AH = pd.read_csv("./DB/cleaned/RIPS/T1/AH5000015_INS.csv")
    AU = pd.read_csv("./DB/cleaned/RIPS/T1/AU5000015_INS.csv")
    AC = pd.read_csv("./DB/cleaned/RIPS/T1/AC5000015_INS.csv")
    
    AU[["ICE_PRIN","ICE_REL1","ICE_REL2","ICE_REL3"]] = AU[["ICE_PRIN","ICE_REL1","ICE_REL2","ICE_REL3"]].fillna(" ")
    saver = pd.DataFrame()
    total = pd.DataFrame()
    
    for ICE in ICEinterest:
        PRIN = AU[AU["ICE_PRIN"].str.contains(ICE)]
        REL1 = AU[AU["ICE_REL1"].str.contains(ICE)]
        REL2 = AU[AU["ICE_REL2"].str.contains(ICE)]
        REL3 = AU[AU["ICE_REL3"].str.contains(ICE)]
        saver = pd.concat([saver, PRIN, REL1, REL2, REL3])
    saver = pd.merge(saver,US, on=["TIPO_ID","ID","DEP", "MUN","ZONA"], how="left")
    saver.to_csv("./DB/cleaned/RIPS/T1/AU5000015_INS_Interest.csv", index=False)
    
    
    total = pd.concat([total, saver])
    #18 URGENCIAS
    AC[["ICE_PRIN","ICE_REL1","ICE_REL2","ICE_REL3"]] = AC[["ICE_PRIN","ICE_REL1","ICE_REL2","ICE_REL3"]].fillna(" ")
    saver = pd.DataFrame()
    for ICE in ICEinterest:
        PRIN = AC[AC["ICE_PRIN"].str.contains(ICE)]
        REL1 = AC[AC["ICE_REL1"].str.contains(ICE)]
        REL2 = AC[AC["ICE_REL2"].str.contains(ICE)]
        REL3 = AC[AC["ICE_REL3"].str.contains(ICE)]
        saver = pd.concat([saver, PRIN, REL1, REL2, REL3])
    saver = pd.merge(saver,US, on=["TIPO_ID","ID","DEP", "MUN","ZONA"], how="left")
    saver.to_csv("./DB/cleaned/RIPS/T1/AC5000015_INS_Interest.csv", index=False)
    #125 consultas
    total = pd.concat([total, saver])
    AH[["ICE_ING","ICE_EGR","ICE_REL1","ICE_REL2","ICE_REL3", "ICE_REL4","ICE_MUER"]] = AH[["ICE_ING","ICE_EGR","ICE_REL1","ICE_REL2","ICE_REL3", "ICE_REL4","ICE_MUER"]].fillna(" ")
    saver = pd.DataFrame()
    for ICE in ICEinterest:
        ING = AH[AH["ICE_ING"].str.contains(ICE)]
        EGR = AH[AH["ICE_EGR"].str.contains(ICE)]
        REL1 = AH[AH["ICE_REL1"].str.contains(ICE)]
        REL2 = AH[AH["ICE_REL2"].str.contains(ICE)]
        REL3 = AH[AH["ICE_REL3"].str.contains(ICE)]
        REL4 = AH[AH["ICE_REL4"].str.contains(ICE)]
        MUER = AH[AH["ICE_MUER"].str.contains(ICE)]
        saver = pd.concat([saver, ING, EGR, REL1, REL2, REL3, REL4, MUER])
    saver = pd.merge(saver,US, on=["TIPO_ID","ID","DEP", "MUN","ZONA"], how="left")
    saver.to_csv("./DB/cleaned/RIPS/T1/AH5000015_INS_Interest.csv", index=False)
    total = pd.concat([total, saver])
    print(total.info())
    total = RIPS_FirstTri(total)
    total.to_csv("./DB/cleaned/RIPS/T1/Total_Interest.csv", index=False)
    print(total.info())

    #32 Hospitalizaciones
    return total



if __name__ == "__main__":

    pass

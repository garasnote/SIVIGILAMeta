import pandas as pd
import matplotlib.pyplot as plt
import math

cases = {"Plaguicidas":360, "Medicamentos":370, "Metanol":380,  "Metales Pesados":390,"Solventes":400, "Otras Sustancias químicas":410,
        "Gases":412, "Sustancias Psicoactivas":414}
years = range(2013,2022+1)
pop = {"COLOMBIA": {2013:45434942,2014:45866010,2015:46313898,2016:46830116, 2017:47419200, 2018:48258494, 2019:49395678, 
       2020:50407647, 2021:51117378, 2022:51682692}, "META": {2013:952101,2014:969808,2015:987232,2016:1004633, 2017:1021943, 2018:1039722, 2019:1052125, 
       2020:1082032, 2021:1098104, 2022:1113810}}

Nunito = "./DB/original/fonts/Nunito/NunitoRegular.ttf"
Nexa = "./DB/original/fonts/Nexa/NexaHeavy.ttf"

def morbilityEvolution(dfN, dfD,years,cases, pop) -> None:
    if len(cases) >=2:
        morbilityEvolutionAll(dfN, dfD,years,pop)
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    plt.figure(num=1)
    for case in cases:
        perCase = dfN.loc[(dfN['CASE'] == case)]
        totalNation = pd.DataFrame()
        for year in years:
            perYear = perCase.loc[(perCase["ANO"]==year)]
            if perCase.loc[(perCase["ANO"]==year)].value_counts().sort_values().empty:
                totalNation = pd.concat([totalNation, pd.Series(0, index=[year], name="count", dtype=int)])
            else:
                perYear = perCase.loc[(perCase["ANO"]==year)]
                totalNation = pd.concat([totalNation, perYear['ANO'].value_counts().sort_values(ascending=False)])
            totalNation = pd.concat([totalNation, perYear['ANO'].value_counts().sort_values(ascending=False)])
            totalNation["count" + f'{year}'] = rateCalc(totalNation['count'], pop["COLOMBIA"][year])
        print("Casos en Colombia:" + str(totalNation["count"].sum()))
        y1 = totalNation["count" + f'{year}']
        plt.plot(y1, label='Nacional', marker='o', markersize=7, linewidth=5, color='royalblue')
        perCase = dfD[dfD['CASE'] == case]
        totalDepartment = pd.DataFrame()
        for year in years:
            perYear = perCase.loc[(perCase["ANO"]==year)]
            if perCase.loc[(perCase["ANO"]==year)].value_counts().sort_values().empty:
                totalDepartment = pd.concat([totalDepartment, pd.Series(0, index=[year], name="count", dtype=int)])
            else:
                totalDepartment = pd.concat([totalDepartment, perYear['ANO'].value_counts().sort_values(ascending=False)])  
        print("Casos en el Meta:" + str(totalDepartment["count"].sum()))
        totalDepartment["count"] = rateCalc(totalDepartment['count'], pop["META"][year])
        y2 = totalDepartment["count"]
        plt.plot(y2, label='Departamento del Meta', marker='o', markersize=7, linewidth=5, color='green')
        plt.title(r'Comparativa de tasa de morbilidad por \textbf{'+ f'{case} '+ r'}'+ '\n' r'entre \textbf{' + f'{years[0]} - {years[-1]}' + r'}', fontsize=28)
        plt.ylabel(r'Eventos de interés por cada 100.000 habitantes', fontsize=20)
        plt.yticks(fontsize=18)
        plt.xlabel(r'Año', fontsize=20)
        plt.ylim(bottom=0)
        plt.xticks(years, fontsize=18)
        plt.legend(fontsize=18)
        plt.tight_layout()
        print("gráfica morbilidad de " + f"{case}")
        plt.savefig('./images/' + f'{case}'+ ' - Morbilidad'   +'.png', dpi=300)
        plt.close()

def morbilityEvolutionAll(dfN:pd.DataFrame, dfD:pd.DataFrame,years:range,pop:dict) ->None:
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    plt.figure(num=1)
    totalNation = pd.DataFrame()
    allCase = dfN
    for year in years:
        perYear = allCase.loc[(allCase["ANO"]==year)]
        totalNation = pd.concat([totalNation, perYear['ANO'].value_counts().sort_values(ascending=False)])
        totalNation["count" + f'{year}'] = rateCalc(totalNation['count'], pop["COLOMBIA"][year])
    y1 = totalNation["count" + f'{year}']
    plt.plot(y1, label = 'Nacional', marker ='o', markersize = 7, linewidth =5, color = 'royalblue')
    allCase = dfD
    totalDept = pd.DataFrame()
    for year in years:
        perYear = allCase.loc[(allCase["ANO"]==year)]
        totalDept = pd.concat([totalDept, perYear['ANO'].value_counts().sort_values(ascending=False)])
        totalDept["count" + f'{year}'] = rateCalc(totalDept['count'], pop["META"][year])
    y2 = totalDept["count" + f'{year}']
    plt.plot(y2,label='Departamento del Meta', marker = 'o', markersize=7, linewidth =5, color='green' )
    
    plt.title(r'Comparativa de tasa de morbilidad por \textbf{'+ "todos los eventos" + r'}'+ '\n' r'entre \textbf{' + f'{years[0]} - {years[-1]}' + r'}', fontsize=28)
    plt.ylabel(r'Eventos de interés por cada 100.000 habitantes', fontsize=20)
    plt.yticks(fontsize=18)
    plt.xlabel(r'Año', fontsize=20)
    plt.ylim(bottom=0)
    plt.xticks(years, fontsize=18)
    plt.legend(fontsize=18)
    plt.tight_layout()
    print("gráfica morbilidad de todos los eventos de interés")
    plt.savefig('./images/' + 'todos'+ ' - Morbilidad'   +'.png', dpi=300)
        
def mortalityEvolution(dfN:pd.DataFrame, dfD:pd.DataFrame,years:range,cases:dict,pop:dict) ->None:
    if len(cases) >=2:
        mortalityEvolutionAll(dfN, dfD,years,pop)

    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    plt.figure(num=1)
    for case in cases:
        perCase = dfN.loc[(dfN['CASE'] == case)&(dfN["CON_FIN"]==1)]
        totalNation = pd.DataFrame()
        for year in years:
            if perCase.loc[(perCase["ANO"]==year)& (perCase["CON_FIN"]==1)].value_counts().sort_values().empty:
                totalNation = pd.concat([totalNation, pd.Series(0, index=[year], name="count", dtype=int)])
            else:
                perYear = perCase.loc[(perCase["ANO"]==year)]
                totalNation = pd.concat([totalNation, perYear['ANO'].value_counts().sort_values(ascending=False)])
        print("Casos en Colombia con muertes:" + str(totalNation["count"].sum()))
        totalNation["count"] = rateCalc(totalNation['count'], pop["COLOMBIA"][year])
        y1 = totalNation["count"]
        plt.plot(y1, label='Nacional', marker='o', markersize=7, linewidth=5, color='royalblue')
        perCase = dfD[dfD['CASE'] == case]
        totalDepartment = pd.DataFrame()
        for year in years:
            if perCase.loc[(perCase["ANO"]==year)& (perCase["CON_FIN"]==1)].value_counts().sort_values().empty:
                totalDepartment = pd.concat([totalDepartment, pd.Series(0, index=[year], name="count", dtype=int)])
            else:
                perYear = perCase.loc[(perCase["ANO"]==year) & (perCase["CON_FIN"]==1)]
                totalDepartment = pd.concat([totalDepartment, perYear['ANO'].value_counts().sort_values(ascending=False)])  
        print("Casos en el Meta con muertes:" + str(totalDepartment["count"].sum()))
        totalDepartment["count"] = rateCalc(totalDepartment['count'], pop["META"][year])
        y2 = totalDepartment["count"]
        plt.plot(y2, label='Departamento del Meta', marker='o', markersize=7, linewidth=5, color='green')
        plt.title(r'Comparativa de tasa de mortalidad por \textbf{'+ f'{case} '+ r'}' + '\n' +  r'entre \textbf{' + f'{years[0]} - {years[-1]}' + r'}', fontsize=28)
        plt.ylabel(r'Muertes por cada 100.000 habitantes', fontsize=20)
        plt.yticks(fontsize=18)
        plt.xlabel(r'Año', fontsize=20)
        plt.ylim(bottom=0)
        plt.xticks(years, fontsize=18)
        plt.legend(fontsize=18)
        plt.tight_layout()
        print("gráfica mortalidad de " + f"{case}")
        plt.savefig('./images/' + f'{case}'+ ' - Mortalidad'   +'.png', dpi=300)
        plt.close()
        
def mortalityEvolutionAll(dfN:pd.DataFrame, dfD:pd.DataFrame,years:range,pop:dict) ->None:
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    plt.figure(num=1)
    totalNation = pd.DataFrame()
    allCase = dfN
    for year in years:
        perYear = allCase.loc[(allCase["ANO"]==year)&(allCase["CON_FIN"] == 1)]
        totalNation = pd.concat([totalNation, perYear['ANO'].value_counts().sort_values(ascending=False)])
        totalNation["count" + f'{year}'] = rateCalc(totalNation['count'], pop["COLOMBIA"][year])
    y1 = totalNation["count" + f'{year}']
    plt.plot(y1, label = 'Nacional', marker ='o', markersize = 7, linewidth =5, color = 'royalblue')
    allCase = dfD
    totalDept = pd.DataFrame()
    for year in years:
        perYear = allCase.loc[(allCase["ANO"]==year)&(allCase["CON_FIN"] == 1)]
        totalDept = pd.concat([totalDept, perYear['ANO'].value_counts().sort_values(ascending=False)])
        totalDept["count" + f'{year}'] = rateCalc(totalDept['count'], pop["META"][year])
    y2 = totalDept["count" + f'{year}']
    plt.plot(y2,label='Departamento del Meta', marker = 'o', markersize=7, linewidth =5, color='green' )
    plt.title(r'Comparativa de tasa de mortalidad por \textbf{'+ "todos los eventos" + r'}'+ '\n' r'entre \textbf{' + f'{years[0]} - {years[-1]}' + r'}', fontsize=28)
    plt.ylabel(r'Eventos de interés por cada 100.000 habitantes', fontsize=20)
    plt.yticks(fontsize=18)
    plt.xlabel(r'Año', fontsize=20)
    plt.ylim(bottom=0)
    plt.xticks(years, fontsize=18)
    plt.legend(fontsize=18)
    plt.tight_layout()
    print("gráfica mortalidad de todos los eventos de interés")
    plt.savefig('./images/' + 'todos'+ ' - Mortalidad'   +'.png', dpi=300)
    
def my_autopct(pct):
    return ('%.1f' % pct) if pct > 5 else ''

    
def demographic(dfD:pd.DataFrame, years:range, pop:pd.DataFrame) ->None:
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    plt.rcParams["savefig.dpi"] = 300
    #MetaRegions
    capitalCordillera = ["Villavicencio","Calvario","San Juanito","Restrepo","Cumaral"]
    altoAriari = ["Acacias","Guamal","Cubarral","Dorado","Castilla","San Carlos"]
    rioMeta = ["Barranca","Cabuyaro","Puerto Lopez","Puerto Gaitan"]
    bajoAriari = ["Puerto Rico", "Puerto Concordia", "Mapiripan"]
    ariari = ["Castillo","Lejanias","San Juan de Arama","Granada","Fuente De Oro",
              "San Martin","Puerto Lleras"]
    macarena = ["Uribe","Mesetas","Vista Hermosa","Macarena"]
    mun = ["Villavicencio","Calvario","San Juanito","Restrepo","Cumaral",
            "Acacias","Guamal","Cubarral","Dorado","Castilla","San Carlos",
            "Barranca","Cabuyaro","Puerto Lopez","Puerto Gaitan",
            "Puerto Rico", "Puerto Concordia", "Mapiripan",
            "Castillo","Lejanias","San Juan de Arama","Granada","Fuente De Oro",
            "San Martin","Puerto Lleras",
            "Uribe","Mesetas","VistaHermosa","Macarena"]
    mun = [x.upper() for x in mun]

    allRates = pd.DataFrame()
    averageSaver = {}
    for m in mun:
        popMun = pop.loc[pop["TERRITORIO"].str.contains(m)]
        townAverage = pd.DataFrame()
        totalMun = pd.DataFrame()
        for year in years:
            perYear = dfD[dfD["ANO"] == year]
            popYearMun = popMun.loc[pop["ANO"] == year]
            popEstudio = popYearMun.iloc[0,2]
            ##Entre 14 y 24 años perYear = perYear[(perYear['EDAD'] >= 14) & (perYear['EDAD'] <= 24)]
            perYear = perYear[perYear["Municipio_ocurrencia"].str.contains(m)].value_counts().sum()
            perYear = rateCalc(perYear,popEstudio)
            townAverage = pd.concat([townAverage, pd.Series(perYear,name="count")])
            allRates = pd.concat([allRates, pd.Series(perYear,name="count")])
            totalMun = pd.concat([totalMun, pd.Series(perYear,index=[str(year)], dtype=int)])
        totalMun.plot()
        averageSaver[m] = townAverage["count"].mean()
        plt.title("Evolución de la tasa de EIS con Plaguicidas por cada 100.000 habitantes en " + "\n" + m + "" , font=Nexa, fontsize= 30, pad=10)
        plt.ylim(bottom=0)
        plt.savefig("./images/Plaguicidas/Pre/Evo" + m + ".png")
        plt.close()

    allRates1 = allRates["count"].describe()
    print(allRates1)
    sortedTowns = sorted(averageSaver.items(), key=lambda x:x[1])
    print(sortedTowns)

    munInter = ["CABUYARO", "VILLAVICENCIO", "LEJANIAS","PUERTO LLERAS","SAN CARLOS","CASTILLO","FUENTE DE ORO"]
    ##munInter = ["MACARENA","VILLAVICENCIO","MAPIRIPAN","FUENTE DE ORO","CASTILLO", "SAN CARLOS","PUERTO LLERAS","LEJANIAS"]
    munSaver = pd.DataFrame()
    for m in munInter:
        popMun = pop.loc[pop["TERRITORIO"].str.contains(m)]
        for year in years:
            popYearMun = popMun.loc[pop["ANO"] == year]
            popEstudio = popYearMun.iloc[0,2]
            ##Entre 14 y 24 años prod1 = dfD[(dfD['EDAD'] >= 14) & (dfD['EDAD'] <= 24) & (dfD["ANO"]==year)]
            prod1 = dfD[dfD["ANO"]==year]
            prod1 = prod1[prod1["Municipio_ocurrencia"].str.contains(m)].value_counts().sum()
            prod1 = rateCalc(prod1,popEstudio)
            munSaver.at[str(year), m] = prod1
    munSaver.plot(label=munInter, marker = 'o', markersize=7, linewidth =5)
    plt.title(r'Comparativa de la tasa de morbilidad de EIS con \textbf{Plaguicidas' + r'}'+ '\n' r'entre los años \textbf{' + f'{years[0]} - {years[-1]}' + r'}', font=Nexa, fontsize= 30, pad=10)
    plt.ylabel(r'Tasa de morbilidad con Plaguicidas por cada 100.000 habitantes', fontsize=20)
    plt.yticks(fontsize=18)
    plt.xlabel(r'Año', fontsize=20)
    plt.ylim(bottom=0)
    plt.xticks(fontsize=18)
    plt.legend(fontsize=18)
    plt.savefig("./images/Plaguicidas/Pre/mejoresypeores.png")
    
    # By age
    kids = dfD[dfD['EDAD'] < 14].value_counts().sum()
    prod1 = dfD[(dfD['EDAD'] >= 14) & (dfD['EDAD'] <= 24)].value_counts().sum()
    prod2 = dfD[(dfD['EDAD'] > 24) & (dfD['EDAD'] <= 34)].value_counts().sum()
    prod3 = dfD[(dfD['EDAD'] > 34) & (dfD['EDAD'] <= 44)].value_counts().sum()
    prod4 = dfD[(dfD['EDAD'] > 44) & (dfD['EDAD'] <= 54)].value_counts().sum()
    prod5 = dfD[(dfD['EDAD'] > 54) & (dfD['EDAD'] <= 64)].value_counts().sum()
    old = dfD[dfD['EDAD'] >= 65].value_counts().sum()
    
    byAge = pd.DataFrame()
    plt.figure(num=1)
    byAge = pd.concat([byAge, pd.Series(kids, index=['Menores de 14 años'], name="afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod1, index=["Entre 14 y 24 años"], name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod2, index=["Entre 24 y 34 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod3, index=["Entre 34 y 44 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod4, index=["Entre 44 y 54 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod5, index=["Entre 54 y 64 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(old, index=["Mayores de 64 años"], name= "afectados", dtype=int)])
    byAge.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225", "#54A121","#E6B91E","#EFD576","#7FCBFF","#0071C1", "#03478B"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, bbox_to_anchor=(1, 0.6))
    plt.title("Involucrados en EIS con Plaguicidas segregados por edad", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/edad.png")

    #By sex
    male = dfD[dfD["SEXO"].str.contains("M")].value_counts().sum()
    female = dfD[dfD["SEXO"].str.contains("F")].value_counts().sum()

    bySex = pd.DataFrame()
    plt.figure(num=2)
    bySex = pd.concat([bySex, pd.Series(male, index=['Hombres'], name="afectados", dtype=int)])
    bySex = pd.concat([bySex, pd.Series(female, index=['Mujeres'], name="afectados", dtype=int)])
    bySex.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["cornflowerblue", "lightpink"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center", bbox_to_anchor=(0, -1))
    plt.title("Involucrados en EIS con Plaguicidas segregados por sexo", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/sexo.png")
    
    #By regime
    notSecured = dfD[dfD["TIP_SS"].str.contains("N|I")].value_counts().sum()
    secured = dfD[~dfD["TIP_SS"].str.contains("N|I")].value_counts().sum()

    byRegime = pd.DataFrame()
    plt.figure(num=3)
    byRegime = pd.concat([byRegime, pd.Series(notSecured, index=['No afiliado'], name="afectados", dtype=int)])
    byRegime = pd.concat([byRegime, pd.Series(secured, index=['Afiliado'], name="afectados", dtype=int)])
    byRegime.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225","#0071C1"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center")
    plt.title("Involucrados en EIS con Plaguicidas segregados por " + "\n" + "tipo de afiliación a salud", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/afiliacion_salud.png")

    #By area
    cabecera = dfD[dfD["AREA"] == 1].value_counts().sum()
    centroPoblado = dfD[dfD["AREA"] == 2].value_counts().sum()
    ruralDisperso = dfD[dfD["AREA"] == 3].value_counts().sum()

    byArea = pd.DataFrame()
    plt.figure(num=4)
    byArea = pd.concat([byArea, pd.Series(cabecera, index=['Cabecera Municipal'], name="afectados", dtype=int)])
    byArea = pd.concat([byArea, pd.Series(centroPoblado, index=['Centro Poblado'], name="afectados", dtype=int)])
    byArea = pd.concat([byArea, pd.Series(ruralDisperso, index=['Rural Disperso'], name="afectados", dtype=int)])
    byArea.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225","#E6B91E","#0071C1"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center")
    plt.title("Involucrados en EIS con Plaguicidas segregados por " + "\n" + "tipo de area de ocurrencia", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/area.png")

    #byEthnicity
    indigena = dfD[dfD["PER_ETN"]== 1].value_counts().sum()
    rom = dfD[dfD["PER_ETN"]== 2].value_counts().sum()
    raizal = dfD[dfD["PER_ETN"]== 3].value_counts().sum()
    palenquero = dfD[dfD["PER_ETN"]== 4].value_counts().sum()
    afro = dfD[dfD["PER_ETN"]== 5].value_counts().sum()
    otro = dfD[dfD["PER_ETN"]== 6].value_counts().sum()

    byEthnicity = pd.DataFrame()
    plt.figure(num=5)
    byEthnicity = pd.concat([byEthnicity, pd.Series(indigena, index=['Indígena'], name="afectados", dtype=int)])
    byEthnicity = pd.concat([byEthnicity, pd.Series(rom, index=['ROM, Gitano'], name="afectados", dtype=int)])
    byEthnicity = pd.concat([byEthnicity, pd.Series(raizal, index=['Raizal'], name="afectados", dtype=int)])
    byEthnicity = pd.concat([byEthnicity, pd.Series(palenquero, index=['Palenquero'], name="afectados", dtype=int)])
    byEthnicity = pd.concat([byEthnicity, pd.Series(afro, index=['Afrocolombiano'], name="afectados", dtype=int)])
    byEthnicity = pd.concat([byEthnicity, pd.Series(otro, index=['Otro'], name="afectados", dtype=int)])
    
    myExplode = (0.2, 0.2, 0.2, 0.2, 0.2, 0)
    
    byEthnicity.plot.pie(y = "afectados", figsize=(15,8), autopct=my_autopct , radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225", "#54A121","#E6B91E","#0071C1","#7FCBFF", "#03478B"], explode = myExplode,
                   startangle=360 - 3.6)
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, bbox_to_anchor=(0, 0.7))
    plt.title("Involucrados en EIS con Plaguicidas segregados por " + "\n" + "Etnicidad", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/etnia.png")

    #ByGP
    grupoP = ["GP_DISCAPA","GP_DESPLAZ", "GP_MIGRANT", "GP_GESTAN", "GP_DESMOVI", "GP_VIC_VIO"]
    expGrupoP = ["Discapacidad","Desplazado", "Migrante", "Gestante", "Desmovilizado", "Víctima de violencia"]
    counter = 0
    for gp in grupoP:
        byGP = pd.DataFrame()
        plt.figure(num=6)
        positive = dfD[dfD[gp] == 1].value_counts().sum()
        negative = dfD[dfD[gp] == 0].value_counts().sum()
        byGP = pd.concat([byGP, pd.Series(positive, index=['Afirmativo'], name="afectados", dtype=int)])
        byGP = pd.concat([byGP, pd.Series(negative, index=['Negativo'], name="afectados", dtype=int)])
        exp = expGrupoP[counter]
        counter += 1
        byGP.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225","#0071C1"])
        plt.ylabel("",fontsize = 0)
        plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center")
        plt.title("Involucrados en EIS con Plaguicidas segregados por " + "\n" + exp, font=Nexa, fontsize= 30, pad=10)
        plt.savefig("./images/Plaguicidas/" + gp + ".png")
    #ByGP in PDET
    PDET = ["MACARENA","URIBE","MESETAS","VISTAHERMOSA","PUERTO LLERAS","PUERTO RICO","PUERTO CONCORDIA","MAPIRIPAN"]
    counter = 0
    for gp in grupoP:    
        byGP = pd.DataFrame()
        plt.figure(num=7)
        DBm = dfD[dfD["Municipio_ocurrencia"].str.contains("|".join(PDET))]
        positive = DBm[DBm[gp] == 1].value_counts().sum()
        negative = DBm[DBm[gp] == 0].value_counts().sum()
        byGP = pd.concat([byGP, pd.Series(positive, index=['Afirmativo'], name="afectados", dtype=int)])
        byGP = pd.concat([byGP, pd.Series(negative, index=['Negativo'], name="afectados", dtype=int)])
        exp = expGrupoP[counter]
        counter += 1
        byGP.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10,colors = ["#90C225","#0071C1"]) 
        plt.ylabel("",fontsize = 0)
        plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center")
        plt.title("Involucrados en EIS con Plaguicidas en municipios PDET segregados por " + "\n" + exp, font=Nexa, fontsize= 30, pad=10)
        plt.savefig("./images/Plaguicidas/PDET_" + gp + ".png")
    pass    
        
def RIPS_evolution(df:pd.DataFrame, years:range) ->None:
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    ans = pd.DataFrame()
    df.head()
    for year in years:
        perYear = df[df['ANO'] == year]
        peYear = perYear['NumeroAtenciones'].sum()
        print("En el año " + str(year) + " hubo: " + str(peYear) + " casos en Colombia")
        ans = pd.concat([ans, pd.Series(peYear, index=[year])])
    print(ans.info())    
    plt.plot(ans, label='RIPS', marker='o', markersize=7, linewidth=5, color='royalblue')
    plt.title( 'Casos RIPS en Colombia', fontsize=28)
    plt.ylabel(r'Casos RIPS', fontsize=20)
    plt.yticks(fontsize=18)
    plt.xlabel(r'Año', fontsize=20)
    plt.ylim(bottom=0)
    plt.xticks(years, fontsize=18)
    plt.legend(fontsize=18)
    plt.tight_layout()
    plt.savefig('./images/' + 'RIPS ocurrencia Colombia'  +'.png', dpi=300)
    plt.show()   


def RIPS_trim_graph(df:pd.Series) -> None:
    Nunito = "./DB/original/fonts/Nunito/NunitoRegular.ttf"
    Nexa = "./DB/original/fonts/Nexa/NexaHeavy.ttf"
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = [15,8]
    ##ADD THIS LINE BACK
    ## plt.rcParams["savefig.dpi"] = 300
    # By age
    kids = df[df['EDAD'] < 14].value_counts().sum()
    prod1 = df[(df['EDAD'] >= 14) & (df['EDAD'] <= 24)].value_counts().sum()
    prod2 = df[(df['EDAD'] > 24) & (df['EDAD'] <= 34)].value_counts().sum()
    prod3 = df[(df['EDAD'] > 34) & (df['EDAD'] <= 44)].value_counts().sum()
    prod4 = df[(df['EDAD'] > 44) & (df['EDAD'] <= 54)].value_counts().sum()
    prod5 = df[(df['EDAD'] > 54) & (df['EDAD'] <= 64)].value_counts().sum()
    old = df[df['EDAD'] >= 65].value_counts().sum()
    
    byAge = pd.DataFrame()
    plt.figure(num=1)
    byAge = pd.concat([byAge, pd.Series(kids, index=['Menores de 14 años'], name="afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod1, index=["Entre 14 y 24 años"], name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod2, index=["Entre 24 y 34 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod3, index=["Entre 34 y 44 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod4, index=["Entre 44 y 54 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(prod5, index=["Entre 54 y 64 años"] , name= "afectados", dtype=int)])
    byAge = pd.concat([byAge, pd.Series(old, index=["Mayores de 64 años"], name= "afectados", dtype=int)])
    byAge.plot.pie(y = "afectados", figsize=(15,8), autopct=my_autopct, radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225", "#54A121","#E6B91E","#EFD576","#7FCBFF","#0071C1", "#03478B"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, bbox_to_anchor=(1, 0.6))
    plt.title("Involucrados en EIS con Plaguicidas durante el" + "\n" + " primer trimestre de 2024 segregados por edad", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/T1/edad.png")

    #By sex
    male = df[df["SEXO"].str.contains("M")].value_counts().sum()
    female = df[df["SEXO"].str.contains("F")].value_counts().sum()

    bySex = pd.DataFrame()
    plt.figure(num=2)
    bySex = pd.concat([bySex, pd.Series(male, index=['Hombres'], name="afectados", dtype=int)])
    bySex = pd.concat([bySex, pd.Series(female, index=['Mujeres'], name="afectados", dtype=int)])
    bySex.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["cornflowerblue", "lightpink"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center", bbox_to_anchor=(0, -1))
    plt.title("Involucrados en EIS con Plaguicidas durante el" + "\n" +  "primer trimestre de 2024 segregados por sexo", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/T1/sexo.png")

     #By area
    rural = df[df["ZONA"].str.contains("R")].value_counts().sum()
    urbana = df[df["ZONA"].str.contains("U")].value_counts().sum()

    byArea = pd.DataFrame()
    plt.figure(num=4)
    byArea = pd.concat([byArea, pd.Series(urbana, index=['Zona Urbana'], name="afectados", dtype=int)])
    byArea = pd.concat([byArea, pd.Series(rural, index=['Zona Rural'], name="afectados", dtype=int)])
    byArea.plot.pie(y = "afectados", figsize=(15,8), autopct='%1.1f%%', radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225","#E6B91E"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center")
    plt.title("Involucrados en EIS con Plaguicidas durante el primer trimestre" + "\n" "de 2024 segregados por zona de ocurrencia", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/T1/area.png")

    Subsidiado = df[df["TIPO_SS"] == 2].value_counts().sum()
    Particular = df[df["TIPO_SS"] == 4].value_counts().sum()
    Otro = df[df["TIPO_SS"] == 5].value_counts().sum()

    byRegime = pd.DataFrame()
    plt.figure(num=3)
    byRegime = pd.concat([byRegime, pd.Series(Subsidiado, index=['Subsidiado'], name="afectados", dtype=int)])
    byRegime = pd.concat([byRegime, pd.Series(Otro, index=['Otro'], name="afectados", dtype=int)])
    byRegime = pd.concat([byRegime, pd.Series(Particular, index=["Particular"], name="afectados", dtype=int)])
    byRegime.plot.pie(y = "afectados", figsize=(15,8), autopct=my_autopct, radius = 1,fontsize=18,
                   labeldistance=10, colors = ["#90C225", "#54A121","#E6B91E","#EFD576"])
    plt.ylabel("",fontsize = 0)
    plt.legend(prop={'family':Nunito, 'size':20}, loc="lower center")
    plt.title("Involucrados en EIS con Plaguicidas durante el primer trimestre" + "\n" + "de 2024 segregados por tipo de afiliación a salud", font=Nexa, fontsize= 30, pad=10)
    plt.savefig("./images/Plaguicidas/T1/afiliacion_salud.png")



def rateCalc(df:pd.Series, pop: int) -> pd.DataFrame:
    return df*100000/pop



if __name__ == '__main__':
    pass
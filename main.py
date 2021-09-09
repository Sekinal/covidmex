import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
sns.set_theme(style="whitegrid")

class Datos():

    def __init__(self, ruta):
        self.ruta = ruta

    def leerCSV(self):
        datos_leidos = pd.read_csv(self.ruta)
        return datos_leidos

    def extraerMunicipio(self, nombre):
        datos_totales = pd.read_csv(self.ruta)
        contador = 0
        for municipio in datos_totales['nombre']:
            if municipio == nombre:
                break
            contador += 1

        datos_procesados = datos_totales.iloc[contador][3:-1]

        fechas = []
        casos = []

        dic_casos = {
            'Fechas': fechas,
            'Casos': casos
        }

        casos_totales = 0

        for casos_diarios in datos_procesados:
            casos_totales += casos_diarios
            casos.append(casos_totales)

        for fecha in pd.date_range(start='2/18/2020', end='7/23/2021'): #cambiar valor al dia anterior del dataset usado
            fechas.append(fecha)

        df_final = pd.DataFrame.from_dict(dic_casos)

        return df_final

datos_CSV = Datos("CasosDiariosMexico.csv")
estados = []
estados_nombres = []
estados_colores = ["#10002b",
                   "#240046",
                   "#3c096c",
                   "#5a189a",
                   "#7b2cbf",
                   "#9d4edd",
                   "#c77dff",
                   "#e0aaff",
                   "#283d3b",
                   "#197278",
                   "#edddd4",
                   "#c44536",
                   "#772e25",
                   "#0466c8",
                   "#0353a4",
                   "#023e7d",
                   "#002855",
                   "#001845",
                   "#33415c",
                   "#5c677d",
                   "#7d8597",
                   "#d4e09b",
                   "#f6f4d2",
                   "#cbdfbd",
                   "#f19c79",
                   "#a44a3f",
                   "#641220",
                   "#ff8500",
                   "#ffb600",
                   "#735d78",
                   "#0091ad",
                   "#f7aef8",
                   ]

for estado in datos_CSV.leerCSV()['nombre']:
    if estado != "Nacional":
        estados.append(datos_CSV.extraerMunicipio(estado))
        estados_nombres.append(estado)

print(len(estados_colores))
print(len(estados_nombres))
"""
xalapa = datos_CSV.extraerMunicipio('Xalapa')
veracruz = datos_CSV.extraerMunicipio('Veracruz')
coatzacoalcos = datos_CSV.extraerMunicipio('Coatzacoalcos')
pozarica = datos_CSV.extraerMunicipio('Poza Rica de Hidalgo')
orizaba = datos_CSV.extraerMunicipio('Orizaba')
cordoba = datos_CSV.extraerMunicipio('Cordoba')
"""

Writer = animation.writers['ffmpeg']
writer = Writer(fps=5, metadata=dict(artist='ieqr'), bitrate=1800)
fig = plt.figure(figsize=(20, 12))
def animate(i):
    plt.clf()
    plt.legend(title='Estados, con casos confirmados', fontsize='xx-small')
    plt.xlabel('Fecha')
    plt.ylabel('Casos acumulados')
    plt.title('Casos acumulados de COVID-19 en México, por estado', fontsize=20)
    plt.suptitle(f'Día {i + 1} desde el primer caso detectado en México')
    contador_temporal = 0
    for estado in estados:
        data = estado.iloc[:int(i+1)]
        p = sns.lineplot(x=data['Fechas'], y=data['Casos'], data=data, color=estados_colores[contador_temporal], markers=True, label=f"{estados_nombres[contador_temporal]} ({data['Casos'][i]})")
        if (i + 1) < len(estados[0]['Fechas']):
            plt.text(estados[0]['Fechas'][i + 1], data['Casos'][i], f"{data['Casos'][i]}", fontsize=6)
        p.tick_params(labelsize=17)
        plt.setp(p.lines, linewidth=7)
        contador_temporal += 1
    """
    data = veracruz.iloc[:int(i + 1)]
    p = sns.lineplot(x=data['Fechas'], y=data['Casos'], data=data, color='#ffd6a5', markers=True, label='Veracruz')
    plt.text(data['Fechas'][i], data['Casos'][i], f"{data['Casos'][i]}")
    plt.ylim(0, data['Casos'].iloc[-1] + int(data['Casos'].iloc[-1] / 10) + 5)
    p.tick_params(labelsize=17)
    plt.setp(p.lines, linewidth=7)

    data = coatzacoalcos.iloc[:int(i + 1)]
    p = sns.lineplot(x=data['Fechas'], y=data['Casos'], data=data, color='#caffbf', markers=True, label='Coatzacoalcos')
    plt.text(data['Fechas'][i], data['Casos'][i], f"{data['Casos'][i]}")
    p.tick_params(labelsize=17)
    plt.setp(p.lines, linewidth=7)

    data = pozarica.iloc[:int(i + 1)]
    p = sns.lineplot(x=data['Fechas'], y=data['Casos'], data=data, color='#9bf6ff', markers=True, label='Poza Rica')
    plt.text(data['Fechas'][i], data['Casos'][i], f"{data['Casos'][i]}")
    p.tick_params(labelsize=17)
    plt.setp(p.lines, linewidth=7)

    data = orizaba.iloc[:int(i + 1)]
    p = sns.lineplot(x=data['Fechas'], y=data['Casos'], data=data, color='#a0c4ff', markers=True, label='Orizaba')
    plt.text(data['Fechas'][i], data['Casos'][i], f"{data['Casos'][i]}")
    p.tick_params(labelsize=17)
    plt.setp(p.lines, linewidth=7)

    data = cordoba.iloc[:int(i + 1)]
    p = sns.lineplot(x=data['Fechas'], y=data['Casos'], data=data, color='#bdb2ff', markers=True, label='Córdoba')
    plt.text(data['Fechas'][i], data['Casos'][i], f"{data['Casos'][i]}")
    p.tick_params(labelsize=17)
    plt.setp(p.lines, linewidth=7)
    """
    if (i+10) < len(estados[0]['Fechas']):
        plt.xlim(datetime.date(2020, 2, 18), estados[0]['Fechas'][i+10])

ani = matplotlib.animation.FuncAnimation(fig, animate, frames=len(estados[0]['Fechas']), repeat=False, interval=20)

ani.save('animac.mp4', writer=writer)
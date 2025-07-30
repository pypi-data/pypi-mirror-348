import pandas as pd

def perfil_de_victimas(df, periodo="anio", victima="peaton"):
    # Validación de entrada
    if periodo not in ["anio", "trimestre", "mes"]:
        raise ValueError("El parámetro 'periodo' debe ser 'anio', 'trimestre' o 'mes'")
    if victima not in ["peaton", "ciclista", "pasajero", "motociclista", "conductor"]:
        raise ValueError("El parámetro 'victima' debe ser 'peaton', 'ciclista', 'pasajero', 'motociclista' o 'conductor'")
        
    lesionados_col = f"{victima}_lesionado"
    fallecidos_col = f"{victima}_fallecido"

    #validar columnas
    if periodo not in df.columns:
        raise ValueError(f"La columna '{periodo}' no existe en el DataFrame")
    if lesionados_col not in df.columns or fallecidos_col not in df.columns:
        raise ValueError(f"Las columnas '{lesionados_col}' y/o '{fallecidos_col}' no existen en el DataFrame")


    # Agrupamos por el periodo y sumamos lesionados y fallecidos
    grupo = df.groupby(periodo).agg(
        lesionados=(lesionados_col, 'sum'),
        fallecidos=(fallecidos_col, 'sum')
    )

    # Convertimos a diccionario con formato {periodo: {'lesionados': X, 'fallecidos': Y}}
    perfil = grupo.to_dict(orient='index')

    # Convertir valores a enteros (porque sum devuelve float)
    for key, value in perfil.items():
        perfil[key]['lesionados'] = int(value['lesionados'])
        perfil[key]['fallecidos'] = int(value['fallecidos'])

    return perfil




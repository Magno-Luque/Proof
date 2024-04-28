import pandas as pd

# Función que permite verificar que los nombres de las columnas, como parámetro, estén en el DataFrame
def verificarDataFrame(df):
    nombresColumnas = ['Ciclo', 'Código', 'Nombre', 'Requisito', 'Nombre Requisito', 'Tipo', 'Sede', 'Modalidad', 'Créditos']
    for columna in nombresColumnas:
        if columna not in df.columns:
            raise ValueError(f"El DataFrame no tiene la columna requerida: {columna}")
    return df

# Función que permite la lectura de DataFrame
def load_csv(file_path):

    extension = file_path.split('.')[-1]
    if extension == 'csv':
        data = pd.read_csv(file_path)
    elif extension == 'xlsx':
        data = pd.read_excel(file_path)
    else:
        raise ValueError("¡Este tipo de archivo no es admitido!")

    verificarDataFrame(data)

    return data

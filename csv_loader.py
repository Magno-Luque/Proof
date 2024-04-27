
import pandas as pd

# Función que permite verificar que los nombres de las columnas, como parámetro, estén en el DataFrame
def verificarDataFrame(df):
  nombresColumnas = ['Ciclo', 'Código', 'Nombre', 'Requisito', 'Nombre Requisito', 'Tipo', 'Sede', 'Modalidad', 'Créditos']
  for columna in nombresColumnas:
    if columna not in df.columns:
      raise ValueError(f"El DataFrame no tiene la columna requerida: {columna}")
  return df

def load_csv(file_path):

    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print("Error:", e)
        return None

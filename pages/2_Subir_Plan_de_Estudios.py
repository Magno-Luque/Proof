import streamlit as st
import pandas as pd

from login import autenticacion_usuario

# Función que permite verificar que los nombres de las columnas, como parámetro, estén en el DataFrame
def verificarDataFrame(df):
    nombresColumnas = ['Ciclo', 'Código', 'Nombre', 'Requisito', 'Nombre Requisito', 'Tipo', 'Sede', 'Modalidad', 'Créditos']
    for columna in nombresColumnas:
        if columna not in df.columns:
            raise ValueError(f"El DataFrame no tiene la columna requerida: {columna}")
    return df

# Función que permite la lectura de DataFrame
def leerDataFrame(df):

    extension = df.split('.')[-1]
    if extension == 'csv':
        data = pd.read_csv(df)
    elif extension == 'xlsx':
        data = pd.read_excel(df)
    else:
        pass

    verificarDataFrame(data)

    return data

def main():
    if autenticacion_usuario():
        st.title("Plan de estudios")
        upload_file = st.file_uploader('Subir el plan de estudios correspondiente a tu carrera')
        if upload_file is not None:
            filename = upload_file.name
            df = leerDataFrame(filename)
            st.session_state['df']= df
            st.write(f"Archivo cargado: {filename}")
    else:
        st.error("Debes iniciar sesión para ver el contenido.")


    



if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd

from login import autenticacion_usuario

# Función que permite arreglar los nombres de los cursos
def arreglarNombres(df, columna):
    nombresCorregidos = []
    for palabras in df[columna]:
        listaPalabras = palabras.split(' ')
        palabras_actualizadas = []
        for palabra in listaPalabras:
            if len(palabra) > 4:
                letra = palabra[0].upper()
                palabra_actualizada = letra + palabra[1:]
            else:
                palabra_actualizada = palabra
            palabras_actualizadas.append(palabra_actualizada)
        nombresCorregidos.append(' '.join(palabras_actualizadas)) 
    return nombresCorregidos


# Función que nos permmite obtener los acrónimos de cada curso
def obtenerAcronimo(df, nombresCorregidos):
  listaAcronimos = []
  for palabras in df['Nombre']:
    listaPalabras = palabras.split()
    ultimaPal = listaPalabras[-1]
    palabras_actualizadas = []
    letTem = ''
    for palabra in listaPalabras:
      if len(palabra) > 4:
        letra = palabra[0].upper()
        palabra_actualizada = letra + palabra[1:]
        letTem += letra
      else:
        palabra_actualizada = palabra
      palabras_actualizadas.append(palabra_actualizada)
    nombresCorregidos.append(' '.join(palabras_actualizadas))
    if len(ultimaPal) < 4:
      letTem += ultimaPal 
    listaAcronimos.append(letTem)
  
  return listaAcronimos
def main():
    if autenticacion_usuario():
        st.title("Plan de estudios")
        st.subheader("Grafo del plan de estudios de la carrera Ing. Informática(Grafo Magno)")
        # Chequea primero si hay un df activo, si no, te sale un mensaje y no un error
        if 'df' not in st.session_state:
            st.error("Primero carga el Plan de Estudios")
        else:
            df = st.session_state['df']
            nombresCorregidos = arreglarNombres(df, 'Nombre')
            df['Nombre'] = nombresCorregidos
            nombresCorregidos = arreglarNombres(df, 'Nombre Requisito')
            df['Nombre Requisito'] = nombresCorregidos
            acronimos = obtenerAcronimo(df,nombresCorregidos)
            df['Acrónimos'] = acronimos
            st.write(df)
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from login import autenticacion_usuario

page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://img.freepik.com/foto-gratis/fondo-acuarela-pintada-mano-forma-cielo-nubes_24972-1095.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

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


# Función que me permite generara los nodos en base a nuestro DatFrame
def generarDatosNodos(df):
    asigCodAcro = {}
    asigAcroCod = {}
    nombresNivel = {}
    cursosNivel = {}
    posic = {}
    nombresCiclo = []

    for index, row in df.iterrows():
        asigCodAcro[row['Código']] = row['Acrónimo']
    for index, row in df.iterrows():
        asigAcroCod[row['Acrónimo']] = row['Código']
    nivel = ["PRIMER","SEGUNDO","TERCER","CUARTO","QUINTO","SEXTO","SÉTIMO","OCTAVO","NOVENO","DÉCIMO"]

    for num, nombre in enumerate(nivel):
        nombresNivel[nivel[num]] = num+1

    for nombre, ciclo in nombresNivel.items():
        dicTem = []
        for index, row in df.iterrows():
            if ciclo == row['Ciclo']:
                dicTem.append(row['Acrónimo'])
        cursosNivel[nombre + ' CICLO'] = dicTem

    for contador, (i, j) in enumerate(cursosNivel.items()):
        c = 1
        nombresCiclo.append(i)
        if contador % 2==0:
            c += 0.5
        for k in j:
            posic[k] = (c, 20 - contador*2)
            c +=1

    return asigCodAcro,asigAcroCod,nombresNivel,cursosNivel,posic,nombresCiclo


# Función que nos permite mostrar la malla curricular como gráfo
def mostrarGrafo(acronimos,posic):
    G = nx.DiGraph()
    G.add_nodes_from(acronimos)
    plt.figure(figsize=(17, 27))
    nx.draw(G, posic, with_labels=True, node_color='skyblue', node_size=8000, edge_color='black', linewidths=1, font_size=20)
    
  
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
            df['Acrónimo'] = acronimos
            asigCodAcro,asigAcroCod,nombresNivel,cursosNivel,posic,nombresCiclo = generarDatosNodos(df)
            mostrarGrafo(acronimos,posic)
            st.pyplot(plt)
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()

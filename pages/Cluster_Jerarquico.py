import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# agregar configuracion de pagina

st.set_page_config(page_title='Cluster Jerarquico', layout='wide')

st.title('Bienvenido a mi tarea del Modulo 10')

st.sidebar.title('Menu de opciones')

#lista de opciones
opciones = ['Cargar datos','Cluster Jerarquico']

#seleccionar una opcion
opcion = st.sidebar.selectbox('Seleccione una opcion',opciones)

@st._cache_data
def cargar_datos(archivo):
    if archivo:
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith('.xlsx'):
            df = pd.read_excel(archivo)
        else:
            raise ValueError("Formato de archivo no soportado. Solo se aceptan archivos CSV y XLSX.")
        return df
    else:
        return None


if opcion == 'Cargar datos':
    st.sidebar.subheader('Cargar datos')
    archivo=st.sidebar.file_uploader('Seleccione un archivo CSV o XLSX',type=['csv','xlsx'])
    if archivo:
        df = cargar_datos(archivo)
        st.session_state.df = df
        st.info('Datos cargados correctamente')
    else:
        st.write('No hay datos para mostrar')
elif opcion == 'Cluster Jerarquico':
    st.subheader('Cluster Jerarquico')
    if 'df' not in st.session_state:
        st.warning('No hay datos cargados')
    else:
        df=st.session_state.df
        st.write('El archivo contiene {} filas y {} columnas'.format(df.shape[0],df.shape[1]))

        # agregar lista de columnas
        lista_columnas = df.columns
        columnas = st.sidebar.multiselect('Seleccione las columnas a utilizar',lista_columnas)

        if columnas:
            X=df[columnas]
            st.write(X.head())

            # seleccionar el tipo de enlace

            enlace = st.sidebar.selectbox('Seleccione el tipo de enlace',['ward','complete','average','single']) 
            
            # calcular la matriz de enlace
            Z = linkage(X, enlace)

            st.write(Z)

            # graficar el dendrograma
            fig=plt.figure(figsize=(6,6))

            # agregar  linea de corte en dendrograma
            corte = st.sidebar.slider('Seleccione el valor de corte',0,10,3)
            
            
            dendrogram(Z)

            plt.axhline(y=corte, color='r', linestyle='--')

            st.pyplot(fig)

            # crear una lista de criterios

            criterios = ['maxclust','distance']

            criterio = st.sidebar.selectbox('Seleccione el criterio para formar los clusters',criterios)

            k=st.sidebar.slider('Seleccione el numero de clusters',2,10,2)

            # asignar clusters
            clusters = fcluster(Z,k,criterion=criterio)

            df['Cluster']=clusters

            st.write(df.head())

            fig=plt.figure(figsize=(6,6))
            sns.scatterplot(x=X.iloc[:,0],y=X.iloc[:,1],c=clusters,s=250,marker='8',palette='tab10')
            st.pyplot(fig)

            
        else:
            st.warning('Seleccione al menos una columna')

        
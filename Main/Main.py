import streamlit as st
import pandas as pd
import pylab as plt
from PIL import Image
import webbrowser
import urllib.request
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from streamlit.components.v1 import html
import base64
import io

st.set_page_config(layout="wide", page_icon="🗞️", page_title="Visibilidad Deportiva")
	
app_mode = st.sidebar.selectbox('Ir a:',['🏠 Inicio', '💻 Web','🏊🏻 Deporte','⚽ Sección','🚻 Género redactor/a'])
df = pd.read_excel('../data/repercusion_noticias_deportivas.xlsx')
df = df.drop(['link','noticia','fecha_publicacion','fecha_actual','desactualizacion'], axis=1)

image_inicio = Image.open("../img/inicio.jpg")
with io.BytesIO() as output:
    image_inicio.save(output, format="PNG")
    b64_1 = base64.b64encode(output.getvalue()).decode()

image_visibilidad = Image.open("../img/visibilidad.jpg")
with io.BytesIO() as output:
    image_visibilidad.save(output, format="PNG")
    b64_2 = base64.b64encode(output.getvalue()).decode()

image_repercusión = Image.open("../img/repercusion.jpg")
with io.BytesIO() as output:
    image_repercusión.save(output, format="PNG")
    b64_3 = base64.b64encode(output.getvalue()).decode()

if app_mode == '🏠 Inicio':

    with st.expander('_¿Cómo usar esta página?_'):
        st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)        

    st.title('👀 Visibilidad Deportiva')

    st.header('🗞️ ANÁLISIS DIARIOS DEPORTIVOS')

    st.write('#### 📈 Análisis de la visibilidad otorgada por deporte, género del redactor, equipos de fútbol, etc. y su repercusión (en web + twitter) de las noticias de las primeras planas digitales de los principales diarios deportivos en España. El objetivo de este estudio es, a partir de los datos, poner de manifiesto si existen sesgos en las decisiones de los propios diarios deportivos a la hora de decidir a qué dar visibilidad en materia deportiva.')

    st.write('#### 🔎 Puedes navegar a través de diferentes gráficos interactivos usando el panel de la izquierda, confeccionando tu propio gráfico según campos, ejes y métricas que desees analizar. Para una mejor explicación, pulsa en los desplegables que encontrarás en la parte superior de cada página ➡️ _¿Cómo usar esta página?_')

    st.write('\n')
    st.write("#### 🎯¿Filtramos Datos?")
    st.markdown("En este apartado puedes visualizar los datos recogidos durante el mes de enero [portadas desde el 04/01/2023 al 23/01/2023] aplicando las condiciones de filtrado que estimes oportundas.")
    with st.expander('_Ver ejemplos de filtrado_'):        
        st.markdown(" - comentarios > 10 and seccion == 'baloncesto' ➡️ **_Noticias con más de 10 comentarios en la web y que hablen de baloncesto_**")
        st.markdown(" - genero_redactor == 'mujer' and seccion == 'ciclismo' ➡️ **_Noticias redactadas por mujeres y que hablen de ciclismo_**")
        st.markdown(" - repercusion_twitter > 1000 and seccion != 'futbol' ➡️ **_Noticias con una repercusión en twitter superior a 1000 y que no hablen de futbol_**")

    condition = st.text_input("**Condición de filtrado:**")
    if condition:
        filtered_df = df.query(condition)[df.columns]
        st.write("Noticias totales:", filtered_df.shape[0])
        st.write("#### ✂️ Datos filtrados:")
        st.write(filtered_df)
    else:
        st.write("Noticias totales:", df.shape[0])


	
    st.write('\n')
    st.write('#### 📋 Datos Totales:')
    df

    st.markdown("#### ✍🏻 Explicación de los Datos")
    with st.expander('_Ver explicación de los datos_'):        
        st.markdown("**web**: Cada uno de los diarios deportivos analizados")
        st.markdown("**titular**: Cabecera de la noticia registrada en el análisis")
        st.markdown("**redactor**: Periodista autor del la noticia analizada")
        st.markdown("**comentarios**: Cantidad de comentarios publicados en la noticia")
        st.markdown("**seccion**: Deporte al que hace referencia la noticia")
        st.markdown("**equipo**: Club del que habla la noticia (en caso de haber sido clasificado por el diario. Generalmente solo lo hacen en el fútbol)")
        st.markdown("**genero_redactor**: Género referente al nombre del periodista que firma la noticia")
        st.markdown("**tweets**: Cantidad de tweets publicados acerca de la noticia registrada")
        st.markdown("**alcance_twitter**: Número total de usuarios que han visto el/los tweets(s) sobre la noticia")
        st.markdown("**likes_twitter**: Cantidad de 'Me Gusta' totales en el/los tweet(s) publicados sobre la noticia")
        st.markdown("**retweets**: Cantidad de 'Retweets' totales en el/los tweet(s) publicados sobre la noticia")
        st.markdown("**respuestas_twitter**: Cantidad de respuestas totales en el/los tweet(s) publicados sobre la noticia")
        st.markdown("**repercusion_twitter**: Suma de 'likes', 'retweets' y respuestas totales en el/los tweet(s) sobre la noticia")
        st.markdown("**exito_tweet**: Medida de la repercusión en twitter dividido por el alcance (en por miles ‰)")

    st.write('\n')
    st.markdown("#### 💻 Fuentes: ")
    st.markdown("##### https://www.marca.com/")
    st.markdown("##### https://as.com/")
    st.markdown("##### https://www.mundodeportivo.com/")
    st.markdown("##### https://www.sport.es/es/")
    st.markdown("##### https://www.estadiodeportivo.com/")
    st.markdown("##### https://www.superdeporte.es/")


elif app_mode == '💻 Web':

    x = 'web'
    y = st.sidebar.selectbox('Visibilidad según:', ['seccion', 'equipo', 'genero_redactor','repercusion'])

    if y != 'repercusion':
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_2}", use_column_width=True)
    else:
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_3}", use_column_width=True)

    st.title('💻 Visibilidad por WEB')

    condition = st.text_input("**Condición de filtrado:**")
    if condition:
        filtered_df = df.query(condition)[df.columns]
    else:
        filtered_df = df.copy()
    st.write("Noticias totales:", filtered_df.shape[0])

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        st.markdown('######')

        data = filtered_df.copy()
        data = pd.crosstab(data[x], data[y])
        data = data.reset_index()

        fig = plt.figure(figsize=(200, 80))
        fig = px.bar(data, x=x, y=data.columns)

        fig.update_layout(
        title={'text': f"Noticias en primera plana por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        )

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        w = st.sidebar.selectbox('Repercusión según:', ['seccion', 'equipo', 'genero_redactor'])
        z = st.sidebar.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])
        
        st.markdown('######')
        
        data = filtered_df.copy()
        data = data.reset_index()
        df_suma = data.groupby(['web', w])[z].sum().reset_index()

        fig = go.Figure()

        for seccion in df_suma[w].unique():
            df_seccion = df_suma[df_suma[w] == seccion]
            fig.add_trace(go.Bar(
                x=df_seccion['web'],
                y=df_seccion[z],
                name=seccion,
                offsetgroup=seccion,
                width=0.5
            ))
            
        fig.update_layout(
        title={'text': f"Repercusión de las noticias por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>',
        legend_title=f'<b style="font-size:1.6em">{w}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        barmode='stack'
        )
        
        st.plotly_chart(fig, use_container_width=True)



elif app_mode == '🏊🏻 Deporte':

    x = 'seccion'
    y = st.sidebar.selectbox('Visibilidad según:', ['web','equipo', 'genero_redactor', 'repercusion'])

    if y != 'repercusion':
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_2}", use_column_width=True)
    else:
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_3}", use_column_width=True)

    st.title('🏊🏻 Visibilidad por DEPORTE')

    condition = st.text_input("**Condición de filtrado:**")
    if condition:
        filtered_df = df.query(condition)[df.columns]
    else:
        filtered_df = df.copy()
    st.write("Noticias totales:", filtered_df.shape[0])

    with st.expander('_Ver datos_'): 
        filtered_df 

    if y != 'repercusion':

        st.markdown('######')

        data = filtered_df.copy()
        data = pd.crosstab(data[x], data[y])
        data = data.reset_index()

        fig = plt.figure(figsize=(200, 80))
        fig = px.bar(data, x=x, y=data.columns)

        fig.update_layout(
        title={'text': f"Noticias en primera plana por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        xaxis=dict(tickangle=30)
        )

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        w = st.sidebar.selectbox('Repercusión según:', ['web', 'equipo', 'genero_redactor'])
        z = st.sidebar.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])
        
        st.markdown('######')
        
        data = filtered_df.copy()
        data = data.reset_index()
        df_suma = data.groupby(['seccion', w])[z].sum().reset_index()

        fig = go.Figure()

        for seccion in df_suma[w].unique():
            df_seccion = df_suma[df_suma[w] == seccion]
            fig.add_trace(go.Bar(
                x=df_seccion['seccion'],
                y=df_seccion[z],
                name=seccion,
                offsetgroup=seccion,
                width=0.5
            ))
            
        fig.update_layout(
        title={'text': f"Repercusión de las noticias por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>',
        legend_title=f'<b style="font-size:1.6em">{w}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        barmode='stack',
        xaxis=dict(tickangle=30)
        )
        
        st.plotly_chart(fig, use_container_width=True)



elif app_mode == '⚽ Equipo':
    
    x = 'equipo'
    y = st.sidebar.selectbox('Visibilidad según:',['web','seccion','genero_redactor','repercusion'])

    if y != 'repercusion':
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_2}", use_column_width=True)
    else:
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_3}", use_column_width=True)

    st.title('⚽ Visibilidad por EQUIPO')

    condition = st.text_input("**Condición de filtrado:**")
    if condition:
        filtered_df = df.query(condition)[df.columns]
    else:
        filtered_df = df.copy()
    st.write("Noticias totales:", filtered_df.shape[0])

    with st.expander('_Ver datos_'): 
        filtered_df 

    if y != 'repercusion':

        st.markdown('######')

        data = filtered_df.copy()
        data = pd.crosstab(data[x], data[y])
        data = data.reset_index()

        fig = plt.figure(figsize=(200, 80))
        fig = px.bar(data, x=x, y=data.columns)

        fig.update_layout(
        title={'text': f"Noticias en primera plana por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        xaxis=dict(tickangle=45)
        )

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        w = st.sidebar.selectbox('Repercusión según:', ['web', 'seccion','genero_redactor'])
        z = st.sidebar.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])
        
        st.markdown('######')
        
        data = filtered_df.copy()
        data = data.reset_index()
        df_suma = data.groupby(['equipo', w])[z].sum().reset_index()

        fig = go.Figure()

        for seccion in df_suma[w].unique():
            df_seccion = df_suma[df_suma[w] == seccion]
            fig.add_trace(go.Bar(
                x=df_seccion['equipo'],
                y=df_seccion[z],
                name=seccion,
                offsetgroup=seccion,
                width=0.5
            ))
            
        fig.update_layout(
        title={'text': f"Repercusión de las noticias por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>',
        legend_title=f'<b style="font-size:1.6em">{w}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        barmode='stack',
        xaxis=dict(tickangle=45)
        )
        
        st.plotly_chart(fig, use_container_width=True)


elif app_mode == '🚻 Género redactor/a':
	
    x = 'genero_redactor'
    y = st.sidebar.selectbox('Visibilidad según:',['web','seccion', 'equipo', 'repercusion'])

    if y != 'repercusion':
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_2}", use_column_width=True)
    else:
        with st.expander('_¿Cómo usar esta página?_'):
            st.image(f"data:image/png;base64,{b64_3}", use_column_width=True)

    st.title('🚻 Visibilidad por GÉNERO_REDACTOR/A')

    condition = st.text_input("**Condición de filtrado:**")
    if condition:
        filtered_df = df.query(condition)[df.columns]
    else:
        filtered_df = df.copy()
    st.write("Noticias totales:", filtered_df.shape[0])

    with st.expander('_Ver datos_'): 
        filtered_df 

    if y != 'repercusion':

        st.markdown('######')

        data = filtered_df.copy()
        data = pd.crosstab(data[x], data[y])
        data = data.reset_index()

        fig = plt.figure(figsize=(200, 80))
        fig = px.bar(data, x=x, y=data.columns)

        fig.update_layout(
        title={'text': f"Noticias en primera plana por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        )

        st.plotly_chart(fig, use_container_width=True)
        
    else:
        w = st.sidebar.selectbox('Repercusión según:', ['web', 'seccion','equipo'])
        z = st.sidebar.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])
        
        st.markdown('######')
        
        data = filtered_df.copy()
        data = data.reset_index()
        df_suma = data.groupby(['genero_redactor', w])[z].sum().reset_index()

        fig = go.Figure()

        for seccion in df_suma[w].unique():
            df_seccion = df_suma[df_suma[w] == seccion]
            fig.add_trace(go.Bar(
                x=df_seccion['genero_redactor'],
                y=df_seccion[z],
                name=seccion,
                offsetgroup=seccion,
                width=0.5
            ))
            
        fig.update_layout(
        title={'text': f"Repercusión de las noticias por {app_mode.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.6em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>',
        legend_title=f'<b style="font-size:1.6em">{w}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        barmode='stack'
        )
        
        st.plotly_chart(fig, use_container_width=True)

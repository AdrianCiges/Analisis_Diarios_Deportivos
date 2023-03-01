import streamlit as st
import pandas as pd
import numpy as np
import pylab as plt
from PIL import Image
import webbrowser
import urllib.request
import plotly.express as px
import plotly.graph_objs as go
from streamlit.components.v1 import html
import base64
import io

st.set_page_config(layout="wide", page_icon="🗞️", page_title="Visibilidad Deportiva")
	
app_mode = st.sidebar.selectbox('Ir a:',['🏠 Inicio', '💻 Web','🏊🏻 Deporte','⚽ Sección','🚻 Género redactor/a'])
df = pd.read_excel('./data/repercusion_noticias_deportivas.xlsx')
df = df.drop(['link','noticia','fecha_publicacion','fecha_actual','desactualizacion'], axis=1)

image_inicio = Image.open("./img/inicio.jpg")
with io.BytesIO() as output:
    image_inicio.save(output, format="PNG")
    b64_1 = base64.b64encode(output.getvalue()).decode()

image_visibilidad = Image.open("./img/visibilidad.jpg")
with io.BytesIO() as output:
    image_visibilidad.save(output, format="PNG")
    b64_2 = base64.b64encode(output.getvalue()).decode()

image_repercusión = Image.open("./img/repercusion.jpg")
with io.BytesIO() as output:
    image_repercusión.save(output, format="PNG")
    b64_3 = base64.b64encode(output.getvalue()).decode()

def apply_filters(df, option_web, option_seccion, option_equipo, option_genero,
                  operando_comentario, option_comentario, operando_tweets, option_tweets,
                  operando_alcance, option_alcance, operando_likes, option_likes,
                  operando_rt, option_rt, operando_respuestas, option_respuestas,
                  operando_repercusion, option_repercusion, operando_exito, option_exito):
    
    # Aplicar filtro de dimensiones
    filters = []
    if option_web and '(todos)' not in option_web:
        filters.append(df['web'].isin(option_web))
    if option_seccion and '(todos)' not in option_seccion:
        filters.append(df['seccion'].isin(option_seccion))
    if option_equipo and '(todos)' not in option_equipo:
        filters.append(df['equipo'].isin(option_equipo))
    if option_genero and '(todos)' not in option_genero:
        filters.append(df['genero_redactor'].isin(option_genero))
    if filters:
        df = df[np.logical_and.reduce(filters)]
    
    # Aplicar filtro de métricas
    filters = []
    if operando_comentario != '(todos)':
        filters.append(eval(f"df['comentarios'] {operando_comentario} {option_comentario}"))
    if operando_tweets != '(todos)':
        filters.append(eval(f"df['tweets'] {operando_tweets} {option_tweets}"))
    if operando_alcance != '(todos)':
        filters.append(eval(f"df['alcance_twitter'] {operando_alcance} {option_alcance}"))
    if operando_likes != '(todos)':
        filters.append(eval(f"df['likes_twitter'] {operando_likes} {option_likes}"))
    if operando_rt != '(todos)':
        filters.append(eval(f"df['retweets'] {operando_rt} {option_rt}"))
    if operando_respuestas != '(todos)':
        filters.append(eval(f"df['respuestas_twitter'] {operando_respuestas} {option_respuestas}"))
    if operando_repercusion != '(todos)':
        filters.append(eval(f"df['repercusion_twitter'] {operando_repercusion} {option_repercusion}"))
    if operando_exito != '(todos)':
        filters.append(eval(f"df['exito_tweet'] {operando_exito} {option_exito}"))
    if filters:
        df = df[np.logical_and.reduce(filters)]
    
    return df


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
    

    col1, col2, col3, col4 = st.columns(4)

    expander_filtros1 = st.expander("Filtros de DIMENSIONES")

    with expander_filtros1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            option_web = st.multiselect('WEB', ['(todos)']+sorted(list(df['web'].unique())))

        with col2:
            option_seccion = st.multiselect('SECCIÓN', ['(todos)']+sorted(list(df['seccion'].unique())))

        with col3:
            option_equipo = st.multiselect('EQUIPO', ['(todos)']+sorted(list(df['equipo'].unique())))

        with col4:
            option_genero = st.multiselect('GÉNERO REDACTOR', ['(todos)']+sorted(list(df['genero_redactor'].unique())))



    expander_filtros2 = st.expander("Filtro de MÉTRICAS")

    with expander_filtros2:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        with col1:
            operando_comentario = st.selectbox('COMENTARIOS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_comentario = st.number_input('nº comentarios', value=0)
            st.write(f"Rango: [{df['comentarios'].min()} - {df['comentarios'].max()}]")

        with col2:
            operando_tweets = st.selectbox('TWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_tweets = st.number_input('nº tweets', value=0)
            st.write(f"Rango: [{df['tweets'].min()} - {df['tweets'].max()}]")

        with col3:
            operando_alcance = st.selectbox('ALCANCE TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_alcance = st.number_input('nº cuentas alcanzadas', value=0)
            st.write(f"Rango: [{df['alcance_twitter'].min()} - {df['alcance_twitter'].max()}]")

        with col4:
            operando_likes = st.selectbox('LIKES TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_likes = st.number_input('nº likes', value=0)
            st.write(f"Rango: [{df['likes_twitter'].min()} - {df['likes_twitter'].max()}]")

        with col5:
            operando_rt = st.selectbox('RETWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_rt = st.number_input('nº retweets', value=0)
            st.write(f"Rango: [{df['retweets'].min()} - {df['retweets'].max()}]")

        with col6:
            operando_respuestas = st.selectbox('RESPUESTAS TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_respuestas = st.number_input('nº respuestas', value=0)
            st.write(f"Rango: [{df['respuestas_twitter'].min()} - {df['respuestas_twitter'].max()}]")

        with col7:
            operando_repercusion = st.selectbox('REPERCUSIÓN TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_repercusion = st.number_input('índice de repercusión', value=0)
            st.write(f"Rango: [{df['repercusion_twitter'].min()} - {df['repercusion_twitter'].max()}]")

        with col8:
            operando_exito = st.selectbox('ÉXITO TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_exito = st.number_input('índice de éxito', value=0)
            st.write(f"Rango: [{df['exito_tweet'].min()} - {round(df['exito_tweet'].max())}]")

    filtrar = st.button('Filtrar')

    if filtrar:
        filtered_df = apply_filters(df, option_web, option_seccion, option_equipo, option_genero,
                  operando_comentario, option_comentario, operando_tweets, option_tweets,
                  operando_alcance, option_alcance, operando_likes, option_likes,
                  operando_rt, option_rt, operando_respuestas, option_respuestas,
                  operando_repercusion, option_repercusion, operando_exito, option_exito)
        st.write("#### ✂️ Datos filtrados:")
        st.write(filtered_df)
        st.write("Noticias totales:", filtered_df.shape[0])

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

    col1, col2, col3, col4 = st.columns(4)

    expander_filtros1 = st.expander("Filtros de DIMENSIONES")

    with expander_filtros1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            option_web = st.multiselect('WEB', ['(todos)']+sorted(list(df['web'].unique())))

        with col2:
            option_seccion = st.multiselect('SECCIÓN', ['(todos)']+sorted(list(df['seccion'].unique())))

        with col3:
            option_equipo = st.multiselect('EQUIPO', ['(todos)']+sorted(list(df['equipo'].unique())))

        with col4:
            option_genero = st.multiselect('GÉNERO REDACTOR', ['(todos)']+sorted(list(df['genero_redactor'].unique())))



    expander_filtros2 = st.expander("Filtro de MÉTRICAS")

    with expander_filtros2:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        with col1:
            operando_comentario = st.selectbox('COMENTARIOS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_comentario = st.number_input('nº comentarios', value=0)
            st.write(f"Rango: [{df['comentarios'].min()} - {df['comentarios'].max()}]")

        with col2:
            operando_tweets = st.selectbox('TWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_tweets = st.number_input('nº tweets', value=0)
            st.write(f"Rango: [{df['tweets'].min()} - {df['tweets'].max()}]")

        with col3:
            operando_alcance = st.selectbox('ALCANCE TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_alcance = st.number_input('nº cuentas alcanzadas', value=0)
            st.write(f"Rango: [{df['alcance_twitter'].min()} - {df['alcance_twitter'].max()}]")

        with col4:
            operando_likes = st.selectbox('LIKES TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_likes = st.number_input('nº likes', value=0)
            st.write(f"Rango: [{df['likes_twitter'].min()} - {df['likes_twitter'].max()}]")

        with col5:
            operando_rt = st.selectbox('RETWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_rt = st.number_input('nº retweets', value=0)
            st.write(f"Rango: [{df['retweets'].min()} - {df['retweets'].max()}]")

        with col6:
            operando_respuestas = st.selectbox('RESPUESTAS TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_respuestas = st.number_input('nº respuestas', value=0)
            st.write(f"Rango: [{df['respuestas_twitter'].min()} - {df['respuestas_twitter'].max()}]")

        with col7:
            operando_repercusion = st.selectbox('REPERCUSIÓN TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_repercusion = st.number_input('índice de repercusión', value=0)
            st.write(f"Rango: [{df['repercusion_twitter'].min()} - {df['repercusion_twitter'].max()}]")

        with col8:
            operando_exito = st.selectbox('ÉXITO TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_exito = st.number_input('índice de éxito', value=0)
            st.write(f"Rango: [{df['exito_tweet'].min()} - {round(df['exito_tweet'].max())}]")


    filtrar = st.button('Filtrar')

    if filtrar:
        filtered_df = apply_filters(df, option_web, option_seccion, option_equipo, option_genero,
                  operando_comentario, option_comentario, operando_tweets, option_tweets,
                  operando_alcance, option_alcance, operando_likes, option_likes,
                  operando_rt, option_rt, operando_respuestas, option_respuestas,
                  operando_repercusion, option_repercusion, operando_exito, option_exito)

    else:
        filtered_df = df.copy()
    
    st.write("Noticias totales:", df.shape[0])


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

    col1, col2, col3, col4 = st.columns(4)

    expander_filtros1 = st.expander("Filtros de DIMENSIONES")

    with expander_filtros1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            option_web = st.multiselect('WEB', ['(todos)']+sorted(list(df['web'].unique())))

        with col2:
            option_seccion = st.multiselect('SECCIÓN', ['(todos)']+sorted(list(df['seccion'].unique())))

        with col3:
            option_equipo = st.multiselect('EQUIPO', ['(todos)']+sorted(list(df['equipo'].unique())))

        with col4:
            option_genero = st.multiselect('GÉNERO REDACTOR', ['(todos)']+sorted(list(df['genero_redactor'].unique())))



    expander_filtros2 = st.expander("Filtro de MÉTRICAS")

    with expander_filtros2:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        with col1:
            operando_comentario = st.selectbox('COMENTARIOS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_comentario = st.number_input('nº comentarios', value=0)
            st.write(f"Rango: [{df['comentarios'].min()} - {df['comentarios'].max()}]")

        with col2:
            operando_tweets = st.selectbox('TWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_tweets = st.number_input('nº tweets', value=0)
            st.write(f"Rango: [{df['tweets'].min()} - {df['tweets'].max()}]")

        with col3:
            operando_alcance = st.selectbox('ALCANCE TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_alcance = st.number_input('nº cuentas alcanzadas', value=0)
            st.write(f"Rango: [{df['alcance_twitter'].min()} - {df['alcance_twitter'].max()}]")

        with col4:
            operando_likes = st.selectbox('LIKES TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_likes = st.number_input('nº likes', value=0)
            st.write(f"Rango: [{df['likes_twitter'].min()} - {df['likes_twitter'].max()}]")

        with col5:
            operando_rt = st.selectbox('RETWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_rt = st.number_input('nº retweets', value=0)
            st.write(f"Rango: [{df['retweets'].min()} - {df['retweets'].max()}]")

        with col6:
            operando_respuestas = st.selectbox('RESPUESTAS TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_respuestas = st.number_input('nº respuestas', value=0)
            st.write(f"Rango: [{df['respuestas_twitter'].min()} - {df['respuestas_twitter'].max()}]")

        with col7:
            operando_repercusion = st.selectbox('REPERCUSIÓN TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_repercusion = st.number_input('índice de repercusión', value=0)
            st.write(f"Rango: [{df['repercusion_twitter'].min()} - {df['repercusion_twitter'].max()}]")

        with col8:
            operando_exito = st.selectbox('ÉXITO TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_exito = st.number_input('índice de éxito', value=0)
            st.write(f"Rango: [{df['exito_tweet'].min()} - {round(df['exito_tweet'].max())}]")


    filtrar = st.button('Filtrar')

    if filtrar:
        filtered_df = apply_filters(df, option_web, option_seccion, option_equipo, option_genero,
                  operando_comentario, option_comentario, operando_tweets, option_tweets,
                  operando_alcance, option_alcance, operando_likes, option_likes,
                  operando_rt, option_rt, operando_respuestas, option_respuestas,
                  operando_repercusion, option_repercusion, operando_exito, option_exito)

    else:
        filtered_df = df.copy()
    
    st.write("Noticias totales:", df.shape[0])

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

    col1, col2, col3, col4 = st.columns(4)

    expander_filtros1 = st.expander("Filtros de DIMENSIONES")

    with expander_filtros1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            option_web = st.multiselect('WEB', ['(todos)']+sorted(list(df['web'].unique())))

        with col2:
            option_seccion = st.multiselect('SECCIÓN', ['(todos)']+sorted(list(df['seccion'].unique())))

        with col3:
            option_equipo = st.multiselect('EQUIPO', ['(todos)']+sorted(list(df['equipo'].unique())))

        with col4:
            option_genero = st.multiselect('GÉNERO REDACTOR', ['(todos)']+sorted(list(df['genero_redactor'].unique())))



    expander_filtros2 = st.expander("Filtro de MÉTRICAS")

    with expander_filtros2:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        with col1:
            operando_comentario = st.selectbox('COMENTARIOS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_comentario = st.number_input('nº comentarios', value=0)
            st.write(f"Rango: [{df['comentarios'].min()} - {df['comentarios'].max()}]")

        with col2:
            operando_tweets = st.selectbox('TWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_tweets = st.number_input('nº tweets', value=0)
            st.write(f"Rango: [{df['tweets'].min()} - {df['tweets'].max()}]")

        with col3:
            operando_alcance = st.selectbox('ALCANCE TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_alcance = st.number_input('nº cuentas alcanzadas', value=0)
            st.write(f"Rango: [{df['alcance_twitter'].min()} - {df['alcance_twitter'].max()}]")

        with col4:
            operando_likes = st.selectbox('LIKES TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_likes = st.number_input('nº likes', value=0)
            st.write(f"Rango: [{df['likes_twitter'].min()} - {df['likes_twitter'].max()}]")

        with col5:
            operando_rt = st.selectbox('RETWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_rt = st.number_input('nº retweets', value=0)
            st.write(f"Rango: [{df['retweets'].min()} - {df['retweets'].max()}]")

        with col6:
            operando_respuestas = st.selectbox('RESPUESTAS TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_respuestas = st.number_input('nº respuestas', value=0)
            st.write(f"Rango: [{df['respuestas_twitter'].min()} - {df['respuestas_twitter'].max()}]")

        with col7:
            operando_repercusion = st.selectbox('REPERCUSIÓN TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_repercusion = st.number_input('índice de repercusión', value=0)
            st.write(f"Rango: [{df['repercusion_twitter'].min()} - {df['repercusion_twitter'].max()}]")

        with col8:
            operando_exito = st.selectbox('ÉXITO TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_exito = st.number_input('índice de éxito', value=0)
            st.write(f"Rango: [{df['exito_tweet'].min()} - {round(df['exito_tweet'].max())}]")


    filtrar = st.button('Filtrar')

    if filtrar:
        filtered_df = apply_filters(df, option_web, option_seccion, option_equipo, option_genero,
                  operando_comentario, option_comentario, operando_tweets, option_tweets,
                  operando_alcance, option_alcance, operando_likes, option_likes,
                  operando_rt, option_rt, operando_respuestas, option_respuestas,
                  operando_repercusion, option_repercusion, operando_exito, option_exito)

    else:
        filtered_df = df.copy()
    
    st.write("Noticias totales:", df.shape[0])
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

    col1, col2, col3, col4 = st.columns(4)

    expander_filtros1 = st.expander("Filtros de DIMENSIONES")

    with expander_filtros1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            option_web = st.multiselect('WEB', ['(todos)']+sorted(list(df['web'].unique())))

        with col2:
            option_seccion = st.multiselect('SECCIÓN', ['(todos)']+sorted(list(df['seccion'].unique())))

        with col3:
            option_equipo = st.multiselect('EQUIPO', ['(todos)']+sorted(list(df['equipo'].unique())))

        with col4:
            option_genero = st.multiselect('GÉNERO REDACTOR', ['(todos)']+sorted(list(df['genero_redactor'].unique())))



    expander_filtros2 = st.expander("Filtro de MÉTRICAS")

    with expander_filtros2:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        with col1:
            operando_comentario = st.selectbox('COMENTARIOS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_comentario = st.number_input('nº comentarios', value=0)
            st.write(f"Rango: [{df['comentarios'].min()} - {df['comentarios'].max()}]")

        with col2:
            operando_tweets = st.selectbox('TWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_tweets = st.number_input('nº tweets', value=0)
            st.write(f"Rango: [{df['tweets'].min()} - {df['tweets'].max()}]")

        with col3:
            operando_alcance = st.selectbox('ALCANCE TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_alcance = st.number_input('nº cuentas alcanzadas', value=0)
            st.write(f"Rango: [{df['alcance_twitter'].min()} - {df['alcance_twitter'].max()}]")

        with col4:
            operando_likes = st.selectbox('LIKES TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_likes = st.number_input('nº likes', value=0)
            st.write(f"Rango: [{df['likes_twitter'].min()} - {df['likes_twitter'].max()}]")

        with col5:
            operando_rt = st.selectbox('RETWEETS',['(todos)', '>', '>=', '=', '<=', '<'])
            option_rt = st.number_input('nº retweets', value=0)
            st.write(f"Rango: [{df['retweets'].min()} - {df['retweets'].max()}]")

        with col6:
            operando_respuestas = st.selectbox('RESPUESTAS TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_respuestas = st.number_input('nº respuestas', value=0)
            st.write(f"Rango: [{df['respuestas_twitter'].min()} - {df['respuestas_twitter'].max()}]")

        with col7:
            operando_repercusion = st.selectbox('REPERCUSIÓN TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_repercusion = st.number_input('índice de repercusión', value=0)
            st.write(f"Rango: [{df['repercusion_twitter'].min()} - {df['repercusion_twitter'].max()}]")

        with col8:
            operando_exito = st.selectbox('ÉXITO TWITTER',['(todos)', '>', '>=', '=', '<=', '<'])
            option_exito = st.number_input('índice de éxito', value=0)
            st.write(f"Rango: [{df['exito_tweet'].min()} - {round(df['exito_tweet'].max())}]")


    filtrar = st.button('Filtrar')

    if filtrar:
        filtered_df = apply_filters(df, option_web, option_seccion, option_equipo, option_genero,
                  operando_comentario, option_comentario, operando_tweets, option_tweets,
                  operando_alcance, option_alcance, operando_likes, option_likes,
                  operando_rt, option_rt, operando_respuestas, option_respuestas,
                  operando_repercusion, option_repercusion, operando_exito, option_exito)

    else:
        filtered_df = df.copy()
    
    st.write("Noticias totales:", df.shape[0])

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

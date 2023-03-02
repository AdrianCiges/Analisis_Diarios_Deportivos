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

df = pd.read_excel('./data/repercusion_noticias_deportivas.xlsx')
df = df.drop(['link','noticia','fecha_publicacion','fecha_actual','desactualizacion'], axis=1)
df['exito_tweet'] = df['exito_tweet'].replace(np.nan, 0)
df['repercusion_twitter'] = df['repercusion_twitter'].replace(np.nan, 0)



def filter_data(df, op_web, op_seccion, op_equipo, op_genero, op_comentarios, op_tweets, op_alcance, op_likes, op_retweets, op_respuestas, op_repercusion, op_exito):
    filtered_df = df[(df['web'].isin(op_web) if len(op_web) > 0 else True) & 
                     (df['seccion'].isin(op_seccion) if len(op_seccion) > 0 else True) & 
                     (df['equipo'].isin(op_equipo) if len(op_equipo) > 0 else True) & 
                     (df['genero_redactor'].isin(op_genero) if len(op_genero) > 0 else True) & 
                     (df['comentarios'].between(op_comentarios[0], op_comentarios[1])) &
                     (df['tweets'].between(op_tweets[0], op_tweets[1])) &
                     (df['alcance_twitter'].between(op_alcance[0], op_alcance[1])) &
                     (df['likes_twitter'].between(op_likes[0], op_likes[1])) &
                     (df['retweets'].between(op_retweets[0], op_retweets[1])) &
                     (df['respuestas_twitter'].between(op_respuestas[0], op_respuestas[1])) &
                     (df['repercusion_twitter'].between(op_repercusion[0], op_repercusion[1])) &
                     (df['exito_tweet'].between(op_exito[0], op_exito[1]))]
    return filtered_df

def reset_filtros():
    # Reinicia los valores de los filtros
    op_web = ['(todos)']
    op_seccion = ['(todos)']
    op_equipo = ['(todos)']
    op_genero = ['(todos)']

    min_value = int(df['comentarios'].min())
    max_value = int(df['comentarios'].max())
    op_comentarios = [min_value, max_value]

    min_value = int(df['tweets'].min())
    max_value = int(df['tweets'].max())
    op_tweets = [min_value, max_value]

    min_value = int(df['alcance_twitter'].min())
    max_value = int(df['alcance_twitter'].max())
    op_alcance = [min_value, max_value]

    min_value = int(df['likes_twitter'].min())
    max_value = int(df['likes_twitter'].max())
    op_likes = [min_value, max_value]

    min_value = int(df['retweets'].min())
    max_value = int(df['retweets'].max())
    op_retweets = [min_value, max_value]

    min_value = int(df['respuestas_twitter'].min())
    max_value = int(df['respuestas_twitter'].max())
    op_respuestas = [min_value, max_value]

    min_value = int(df['repercusion_twitter'].min())
    max_value = int(df['repercusion_twitter'].max())
    op_repercusion = [min_value, max_value]

    min_value = int(df['exito_tweet'].min())
    max_value = int(df['exito_tweet'].max())+1
    op_exito = [min_value, max_value]


with st.sidebar.container():

    st.write('🎯 Filtrar Datos:')

    with st.sidebar.form("my_form"):

        expander_filtros1 = st.expander("Filtros de DIMENSIONES")
        with expander_filtros1:
            op_web = st.multiselect('**WEB**', ['(todos)']+sorted(list(df['web'].unique())))
            op_seccion = st.multiselect('**SECCIÓN**', ['(todos)']+sorted(list(df['seccion'].unique())))
            op_equipo = st.multiselect('**EQUIPO**', ['(todos)']+sorted(list(df['equipo'].unique())))
            op_genero = st.multiselect('**GÉNERO REDACTOR**', ['(todos)']+sorted(list(df['genero_redactor'].unique())))

        expander_filtros2 = st.expander("Filtros de MÉTRICAS")
        with expander_filtros2:
            min_value = int(df['comentarios'].min())
            max_value = int(df['comentarios'].max())
            op_comentarios = st.slider('**COMENTARIOS**', value = [min_value, max_value])

            min_value = int(df['tweets'].min())
            max_value = int(df['tweets'].max())
            op_tweets = st.slider('**TWEETS**', value = [min_value, max_value])

            min_value = int(df['alcance_twitter'].min())
            max_value = int(df['alcance_twitter'].max())
            op_alcance = st.slider('**ALCANCE TW**', value = [min_value, max_value])

            min_value = int(df['likes_twitter'].min())
            max_value = int(df['likes_twitter'].max())
            op_likes = st.slider('**LIKES TW**', value = [min_value, max_value])

            min_value = int(df['retweets'].min())
            max_value = int(df['retweets'].max())
            op_retweets = st.slider('**RETWEETS**', value = [min_value, max_value])

            min_value = int(df['respuestas_twitter'].min())
            max_value = int(df['respuestas_twitter'].max())
            op_respuestas = st.slider('**RESPUESTAS TW**', value = [min_value, max_value])

            min_value = int(df['repercusion_twitter'].min())
            max_value = int(df['repercusion_twitter'].max())
            op_repercusion = st.slider('**REPERCUSIÓN TW**', value = [min_value, max_value])

            min_value = int(df['exito_tweet'].min())
            max_value = int(df['exito_tweet'].max())+1
            op_exito = st.slider('**ÉXITO TW**', value = [min_value, max_value])

        col1, col2 = st.columns(2)

        with col1:
        	submitted = st.form_submit_button("Filtrar Datos")
        with col2:
            reiniciar = st.form_submit_button("Reiniciar Filtros")


        if submitted:
            filtered_df = filter_data(df, op_web, op_seccion, op_equipo, op_genero, op_comentarios, op_tweets, op_alcance, op_likes, op_retweets, op_respuestas, op_repercusion, op_exito)

        else:
            filtered_df = df.copy()


        if reiniciar:

            # Reinicia el DataFrame filtrado
            reset_filtros()
            filtered_df = filter_data(df, op_web, op_seccion, op_equipo, op_genero, op_comentarios, op_tweets, op_alcance, op_likes, op_retweets, op_respuestas, op_repercusion, op_exito)


try:
    filtered_df = filter_data(df, op_web, op_seccion, op_equipo, op_genero, op_comentarios, op_tweets, op_alcance, op_likes, op_retweets, op_respuestas, op_repercusion, op_exito)

except:
    filtered_df = df.copy()

with st.sidebar:
    st.write("Noticias totales:", filtered_df.shape[0]) 

	
app_mode = st.sidebar.selectbox('Ir a:',['🏠 Inicio', '💻 Web','🏊🏻 Deporte','⚽ Equipo','🚻 Género redactor/a'])

if app_mode == '🏠 Inicio':

    st.title('👀 Visibilidad Deportiva')

    st.header('🗞️ ANÁLISIS DIARIOS DEPORTIVOS')

    st.write('#### 📈 Análisis de la visibilidad otorgada por deporte, género del redactor, equipos de fútbol, etc. y su repercusión (en web + twitter) de las noticias de las primeras planas digitales de los principales diarios deportivos en España. El objetivo de este estudio es, a partir de los datos, poner de manifiesto si existen sesgos en las decisiones de los propios diarios deportivos a la hora de decidir a qué dar visibilidad en materia deportiva.')

    st.write('#### 🔎 Puedes navegar a través de diferentes gráficos interactivos usando el panel de la izquierda, confeccionando tu propio gráfico según campos, ejes y métricas que desees analizar.')

    st.write('\n')
    st.write('#### 📋 Datos Totales:')
    df

    st.write('\n')
    st.write('#### 🎯 Datos Filtrados:')
    st.write('En este apartado podrás ver los datos con los filtros que hayas aplicado en el menú lateral')

    with st.expander('_Ver datos filtrados_'): 
        filtered_df 

    st.write('\n')
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

    st.title('💻 Visibilidad por WEB')

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
        xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
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
    y = st.sidebar.selectbox('Visibilidad según:', ['web' ,'equipo', 'genero_redactor', 'repercusion'])

    st.title('🏊🏻 Visibilidad por DEPORTE')

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
        xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=18),
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
        xaxis_tickfont=dict(size=18),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        barmode='stack',
        xaxis=dict(tickangle=30)
        )
        
        st.plotly_chart(fig, use_container_width=True)



elif app_mode == '⚽ Equipo':
    
    x = 'equipo'
    y = st.sidebar.selectbox('Visibilidad según:',['web','seccion','genero_redactor','repercusion'])

    st.title('⚽ Visibilidad por EQUIPO')

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
        xaxis_tickfont=dict(size=15),
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
        xaxis_tickfont=dict(size=15),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        barmode='stack',
        xaxis=dict(tickangle=45)
        )
        
        st.plotly_chart(fig, use_container_width=True)


elif app_mode == '🚻 Género redactor/a':
	
    x = 'genero_redactor'
    y = st.sidebar.selectbox('Visibilidad según:',['web','seccion', 'equipo', 'repercusion'])

    st.title('🚻 Visibilidad por GÉNERO_REDACTOR/A')

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

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

image_inicio = Image.open("./img/notme2.png")
with io.BytesIO() as output:
    image_inicio.save(output, format="PNG")
    b64_1 = base64.b64encode(output.getvalue()).decode()



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


with st.sidebar.container():

    st.write('🎯 Filtrar Datos:')

    with st.sidebar.form("my_form"):

        expander_filtros1 = st.expander("Filtros de DIMENSIONES")
        with expander_filtros1:
            op_web = st.multiselect('**WEB**', sorted(list(df['web'].unique())))
            op_seccion = st.multiselect('**SECCIÓN**', sorted(list(df['seccion'].unique())))
            op_equipo = st.multiselect('**EQUIPO**', sorted(list(df['equipo'].unique())))
            op_genero = st.multiselect('**GÉNERO REDACTOR**', sorted(list(df['genero_redactor'].unique())))

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

        submitted = st.form_submit_button("Filtrar Datos")


        if submitted:
            filtered_df = filter_data(df, op_web, op_seccion, op_equipo, op_genero, op_comentarios, op_tweets, op_alcance, op_likes, op_retweets, op_respuestas, op_repercusion, op_exito)

        else:
            filtered_df = df.copy()


try:
    filtered_df = filter_data(df, op_web, op_seccion, op_equipo, op_genero, op_comentarios, op_tweets, op_alcance, op_likes, op_retweets, op_respuestas, op_repercusion, op_exito)

except:
    filtered_df = df.copy()

with st.sidebar:
    st.write("Noticias totales:", filtered_df.shape[0]) 


def heatmap(x,y,z=0):   


    if y != 'repercusion':
        ejey = y 

        metrica = 'nº de noticias'

        data = filtered_df.groupby([x, y]).size().reset_index(name='counts')
        z = data['counts']
        y = data[y]
        

    else:
        ejey = w 

        metrica = z

        data = filtered_df.groupby([x, w]).sum().reset_index()
        z = data[z]
        y = data[w]

    x1 = x

    fig = go.Figure(data=go.Heatmap(
               z=z,
               x=data[x],
               y=y,
               colorscale='Oranges'
               ))

    if x == 'seccion' or x == 'deporte' or x == 'equipo':
        angle = 25
        xsize = 16
    else:
        angle = 0
        xsize = 25

    
    fig.update_layout(height=500, yaxis=dict(categoryorder='category descending'))
    fig.update_layout(
    title={'text': f"{metrica.capitalize()} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    yaxis_title=f'<b style="font-size:1.4em">{ejey}</b>',
    #legend_title=f'<b style="font-size:1.6em">{ejey}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle),
    legend_font=dict(size=20),
    height=800 ,
    yaxis=dict(tickangle=-30),
    )         

    return fig




def area(x,y, z=0):   

    if y != 'repercusion':
        ejey = y 

        metrica = 'nº de noticias'

        df = filtered_df.groupby([x, y]).size().reset_index(name='counts')

        df = df.sort_values(y)

        fig = px.area(df, x=x, y='counts', color=y, title='Gráfico de áreas apiladas',
                      labels={x:'Sitios web', 'counts':'Cantidad de registros'})

        fig.update_layout(legend=dict(title=y, orientation='v', yanchor='top', y=1.0, xanchor='right', x=1.0),
                          legend_traceorder='normal', yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',xaxis_title=f'<b style="font-size:1.2em">{x}</b>')
        fig.update_xaxes(categoryorder='category ascending')

    else:
        ejey = w 

        metrica = z

        df = filtered_df.groupby([x, w]).sum().reset_index()
        df = df.sort_values(w)

        fig = px.area(df, x=x, y=z, color=w, title='Gráfico de áreas apiladas',
                      labels={x:'Sitios web', z:'Cantidad de registros'})

        fig.update_layout(legend=dict(title=y, orientation='v', yanchor='top', y=1.0, xanchor='right', x=1.0),
                          legend_traceorder='normal', yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>', xaxis_title=f'<b style="font-size:1.2em">{x}</b>')
        fig.update_xaxes(categoryorder='category ascending')

    if x == 'seccion' or x == 'deporte' or x == 'equipo':
        angle = 25
        xsize = 16
    else:
        angle = 0
        xsize = 25

    fig.update_layout(
    title={'text': f"Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
    legend_title=f'<b style="font-size:1.6em">{ejey}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle),
    legend_font=dict(size=20),
    height=800  
    )        
    return fig


def burbujas(x,y, z=0):   

    if x == 'seccion' or x == 'deporte' or x == 'equipo':
        angle = 25
        xsize = 16

    else:
        angle = 0
        xsize = 25

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        data = filtered_df.groupby([x, y]).size().reset_index(name='counts')
        legend_order = sorted(list(data[y].unique()))

        fig = px.scatter(data, x=x, y=y, size='counts', color=y, category_orders={x: list(data[x].unique()), y: legend_order})
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">{y}</b>',legend_title=f'<b style="font-size:1.6em">{y}</b>')

    else:

        ejey = w

        metrica = z

        data = filtered_df.groupby([x, w]).sum().reset_index()
        legend_order = sorted(list(data[w].unique()))

        fig = px.scatter(data, x=x, y=w, size=z, color=w, category_orders={x: list(data[x].unique()), w: legend_order}, color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">{w}</b>',legend_title=f'<b style="font-size:1.6em">{w}</b>')


    fig.update_layout(
    title={'text': f"{metrica.capitalize()} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    yaxis=dict(tickangle=-30),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=800 
    )            
    return fig


def barras_apiladas(x,y, z=0):   

    if x == 'seccion' or x == 'deporte' or x == 'equipo':
        angle = 25
        xsize = 16
    else:
        angle = 0
        xsize = 25

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        df_count = filtered_df.groupby([x, y]).size().reset_index(name='count')
        legend_order = sorted(list(df_count[y].unique()))

        fig = px.bar(df_count, x=x, y='count', color=y,
             log_y=False, category_orders={x: list(df_count[x].unique()), y: legend_order})
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',legend_title=f'<b style="font-size:1.6em">{y}</b>')

    else:

        ejey = w

        metrica = z

        df_count = filtered_df.groupby([x, w]).sum().reset_index()
        legend_order = sorted(list(df_count[w].unique()))

        fig = px.bar(df_count, x=x, y=z, color=w,
             log_y=False, category_orders={x: list(df_count[x].unique()), w: legend_order})
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>',legend_title=f'<b style="font-size:1.6em">{w}</b>')



    fig.update_layout(
    title={'text': f"Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=600 
    )            
    return fig



def barras_log(x,y,z=0):   

    if x == 'seccion' or x == 'deporte' or x == 'equipo':
        angle = 25
        xsize = 16
    else:
        angle = 0
        xsize = 25

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        df_count = filtered_df.groupby([x, y]).size().reset_index(name='count')
        legend_order = sorted(list(df_count[y].unique()))

        fig = px.bar(df_count, x=x, y='count', color=y,
             log_y=True, category_orders={x: list(df_count[x].unique()), y: legend_order})
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',legend_title=f'<b style="font-size:1.6em">{y}</b>')

    else:

        ejey = w

        metrica = z

        df_count = filtered_df.groupby([x, w]).sum().reset_index()
        legend_order = sorted(list(df_count[w].unique()))

        fig = px.bar(df_count, x=x, y=z, color=w,
             log_y=True, category_orders={x: list(df_count[x].unique()), w: legend_order})
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">suma de {z}</b>',legend_title=f'<b style="font-size:1.6em">{w}</b>')



    fig.update_layout(
    title={'text': f"Acumulado logarítmico de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=600 
    )            
    return fig

def barras_perc(x,y,z=0):   

    if x == 'seccion' or x == 'deporte' or x == 'equipo':
        angle = 25
        xsize = 16
    else:
        angle = 0
        xsize = 25

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        df_pcts = filtered_df.groupby([x, y]).size().reset_index(name='count')
        df_pcts['pct'] = df_pcts.groupby(x)['count'].apply(lambda x: x / float(x.sum()) * 100)
        legend_order = sorted(list(df_pcts[y].unique()))


        fig = px.bar(df_pcts, x=x, y='pct', color=y,
             barmode='stack', category_orders={x: list(df_pcts[x].unique()), y: legend_order})

        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">% de noticias</b>',legend_title=f'<b style="font-size:1.6em">{y}</b>')

    else:

        ejey = w

        metrica = z

        df_pcts = filtered_df.groupby([x, w]).sum().reset_index()
        df_pcts['pct'] = df_pcts.groupby(x)[z].apply(lambda x: x / float(x.sum()) * 100)
        legend_order = sorted(list(df_pcts[w].unique()))


        fig = px.bar(df_pcts, x=x, y='pct', color=w,
             barmode='stack', category_orders={x: list(df_pcts[x].unique()), w: legend_order})
        fig.update_layout(yaxis_title=f'<b style="font-size:1.4em">% de {z}</b>',legend_title=f'<b style="font-size:1.6em">{w}</b>')



    fig.update_layout(
    title={'text': f"Porcentaje de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=600 
    )            
    return fig

def treemap(x,y,z=0):   

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        df_count = filtered_df.groupby([x, y]).size().reset_index(name='count')

        fig = px.treemap(df_count, path=[px.Constant('TODOS'), x, y], values='count',height=600)

    else:

        ejey = w

        metrica = z

        df_count = filtered_df.groupby([x, w]).sum().reset_index()

        fig = px.treemap(df_count, path=[px.Constant('TODOS'), x, w], values=z,height=600)

    fig.update_traces(root_color="lightgrey")

    fig.update_layout(
        title={'text': f"Proporción de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        margin = dict(t=50, l=25, r=25, b=25),
        height=600  
    )
    return fig

def sol(x,y,z=0):   

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        df_count = filtered_df.groupby([x, y]).size().reset_index(name='count')

        fig = px.sunburst(df_count, path=[x, y], values='count',height=800, width=800)
    
    else:

        ejey = w

        metrica = z

        df_count = filtered_df.groupby([x, w]).sum().reset_index()

        fig = px.sunburst(df_count, path=[x, w], values=z,height=800, width=800)

    fig.update_layout(
        title={'text': f"Proporción de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        margin = dict(t=50, l=25, r=25, b=25)
    )
    return fig

app_mode = st.sidebar.selectbox('Visibilidad por (_elegir **eje X**_):',['🏠 Inicio', '💻 Web','🏊🏻 Deporte','⚽ Equipo','🚻 Género redactor/a'])

if app_mode == '🏠 Inicio':

    st.title('👀 Visibilidad Deportiva')

    st.header('🗞️ ANÁLISIS DIARIOS DEPORTIVOS')

    st.write('#### 📈 Análisis de la visibilidad otorgada por deporte, género del redactor, equipos de fútbol, etc. y su repercusión (en web + twitter) de las noticias de las primeras planas digitales de los principales diarios deportivos en España. El objetivo de este estudio es, a partir de los datos, poner de manifiesto si existen sesgos en las decisiones de los propios diarios deportivos a la hora de decidir a qué dar visibilidad en materia deportiva.')

    st.write('##### 🔎 Puedes navegar a través de diferentes gráficos interactivos usando el panel de la izquierda, confeccionando tu propio gráfico según campos, ejes y métricas que desees analizar.')
	
    st.write('##### ⚠️ La interfaz está diseñada para ser visualizada desde un ordenador, pero, si estás accediendo desde un teléfono móvil, podrás disfrutar igualmente del contenido rotando tu pantalla para una mejor adaptación de los gráficos que vas a visualizar.')
   
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
    y = st.sidebar.selectbox('Desagrupar por (**Dimensión**):', ['seccion', 'equipo', 'genero_redactor','repercusion'])

    st.title('💻 Visibilidad por WEB')

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **casilla** del heatmap se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor **nº de noticias** (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica **nº de noticias** correspondiente._') 
                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el **nº de noticias** correspondientes a cada {x}. Cada una de las **líneas** representa cada uno de los valores de **{y}** (colores indicados en la leyenda). El **área** debajo de cada línea indica el **nº noticias** aportadas por cada {y} a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {y} al sumatorio total de noticias está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **burbuja** del gráfico se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **diámetro**, mayor **nº de noticias** (y viceversa). Colocándote encima de una burbuja verás que el valor de **counts** indica **nº de noticias** correspondiente. El **color** de cada burbuja hace referencia a cada **{y}** (indicado en la leyenda)_') 
                    st.plotly_chart(burbujas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el **nº de noticias** (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{y}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}._') 
                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el **nº de noticias** (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{y}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el **porcentaje de noticias** de cada {y} respecto al total para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{y}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada una de las **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{y}**. El **tamaño** de cada sub-caja representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada una de las **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{y}**. El **tamaño** de cada sub-sector representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y), use_container_width=True)  

            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)

        
    else:

        col1, col2 = st.sidebar.columns((1,5))


        with col2:
            w = st.selectbox('Repercusión desagrupada por:', ['seccion', 'equipo', 'genero_redactor'])
            z = st.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])


        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representan los valores de **{w}**. En cada **casilla** del heatmap se representa el sumatorio de **{z}** correspondiente a cada {w} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica el **sumatorio** de {z}._') 
                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el sumatorio de **{z}**. Cada una de las **líneas** representa cada uno de los valores de {w} (colores indicados en la leyenda). El **área** debajo de cada línea indica el sumatorio de {z} aportado a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {w} al sumatorio total de {z} está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y,z), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** encontramos los valores de **{w}**. En cada **burbuja** del gráfico se representa el sumatorio de **{z}** correspondientes a cada {w} para la {x} que indique el eje X. A mayor **diámetro**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una burbuja verás el valor de **{z}** correspondiente. El **color** de cada burbuja hace referencia a cada {w} (indicado en la leyenda)._') 
                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el sumatorio de {z} (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}._') 
                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el sumatorio de {z} (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos las **{x}**. En el **eje Y** se representa el **porcentaje** que cada {w} aporta al total de **{z}** para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada una de las **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del sumatorio de **{z}** frente al total para esa {x}. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{w}**. El **tamaño** de cada sub-caja representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada una de las **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** de **{z}** frenta al total para esa {x}. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{w}**. El **tamaño** de cada sub-sector representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y,z), use_container_width=True) 
      
            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)


elif app_mode == '🏊🏻 Deporte':

    x = 'seccion'
    y = st.sidebar.selectbox('Desagrupar por (**Dimension**):', ['web' ,'equipo', 'genero_redactor', 'repercusion'])

    st.title('🏊🏻 Visibilidad por DEPORTE')

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **casilla** del heatmap se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor nº de noticias (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica **nº de noticias** correspondiente._') 
                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **nº de noticias** correspondientes a cada {x}. Cada una de las **líneas** representa cada uno de los valores de **{y}** (colores indicados en la leyenda). El **área** debajo de cada línea indica el **nº noticias** aportadas por cada {y} a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {y} al sumatorio total de noticias está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **burbuja** del gráfico se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **diámetro**, mayor nº de noticias (y viceversa). Colocándote encima de una burbuja verás que el valor de **counts** indica **nº de noticias** correspondiente. El **color** de cada burbuja hace referencia a cada {y} (indicado en la leyenda)_') 
                    st.plotly_chart(burbujas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **nº de noticias** (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}._') 
                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **nº de noticias** (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **porcentaje de noticias** de cada {y} respecto al total para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{y}**. El **tamaño** de cada sub-caja representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{y}**. El **tamaño** de cada sub-sector representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y), use_container_width=True)    

            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)

    else:

        col1, col2 = st.sidebar.columns((1,5))


        with col2:
            w = st.selectbox('Repercusión desagrupada por:', ['web', 'equipo', 'genero_redactor'])
            z = st.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representan los valores de **{w}**. En cada **casilla** del heatmap se representa el sumatorio de **{z}** correspondiente a cada {w} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica el **sumatorio** de {z}._') 
                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el sumatorio de **{z}**. Cada una de las **líneas** representa cada uno de los valores de {w} (colores indicados en la leyenda). El **área** debajo de cada línea indica el sumatorio de {z} aportado a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {w} al sumatorio total de {z} está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y,z), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** encontramos los valores de **{w}**. En cada **burbuja** del gráfico se representa el sumatorio de **{z}** correspondientes a cada {w} para la {x} que indique el eje X. A mayor **diámetro**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una burbuja verás el valor de **{z}** correspondiente. El **color** de cada burbuja hace referencia a cada {w} (indicado en la leyenda)._') 
                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el sumatorio de {z} (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}._') 
                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el sumatorio de {z} (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **porcentaje** que cada {w} aporta al total de **{z}** para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del sumatorio de **{z}** frente al total para esa {x}. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{w}**. El **tamaño** de cada sub-caja representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** de **{z}** frenta al total para esa {x}. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{w}**. El **tamaño** de cada sub-sector representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y,z), use_container_width=True)
            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)


elif app_mode == '⚽ Equipo':
    
    x = 'equipo'
    y = st.sidebar.selectbox('Desagrupar por (**Domensión**):',['web','seccion','genero_redactor','repercusion'])

    st.title('⚽ Visibilidad por EQUIPO')

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **casilla** del heatmap se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor nº de noticias (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica **nº de noticias** correspondiente._') 
                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **nº de noticias** correspondientes a cada {x}. Cada una de las **líneas** representa cada uno de los valores de **{y}** (colores indicados en la leyenda). El **área** debajo de cada línea indica el **nº noticias** aportadas por cada {y} a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {y} al sumatorio total de noticias está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **burbuja** del gráfico se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **diámetro**, mayor nº de noticias (y viceversa). Colocándote encima de una burbuja verás que el valor de **counts** indica **nº de noticias** correspondiente. El **color** de cada burbuja hace referencia a cada {y} (indicado en la leyenda)_') 
                    st.plotly_chart(burbujas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **nº de noticias** (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}._') 
                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **nº de noticias** (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **porcentaje de noticias** de cada {y} respecto al total para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{y}**. El **tamaño** de cada sub-caja representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{y}**. El **tamaño** de cada sub-sector representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y), use_container_width=True)   

            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)      
        
    else:

        col1, col2 = st.sidebar.columns((1,5))


        with col2:
            w = st.selectbox('Repercusión desagrupada por:', ['web', 'seccion','genero_redactor'])
            z = st.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representan los valores de **{w}**. En cada **casilla** del heatmap se representa el sumatorio de **{z}** correspondiente a cada {w} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica el **sumatorio** de {z}._') 
                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el sumatorio de **{z}**. Cada una de las **líneas** representa cada uno de los valores de {w} (colores indicados en la leyenda). El **área** debajo de cada línea indica el sumatorio de {z} aportado a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {w} al sumatorio total de {z} está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y,z), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** encontramos los valores de **{w}**. En cada **burbuja** del gráfico se representa el sumatorio de **{z}** correspondientes a cada {w} para la {x} que indique el eje X. A mayor **diámetro**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una burbuja verás el valor de **{z}** correspondiente. El **color** de cada burbuja hace referencia a cada {w} (indicado en la leyenda)._') 
                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el sumatorio de {z} (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}._') 
                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el sumatorio de {z} (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos cada **{x}**. En el **eje Y** se representa el **porcentaje** que cada {w} aporta al total de **{z}** para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del sumatorio de **{z}** frente al total para esa {x}. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{w}**. El **tamaño** de cada sub-caja representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** de **{z}** frenta al total para esa {x}. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{w}**. El **tamaño** de cada sub-sector representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y,z), use_container_width=True)


            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)

elif app_mode == '🚻 Género redactor/a':
	
    x = 'genero_redactor'
    y = st.sidebar.selectbox('Desagrupar por (**Dimensión**):',['web','seccion', 'equipo', 'repercusion'])

    st.title('🚻 Visibilidad por GÉNERO_REDACTOR/A')

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **casilla** del heatmap se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor nº de noticias (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica **nº de noticias** correspondiente._') 
                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el **nº de noticias** correspondientes a cada {x}. Cada una de las **líneas** representa cada uno de los valores de **{y}** (colores indicados en la leyenda). El **área** debajo de cada línea indica el **nº noticias** aportadas por cada {y} a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {y} al sumatorio total de noticias está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** encontramos los valores de **{y}**. En cada **burbuja** del gráfico se representa el **nº de noticias** correspondientes a cada {y} para la {x} que indique el eje X. A mayor **diámetro**, mayor nº de noticias (y viceversa). Colocándote encima de una burbuja verás que el valor de **counts** indica **nº de noticias** correspondiente. El **color** de cada burbuja hace referencia a cada {y} (indicado en la leyenda)_') 
                    st.plotly_chart(burbujas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el **nº de noticias** (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}._') 
                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el **nº de noticias** (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el **porcentaje de noticias** de cada {y} respecto al total para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada {y} (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {y}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{y}**. El **tamaño** de cada sub-caja representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** del **nº de noticias** de esa {x} frente al total. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{y}**. El **tamaño** de cada sub-sector representa la **proporción** del **nº de noticias** de cada {y} frente al total de noticias de esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y), use_container_width=True)  

            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True) 
        
            
    else:

        col1, col2 = st.sidebar.columns((1,5))


        with col2:
            w = st.selectbox('Repercusión desagrupada por:', ['web', 'seccion','equipo'])
            z = st.selectbox('Métrica:', ['comentarios', 'tweets', 'alcance_twitter', 'likes_twitter', 'retweets', 'respuestas_twitter', 'repercusion_twitter', 'exito_tweet'])

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Heatmap', expanded=True): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representan los valores de **{w}**. En cada **casilla** del heatmap se representa el sumatorio de **{z}** correspondiente a cada {w} para la {x} que indique el eje X. A mayor **intensidad de color**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una casilla verás que el valor de **z** indica el **sumatorio** de {z}._') 
                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el sumatorio de **{z}**. Cada una de las **líneas** representa cada uno de los valores de {w} (colores indicados en la leyenda). El **área** debajo de cada línea indica el sumatorio de {z} aportado a cada {x}. Colocándote encima del pico de la línea verás la información correspondiente a ese área. Téngase en cuenta que el aporte de cada {w} al sumatorio total de {z} está representado solo por el área que va desde el pico de su línea hasta el de la línea inmediatamente por debajo, no hasta el eje X._') 
                    st.plotly_chart(area(x,y,z), use_container_width=True)    

                with st.expander('Burbujas', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** encontramos los valores de **{w}**. En cada **burbuja** del gráfico se representa el sumatorio de **{z}** correspondientes a cada {w} para la {x} que indique el eje X. A mayor **diámetro**, mayor sumatorio de {z} (y viceversa). Colocándote encima de una burbuja verás el valor de **{z}** correspondiente. El **color** de cada burbuja hace referencia a cada {w} (indicado en la leyenda)._') 
                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el sumatorio de {z} (en términos absolutos) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}._') 
                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el sumatorio de {z} (en escala logarítmica) correspondientes a cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}. Téngase en cuenta que las distancias del eje Y son mayores conforme se asciende dada la **escala logarítmica** del eje. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos._') 
                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: En el **eje X** tenemos el **{x}**. En el **eje Y** se representa el **porcentaje** que cada {w} aporta al total de **{z}** para cada {x}. Cada uno de los **colores** de las barras hace referencia a cada **{w}** (indicado en la leyenda). Colocándote encima de las barras puedes ver la información correspondiente a cada {w}, indicándose el % correspondiente para cada uno en la etiqueta "pct"._') 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)   

                with st.expander('Treemap', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada una de las **cajas externas** hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada una representa la **proporción** del sumatorio de **{z}** frente al total para esa {x}. Dentro de cada caja encontramos **sub-cajas**, donde cada una hace referencia a cada **{w}**. El **tamaño** de cada sub-caja representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** las cajas puedes ampliar la visualización. Para volver al origen, puedes hacer click en "TODOS"._') 
                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=False): 
                    st.write(f'_❓ **CÓMO INTERPRETAR ESTE GRÁFICO**: Cada uno de las **sectores** del círculo interno hace referencia a cada **{x}** (diferenciadas por colores). El **tamaño** de cada uno representa la **proporción** de **{z}** frenta al total para esa {x}. Dentro de cada sector interno encontramos **sub-sectores**, donde cada uno hace referencia a cada **{w}**. El **tamaño** de cada sub-sector representa la **proporción** de **{z}** frente al total para cada {w} en esa {x}. Haciendo **click** en los sectores internos puedes ampliar la visualización. Para volver al origen, puedes hacer click en el centro._') 
                    st.plotly_chart(sol(x,y,z), use_container_width=True)

            else:
                st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns((1,3,1))

                with col2:
                    st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)    
                 
        except:

            st.write("<h1 align='center'>❌ No hay datos para los filtros que has aplicado ❌</h1>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,3,1))

            with col2:
                st.image(f"data:image/png;base64,{b64_1}", use_column_width=True)


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

st.set_page_config(layout="wide",initial_sidebar_state="collapsed", page_icon="🗞️", page_title="Visibilidad Deportiva")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def add_google_analytics():
    st.markdown(
        """
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-EMZNHRNE90"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          
          gtag('config', 'G-EMZNHRNE90');
        </script>
        """,
        unsafe_allow_html=True,
    )

# Llamada a la función add_google_analytics en el lugar apropiado del código
add_google_analytics()

df = pd.read_excel('./data/repercusion_noticias_deportivas.xlsx')
df = df.drop(['link','noticia','fecha_publicacion','fecha_actual','desactualizacion'], axis=1)
df['exito_tweet'] = df['exito_tweet'].replace(np.nan, 0)
df['repercusion_twitter'] = df['repercusion_twitter'].replace(np.nan, 0)

image_inicio = Image.open("./img/notme2.png")
with io.BytesIO() as output:
    image_inicio.save(output, format="PNG")
    b64_1 = base64.b64encode(output.getvalue()).decode()

image_icono = Image.open("./img/icono.png")
with io.BytesIO() as output:
    image_icono.save(output, format="PNG")
    b64_2 = base64.b64encode(output.getvalue()).decode()

image_filtrar = Image.open("./img/filtrar.png")
with io.BytesIO() as output:
    image_filtrar.save(output, format="PNG")
    b64_3 = base64.b64encode(output.getvalue()).decode()

image_desplegable12 = Image.open("./img/desplegables12.png")
with io.BytesIO() as output:
    image_desplegable12.save(output, format="PNG")
    b64_4 = base64.b64encode(output.getvalue()).decode()

image_desplegable34 = Image.open("./img/desplegables34.png")
with io.BytesIO() as output:
    image_desplegable34.save(output, format="PNG")
    b64_5 = base64.b64encode(output.getvalue()).decode()

image_boton = Image.open("./img/boton.png")
with io.BytesIO() as output:
    image_boton.save(output, format="PNG")
    b64_6 = base64.b64encode(output.getvalue()).decode()



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

movil = st.sidebar.checkbox("Accedo desde un móvil")
st.sidebar.write('\n')

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

st.sidebar.write('\n')


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

    if movil:
        xsize = 8
    
    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>{metrica.capitalize()} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(height=500, yaxis=dict(categoryorder='category descending'))
    fig.update_layout(
    #title={'text': f"{metrica.capitalize()} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24, 'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    yaxis_title=f'<b style="font-size:1.4em">{ejey}</b>',
    #legend_title=f'<b style="font-size:1.6em">{ejey}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle),
    legend_font=dict(size=20),
    height=800 ,
    yaxis=dict(tickangle=-30),
    margin=dict(t=30)
    )         

    return fig




def area(x,y, z=0):   

    if y != 'repercusion':
        ejey = y 

        metrica = 'nº de noticias'

        df = filtered_df.groupby([x, y]).size().reset_index(name='counts')

        df = df.sort_values(y)

        fig = px.area(df, x=x, y='counts', color=y, title='',
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
	
    if movil:
        xsize = 8

    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
    # title={'text': f"Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24, 'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'},
    legend_title=f'<b style="font-size:1.6em">{ejey}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle),
    legend_font=dict(size=20),
    height=800,
    margin=dict(t=30)
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

    if movil:
        xsize = 8

    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>{metrica.capitalize()} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
    # title={'text': f"{metrica.capitalize()} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24, 'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    yaxis=dict(tickangle=-30),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=800,
    margin=dict(t=30)
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

    if movil:
        xsize = 8

    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
    # title={'text': f"Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24, 'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=600,
    margin=dict(t=30)
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

    if movil:
        xsize = 8
	
    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>Acumulado de {metrica} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
    # title={'text': f"Acumulado logarítmico de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24, 'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=600,
    margin=dict(t=30)
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

    if movil:
        xsize = 8

    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>Porcentaje de {metrica} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
    # title={'text': f"Porcentaje de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24, 'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'},
    xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
    xaxis_tickfont=dict(size=xsize),
    yaxis_tickfont=dict(size=12),
    xaxis=dict(tickangle=angle, categoryorder='category ascending'),
    legend_font=dict(size=20),
    legend_traceorder='normal',
    height=600,
    margin=dict(t=30)
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

    if movil:
        xsize = 8
	
    fig.update_traces(root_color="lightgrey")

    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>Porporción de {metrica} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
        # title={'text': f"Proporción de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        margin = dict(t=30, l=25, r=25, b=25)
    )

    return fig

def sol(x,y,z=0):   

    if y != 'repercusion':

        ejey = y

        metrica = 'nº de noticias'

        df_count = filtered_df.groupby([x, y]).size().reset_index(name='count')

        fig = px.sunburst(df_count, path=[x, y], values='count',height=600, width=600)
    
    else:

        ejey = w

        metrica = z

        df_count = filtered_df.groupby([x, w]).sum().reset_index()

        fig = px.sunburst(df_count, path=[x, w], values=z,height=800, width=600)

    if movil:
        xsize = 8
	
    st.write('\n')
    st.markdown(f"<h4 style='text-align: center;'>Porporción de {metrica} por {app_mode.upper()} y {ejey.upper()}</h4>", unsafe_allow_html=True)

    fig.update_layout(
        # title={'text': f"Proporción de {metrica} por {app_mode.upper()} y {ejey.upper()}",'font_size': 24},
        xaxis_title=f'<b style="font-size:1.2em">{x}</b>',
        yaxis_title=f'<b style="font-size:1.4em">nº de noticias</b>',
        legend_title=f'<b style="font-size:1.6em">{y}</b>',
        xaxis_tickfont=dict(size=25),
        yaxis_tickfont=dict(size=12),
        legend_font=dict(size=20),
        margin = dict(t=30, l=25, r=25, b=25)
    )
    return fig

app_mode = st.sidebar.selectbox('Visibilidad por (_elegir **eje horizontal**_):',['🏠 Inicio', '💻 Web','🏊🏻 Deporte','⚽ Equipo','🚻 Género redactor/a'])

if app_mode == '🏠 Inicio':

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">🗞️</span> <u>ANÁLISIS DIARIOS DEPORTIVOS</u></h1>', unsafe_allow_html=True)
    
    st.write('\n')
    
    st.markdown('<h5 style="text-align:left;"><span style="font-size: 28px; font-weight:semibold;">📈 Visibilidad otorgada por deporte, género del redactor, equipos de fútbol, etc. y su repercusión (en web + twitter) de las noticias de las primeras planas digitales de los principales diarios deportivos en España.</span></h5>', unsafe_allow_html=True)
    st.markdown('<h5 style="text-align:left;"><span style="font-size: 22px; font-weight:normal;">El objetivo de este estudio es, a partir de los datos, poner de manifiesto si existen sesgos en las decisiones de los propios diarios deportivos a la hora de decidir a qué dar visibilidad en materia deportiva.</span></h5>', unsafe_allow_html=True)


    st.write('\n')
    st.markdown('<h5 style="text-align:center;"><span style="font-size: 22px; font-weight:semibold;">⚠️</span></h5>', unsafe_allow_html=True)

    st.warning('La interfaz está diseñada para ser visualizada desde un ordenador, pero, si estás accediendo desde un teléfono móvil, por favor, pulsa ✅ la casilla de "Accedo desde un móvil" (situada en el menú lateral) y rota 🔃 la pantalla para poder disfrutar del contenido con una mejor adaptación de los gráficos que vas a visualizar.')

    st.write('\n')
    st.write('\n')

    st.write('#### 🔎 Cómo crear tus gráficos')
    with st.expander('_La diversión empieza aquí_', expanded=True): 

        st.write('⬅️ Utiliza el **panel de la izquierda** para elegir filtrar datos y/o decidir qué ver en los ejes, en los colores, etc.')
        def show_hide_img():
            if st.button("**Ayuda gráfica 📷**"):
                imagen = st.image(f"data:image/png;base64,{b64_2}", use_column_width=True) 
                if st.button("❌ Ocultar"):
                    imagen.empty()
        show_hide_img()

        st.write('🎯 En "**Filtrar Datos**" puedes elegir **QUÉ VER**, filtrando por DIMENSIONES [_por ejemplo noticias de baloncesto y motor (seccion) publicadas en SuperDeporte y AS (web), etc._] y/o por MÉTRICAS (los valores numéricos) [_por ejemplo, noticias con más de 220 RT y menos de 3130 LIKES, etc._].')

        def show_hide_img():
            if st.button("**Ejemplo de filtrado ✂️**"):
                imagen = st.image(f"data:image/png;base64,{b64_3}", use_column_width=False, width = 300) 
                if st.button("❌ Ocultar"):
                    imagen.empty()
        show_hide_img()

        st.write('🌐 Si no especificas algún filtro, se seleccionan todos las DIMENSIONES y MÉTRICAS de los datos, pero si has elegido alguno, no olvides pulsar el botón de "Filtrar Datos".')

        def show_hide_img():
            if st.button("**Pulsa el botón 👆🏻**"):
                imagen = st.image(f"data:image/png;base64,{b64_6}", use_column_width=False, width = 300) 
                if st.button("❌ Ocultar"):
                    imagen.empty()
        show_hide_img()

        st.write('👀 En los **desplegables** de la parte inferior del menú lateral puedes elegir **CÓMO VERLO**, eligiendo qué ver en el **eje horizontal** usando el **primer desplegable**, y por qué dimensión **desagrupar por color** usando el **segundo desplegable**.')

        def show_hide_img():
            if st.button("**Ejemplo de desplegables ⬇️**"):
                imagen = st.image(f"data:image/png;base64,{b64_4}", use_column_width=False, width = 300) 
                if st.button("❌ Ocultar"):
                    imagen.empty()
        show_hide_img()

        st.write('❗ Si eliges **Repercusion** en el **segundo desplegable**, podrás elegir qué **MÉTRICA** ver en el **eje vertical** usando el **cuarto desplegable** y, nuevamente, por qué dimensión **desagrupar por color** usando el **tercer desplegable**')

        def show_hide_img():
            if st.button("**Ejemplo Repercusión 🔢**"):
                imagen = st.image(f"data:image/png;base64,{b64_5}", use_column_width=False, width = 300) 
                if st.button("❌ Ocultar"):
                    imagen.empty()
        show_hide_img()

    st.write('\n')
    st.write('\n')
    st.write('#### 📋 Datos Totales:')
    with st.expander('_Ver datos totales_'): 
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

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.markdown('![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=https://share.streamlit.io/your_deployed_app_link&label=VisitorsCount&labelColor=000000&logo=GitHub&logoColor=FFFFFF&color=1D70B8&style=for-the-badge)')

elif app_mode == '💻 Web':

    x = 'web'
    y = st.sidebar.selectbox('Desagrupar por (**Dimensión**):', ['seccion', 'equipo', 'genero_redactor','repercusion'])

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">💻</span> <u>Visibilidad por WEB</u></h1>', unsafe_allow_html=True)

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma del _nº de noticias_ (en valor absoluto). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: porcentaje de _nº de noticias_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: el % de cada _{y}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{y}_. \n\n **Tamaño de las cajas**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{y}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{y}_. \n\n **Tamaño de las secciones**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{y}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(sol(x,y), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Burbujas**: el tamaño indica la suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{y}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y), use_container_width=True)  

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Casillas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: suma del _nº de noticias_ (más intensidad de color a mayor nº de noticias). \n\n **Importante**: la suma del _nº de noticias_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_. \n\n **Áreas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: diferencia cada _{y}_ \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(area(x,y), use_container_width=True)     


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

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en valor absoluto). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: porcentaje de _{z}_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: el % de cada _{w}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()   
 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)  

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{w}_. \n\n **Tamaño de las cajas**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{w}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{w}_. \n\n **Tamaño de las secciones**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{w}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(sol(x,y,z), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Burbujas**: el tamaño indica la suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{w}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Casillas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: suma de _{z}_ (más intensidad de color a mayor suma de _{z}_). \n\n **Importante**: la suma de _{z}_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _{z}_. \n\n **Áreas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: diferencia cada _{w}_ \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(area(x,y,z), use_container_width=True)    
      
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

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">🏊🏻</span> <u>Visibilidad por DEPORTE</u></h1>', unsafe_allow_html=True)

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma del _nº de noticias_ (en valor absoluto). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: porcentaje de _nº de noticias_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: el % de cada _{y}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{y}_. \n\n **Tamaño de las cajas**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{y}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{y}_. \n\n **Tamaño de las secciones**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{y}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(sol(x,y), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Burbujas**: el tamaño indica la suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{y}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y), use_container_width=True)  

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Casillas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: suma del _nº de noticias_ (más intensidad de color a mayor nº de noticias). \n\n **Importante**: la suma del _nº de noticias_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_. \n\n **Áreas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: diferencia cada _{y}_ \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(area(x,y), use_container_width=True)     

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

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en valor absoluto). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: porcentaje de _{z}_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: el % de cada _{w}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()   
 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)  

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{w}_. \n\n **Tamaño de las cajas**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{w}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{w}_. \n\n **Tamaño de las secciones**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{w}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(sol(x,y,z), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Burbujas**: el tamaño indica la suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{w}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Casillas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: suma de _{z}_ (más intensidad de color a mayor suma de _{z}_). \n\n **Importante**: la suma de _{z}_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _{z}_. \n\n **Áreas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: diferencia cada _{w}_ \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(area(x,y,z), use_container_width=True)  
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

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">⚽</span> <u>Visibilidad por EQUIPO</u></h1>', unsafe_allow_html=True)

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma del _nº de noticias_ (en valor absoluto). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: porcentaje de _nº de noticias_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: el % de cada _{y}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{y}_. \n\n **Tamaño de las cajas**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{y}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{y}_. \n\n **Tamaño de las secciones**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{y}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(sol(x,y), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Burbujas**: el tamaño indica la suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{y}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y), use_container_width=True)  

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Casillas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: suma del _nº de noticias_ (más intensidad de color a mayor nº de noticias). \n\n **Importante**: la suma del _nº de noticias_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_. \n\n **Áreas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: diferencia cada _{y}_ \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(area(x,y), use_container_width=True)   

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

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en valor absoluto). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: porcentaje de _{z}_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: el % de cada _{w}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()   
 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)  

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{w}_. \n\n **Tamaño de las cajas**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{w}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{w}_. \n\n **Tamaño de las secciones**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{w}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(sol(x,y,z), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Burbujas**: el tamaño indica la suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{w}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Casillas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: suma de _{z}_ (más intensidad de color a mayor suma de _{z}_). \n\n **Importante**: la suma de _{z}_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _{z}_. \n\n **Áreas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: diferencia cada _{w}_ \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(area(x,y,z), use_container_width=True) 


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

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">🚻</span> <u>Visibilidad por GÉNERO_REDACTOR/A</u></h1>', unsafe_allow_html=True)

    st.markdown('##### Datos 🎯')

    with st.expander('_Ver datos_'): 
        filtered_df       

    if y != 'repercusion':

        try:

            if filtered_df.shape[0] != 0:

                st.markdown('######')

                st.markdown('##### Gráficos 📈')

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma del _nº de noticias_ (en valor absoluto). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_log(x,y), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: porcentaje de _nº de noticias_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{y}_. \n\n **Importante**: el % de cada _{y}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_perc(x,y), use_container_width=True)   

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{y}_. \n\n **Tamaño de las cajas**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{y}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(treemap(x,y), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{y}_. \n\n **Tamaño de las secciones**: proporcional al _nº de noticias_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{y}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(sol(x,y), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Burbujas**: el tamaño indica la suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{y}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y), use_container_width=True)  

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{y}_. \n\n **Casillas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: suma del _nº de noticias_ (más intensidad de color a mayor nº de noticias). \n\n **Importante**: la suma del _nº de noticias_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y), use_container_width=True)   


                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _nº de noticias_. \n\n **Áreas**: suma del _nº de noticias_ de cada _{y}_ en cada _{x}_. \n\n **Color**: diferencia cada _{y}_ \n\n **Importante**: la aportación de cada _{y}_ al total del _nº de noticias_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(area(x,y), use_container_width=True) 

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

                with st.expander('Barras Apiladas - Valores Absolutos', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**   "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en valor absoluto). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área ocupada por su color en cada barra.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()  

                    st.plotly_chart(barras_apiladas(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Logarítmica', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**    "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: suma de _{z}_ (en escala logarítmica). \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: las distancias del eje vertical son mayores conforme se asciende dada la escala logarítmica. Esto ayuda a ver mejor valores que en términos absolutos quedan muy ocultos.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(barras_log(x,y,z), use_container_width=True)   

                with st.expander('Barras Apiladas - Escala Porcentual', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**     "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: porcentaje de _{z}_ frente al total de cada {x}. \n\n **Colores**: diferencia cada _{w}_. \n\n **Importante**: el % de cada _{w}_ en cada _{x}_ se puede ver en la etiqueta _pct_ al pulsar el color correspondiente.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()   
 
                    st.plotly_chart(barras_perc(x,y,z), use_container_width=True)  

                with st.expander('Treemap', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**      "):
                            texto = st.write(f"**Cajas externas**: cada _{x}_. \n\n **Cajas internas**: cada _{w}_. \n\n **Tamaño de las cajas**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las cajas externas) y de cada _{w}_ en cada _{x}_ (en las cajas internas). \n\n **Importante**: puedes pulsar en las cajas para ver mejor su contenido y luego pulsar en TODOS para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(treemap(x,y,z), use_container_width=True)   

                with st.expander('Gráfico Solar', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**       "):
                            texto = st.write(f"**Secciones internas**: cada _{x}_. \n\n **Secciones externas**: cada _{w}_. \n\n **Tamaño de las secciones**: proporcional al sumatorio de _{z}_ de cada _{x}_ frente al total (en las secciones internas) y de cada _{w}_ en cada _{x}_ (en las secciones externas). \n\n **Importante**: puedes pulsar en las secciones para ver mejor su contenido y luego pulsar el medio para volver a la vista inicial.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text()

                    st.plotly_chart(sol(x,y,z), use_container_width=True)  

                with st.expander('Burbujas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**  "):
                            texto = st.write(f"**Eje horizontal**: cada _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Burbujas**: el tamaño indica la suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: Diferencia cada _{w}_")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(burbujas(x,y,z), use_container_width=True)   

                with st.expander('Mapa de calor', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO**"):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: cada _{w}_. \n\n **Casillas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: suma de _{z}_ (más intensidad de color a mayor suma de _{z}_). \n\n **Importante**: la suma de _{z}_ se puede ver en la etiqueta 'z' al pulsar cada casilla.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(heatmap(x,y,z), use_container_width=True)    

                with st.expander('Áreas', expanded=True): 

                    def show_hide_text():
                        if st.button("**🤔 CÓMO INTERPRETAR ESTE GRÁFICO** "):
                            texto = st.write(f"**Eje horizontal**: las _{x}_. \n\n **Eje vertical**: suma de _{z}_. \n\n **Áreas**: suma de _{z}_ de cada _{w}_ en cada _{x}_. \n\n **Color**: diferencia cada _{w}_ \n\n **Importante**: la aportación de cada _{w}_ al total de _{z}_ en cada _{x}_ está marcada por el área comprendida entre su línea y la inmediatamente inferior.")

                            if st.button("❌ Ocultar"):
                                texto.empty()
                    show_hide_text() 

                    st.plotly_chart(area(x,y,z), use_container_width=True) 

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

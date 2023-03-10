# Analisis_Diarios_Deportivos
## CONTENIDO 📑
[1 - Objetivo 🎯](#O)<br />
[2 - Extracción, Transformación y Carga ⚙️](#ETL) <br />
[3 - Streamlit 🌐](#ST)<br />
 
## 1 - OBJETIVO 🎯<a name="O"/>   
💥  Analizar de la visibilidad otorgada por deporte, género del redactor, equipos de fútbol, etc. y su repercusión (en web + twitter) de las noticias de las primeras planas digitales de los principales diarios deportivos en España. El objetivo de este estudio es, a partir de los datos, poner de manifiesto si existen sesgos en las decisiones de los propios diarios deportivos a la hora de decidir a qué dar visibilidad en materia deportiva.<br />

💥 Crear una interfaz web para que usuarios externos puedan:<br />

&emsp; &emsp; • Visualizar los datos recogidos en los diferentes diarios deportivos.<br />
&emsp; &emsp; • Filtrar los datos según las métricas y dimensiones que desee analizar.<br />
&emsp; &emsp; • Crear gráficos interactivos con los datos y estructura deseados.<br />

💥 Emplear todos los conceptos y herramientas posibles en el campo del análisis de datos:<br />

&emsp;&emsp;&emsp;<img src="https://github.com/AdrianCiges/Eurovision-Project/blob/main/Images/python.webp" width="25" height="25">&emsp;<img src="https://github.com/AdrianCiges/Eurovision-Project/blob/main/Images/jupyter.jpg" width="22" height="30">  &nbsp;&nbsp;    <img src="https://github.com/AdrianCiges/Eurovision-Project/blob/main/Images/pandas.png" width="22" height="30"> &nbsp; &nbsp;<img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/plotly.png" width="23" height="25">   &nbsp;&nbsp;    <img src="https://github.com/AdrianCiges/Eurovision-Project/blob/main/Images/selenium.png" width="23" height="25">     &nbsp;&nbsp;  <img src="https://github.com/AdrianCiges/Eurovision-Project/blob/main/Images/bs4.jpg" width="23" height="25">&nbsp;&nbsp;      <img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/streamlit.png" width="25" height="30">     



## 2 - EXTRACCIÓN, TRANSFORMACIÓN Y CARGA ⚙️ <a name="ETL"/>
### Obtenemos datos de diferentes fuentes (7) utilizando 2 métodos de extracción.
📰 Scrappeo Diarios: Extraemos la información de todas las noticias publicadas en las primeras planas digitales de los 6 principales diarios deportivos de España:<br />

&emsp; &emsp; • Diarios:<br /> 
&emsp;&emsp;&emsp;&emsp;&emsp;<img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/marca.png" width="70" height="30">&emsp;<img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/MundoDeportivo.png" width="80" height="30">  &nbsp;&nbsp;    <img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/AS.png" width="50" height="30"> &nbsp; &nbsp;<img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/super.png" width="75" height="30">   &nbsp;&nbsp;    <img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/sport.png" width="80" height="30">     &nbsp;&nbsp;  <img src="https://github.com/AdrianCiges/Analisis_Diarios_Deportivos/blob/main/img/Estadio.jpg" width="55" height="30">&nbsp;&nbsp;<br />
&emsp; &emsp; • Métodos: Selenium y BeautifulSoup.<br />
&emsp; &emsp; • Crear gráficos interactivos con los datos y estructura deseados.<br />

🐦 Scrapping Twitter: Inicialmente usamos la API de twitter, pero tras hacerse de pago, empleamos Selenium para conseguir los datos de las métricas de repercusión de las noticias a través de twitter:<br />

&emsp; &emsp;• ▶️ Tweets (cantidad de tweets sobre la noticia) <br />
&emsp; &emsp;• 👥 Alcance (cuentas única alcanzadas)<br />
&emsp; &emsp;• 🔁 Retweets (sumatorio de la cantidad de RT de los tweets sobre la noticia)<br />
&emsp; &emsp;• ♥️ Likes (sumatorio de la cantidad de Likes de los tweets sobre la noticia)<br />
&emsp; &emsp;• 🗣️ Respuestas (sumatorio de la cantidad de Respuestas de los tweets sobre la noticia)<br />
&emsp; &emsp;• ‼️ Índice de respercusión (sumatorio de la cantidad de RT+Likes+Respuestas de los tweets sobre la noticia)<br />
&emsp; &emsp;• ✅ Índice de éxito (Índice de Respercusión / Alcance de los tweets)<br />


🚻 Obtenemos el género de los redactores: A través del registro de nombres del INE, clasificamos a l@s redactores/as en 'hombre', 'mujer' o 'desconocido'.


## 3 - STREAMLIT 🌐 <a name="ST"/>
### Creamos la interfaz para la visualización y manejo de los datos a través de Streamlit.

&emsp; &emsp; • Estructura: Creamos el código python para levantar la interfaz a través de la librería streamlit. <br /> 
&emsp; &emsp; • Test: Probamos las diferentes funcionalidades deseadas a través de la ejecución del código en local. <br /> 
&emsp; &emsp; • Deploy: <br /> 
&emsp; &emsp;&emsp; &emsp; - Creamos el presente repositorio en GitHub para poder ejecutar el código desde la nube. <br /> 
&emsp; &emsp;&emsp; &emsp; - Utilizamos streamlit.app para subir la aplicación a la nube y hacerla accesible a cualquier usuario.

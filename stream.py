import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import texto
import os

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
URL = 'http://localhost:5000/consulta'
data_to_send = {
    'index_name':'recetas',
    'pregunta':''
    }
bandera = False
lottie_coding = load_lottieurl("https://lottie.host/6cb2d2ce-1ae6-46a4-90c5-3c6525807d70/nF2rS3jJHS.json")
imagen_video = Image.open("Kitchen-PNG-Transparent-Image.png")
imagen_kit = Image.open("kit.png")

with st.container():
    Subheader_Volumes = '<p style="text-align: center; font-family: Times New Roman; color: Green; font-size: 30px">👨‍🍳BIENVENIDO A TU AYUDANTE DE COCINA👩‍🍳</p>'
    st.markdown(Subheader_Volumes, unsafe_allow_html=True)
    st.write("---")
    st.write("<p style='text-align: center; color: black;font-family: Arial Black'>🍅🧀🍷🥐Tu Pasaporte hacia el Sabor y la Creatividad en la Cocina🥐🍷🧀🍅</p>",
        unsafe_allow_html=True)
    st.image(imagen_kit)
    import streamlit as st
    #st.markdown("<h1 style='text-align: center; color: black;font-family: Times New Roman'>KITCHEN HELPER</h1>", unsafe_allow_html=True)

    st.write("[Acerca de Nosotros >](https://www.directoalpaladar.com/)")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        form = st.form(key='my_form')
        data_to_send['pregunta'] = form.text_input('Escribe o Presiona el botón para hablar',
                                           placeholder='Ingresa un platillo o ingrediente')
        print(data_to_send['pregunta'])
        submitted = form.form_submit_button('Enviar')

    with right_column:
        if st.button("🎙️"):
            #question =
            data_to_send['pregunta']=texto.audiov()
            st.write(data_to_send['pregunta'])
            print(data_to_send)
            bandera = True
        pass
    #respuesta a la API en el metodo de voz a texto
    if bandera:
        try:
            response = requests.post(URL, json=data_to_send)
            result = response.json()
            print(result)
            st.text(result['respuesta'])
        except ValueError as e:
            st.error("Error de decodificación JSON: " + str(e))
            st.error("Respuesta del servidor: " + response.text)
    #respuesta de la API en el metodo de escritura
    if submitted:
        try:
            response = requests.post(URL, json=data_to_send)
            result = response.json()
            st.text(result['respuesta'])
        except ValueError as e:
            st.error("Error de decodificación JSON: " + str(e))
            st.error("Respuesta del servidor: " + response.text)


with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Recetarios De Cocina ")
        st.write(
            """
          Consulta nuestras fuentes de datos,
        de las cuales tomamos cientos de recetas
            para ofrecerte la mejor experiencia y facilidad, todo con un clic.
            """
        )
        st.write("[Recetario Especialidades](https://www.recetasgratis.net/)")
        st.write("[Recetario Cocina Casera y Sencilla](https://www.cocinacaserayfacil.net/comidas-faciles-rapidas-ricas-de-hacer/)")
        st.write("[Recetario Comida Ecuatoriana](https://www.laylita.com/recetas/recetas-ecuatorianas/)")
        st.write("[Recetario Cocina Fácil](https://www.youtube.com/watch?v=AhJpRnQqcVs)")

        with right_column:
            st_lottie(lottie_coding, height=300,key="coding")

with st.container():
    st.write("---")
    st.header("Zona de Videos")
    image_column, text_column = st.columns((1,2))
    with image_column:
        st.image(imagen_video)
    with text_column:
        st.write(
            """
            Si no es suficiente con las instrucciones que te proporciona nuestro ayudante de cocina,
            aqui tenemos algunos videos de los platillos mas buscados en el Ecuador, aqui podras ver tanto 
            la receta como la preparacion para que puedas cocinar paso a paso, Buen provecho!
            """

        )
st.markdown("[Encebollado](https://www.youtube.com/watch?v=AhJpRnQqcVs)")
st.markdown("[Arroz con Pollo para Fiestas](https://www.youtube.com/watch?v=uY45-VpB3CE)")
st.markdown("[Ceviche De Camaron](https://www.youtube.com/watch?v=s8Fmezppr8g)")
st.markdown("[Menestra](https://www.youtube.com/watch?v=QoaZau7G25g)")
st.markdown("[Seco de Carne](https://www.youtube.com/watch?v=d-PhS71NVYE)")
st.markdown("[Seco de Pollo](https://www.youtube.com/watch?v=CJFdqk2HP4A&list=RDLVd-PhS71NVYE&index=7)")
st.markdown("[Caldo de Gallina](https://www.youtube.com/watch?v=iJ-2dnu9YgM)")
st.markdown("[Alitas BBQ](https://www.youtube.com/watch?v=zd0-y2fS95Q)")
import streamlit as st
from groq import Groq

# Configuración básica
# MODELOS = ['modelo1', 'modelo2', 'modelo3'] # Clase 6

# Le agregamos el nombre a la pestaña y un ícono. Esta configuración tiene que ser la primer linea de streamlit.
st.set_page_config(page_title="My pets", page_icon="🐾", layout="centered")


# Entrada de texto
nombre = st.text_input("¿Cuál es tu nombre?")

# Botón para mostrar el saludo
if st.button("Saludar"):
    st.write(f"Hola {nombre}! gracias por venir a my pets", divider="rainbow", anchor=False)


MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'] # Clase 7

def configurar_pagina():
# Agregamos un título principal a nuestra página
    st.title("My pets")
    st.sidebar.title("Configuración de la IA") # Creamos un sidebar con un título.
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# modelo = configurar_pagina() # CLASE 8 => SE COMENTA (o elimina)

# Clase 7: Configuración del modelo y variables de estado
# Seguridad: Nunca subas tu archivo secrets.toml a un repositorio público.
# La gestión de secretos debe hacerse directamente a través de la interfaz de Streamlit Cloud.

# Ciente
def crear_usuario_groq():
    claveSecreta = st.secrets["CLAVE_API"]
    return Groq(api_key=claveSecreta)



def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
    model=modelo,
    messages=[{"role": "user", "content": mensajeDeEntrada}],
    stream=True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
# Generamos un container que va a guardar el historial del chat
    contenedorDelChat = st.container(height=400,border=True)
# Abrimos el contenedor del chat y mostramos el historial.
    with contenedorDelChat:
        mostrar_historial()

# Creo una función main donde voy a ir agrupando todas las funciones de mi código para que corra
# todo desde una misma función
# "rellena la cadena de caracteres"
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    
    mensaje = st.chat_input("Escribí tu mensaje: ")
    
    area_chat()
    
    if mensaje:
        actualizar_historial("user", mensaje, "🧑")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
        st.rerun()

#Explicar que es esto, por que es importante que solo se ejecute si el archivo es el principal en streamlit.
if __name__ == "__main__":
    main()
    # ("1 línea restante")
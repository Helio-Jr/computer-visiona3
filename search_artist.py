import os
from deepface import DeepFace
import cv2
import pandas as pd
from tmdbv3api import TMDb, Person
import streamlit as st
from PIL import Image
from datetime import datetime

# Caminho para as pastas de imagens
dataset_path = "dados/"

# Inicializando a biblioteca do TMDB
tmdb = TMDb()
tmdb.api_key = '2034dacd1d3dda0eeea92969115db83d'
tmdb.language = 'pt-BR'

# Função para prever o artista
def predict_artist(image_path):
    print("Fazendo a predição...")

    result = DeepFace.find(
        img_path=image_path,
        db_path=dataset_path,
        model_name='VGG-Face',
        enforce_detection=False
    )
    return result

def calculate_age(birth_date):
        today = datetime.today()
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age

# Configuração do Streamlit
st.title("Reconhecimento de Artista")
st.write("Faça o upload de uma imagem para identificar o artista.")

# Carregar a imagem via upload
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Abrindo a imagem com o PIL
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_container_width=True)

    # Salvando temporariamente para utilizar no DeepFace
    temp_image_path = "temp_image.jpg"
    image.save(temp_image_path)

    # Realizando a predição
    prediction = predict_artist(temp_image_path)
    print(prediction)
    if not prediction[0].empty and len(prediction[0]) > 1:
        print(prediction)
        print(prediction[0])
        artist = prediction[0].iloc[1, 0].split('/')[1].split('\\')[0]

        person = Person()
        artist_data = person.search(artist)[0]

        st.write("O nome do artista é:", artist)

        # Obter a data de nascimento do artista e calcular a idade
        birth_date = getattr(artist_data, 'birthday', None)

        if birth_date:
            age = calculate_age(birth_date)
            st.write(f"A idade do artista é: {age} anos.")
        else:
            st.write("Idade não disponível.")

        for movie in artist_data["known_for"]:
            st.write(f"- {movie['title']}")
    else:
        st.write("Artista não encontrado na nossa base de dados.")

    #df_prob = prediction[0][['identity', 'distance']]
    #df_prob['identity'] = df_prob['identity'].apply(lambda x: x.split('/')[1].split('\\')[0])

    #st.table(df_prob)

    # Removendo o arquivo temporário
    os.remove(temp_image_path)

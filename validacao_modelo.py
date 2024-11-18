import os
from deepface import DeepFace
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
import numpy as np

# Caminho para as pastas de imagens
train_dataset_path = "dados/"
test_dataset_path = "dados_testes/"

# Função para carregar imagens e suas labels
def carregar_imagens_e_labels(dataset_path):
    imagens = []
    labels = []
    
    for artista in os.listdir(dataset_path):
        artista_pasta = os.path.join(dataset_path, artista)
        
        # Verifica se é um diretório (pasta do artista)
        if os.path.isdir(artista_pasta):
            for imagem in os.listdir(artista_pasta):
                if imagem.lower().endswith(('.png', '.jpg', '.jpeg')):
                    imagens.append(os.path.join(artista_pasta, imagem))
                    labels.append(artista)
    
    return imagens, labels

# Função para realizar a validação do modelo com base nas imagens
def validar_modelo():
    # Carrega as imagens e labels para treinamento e teste
    train_images, train_labels = carregar_imagens_e_labels(train_dataset_path)
    test_images, test_labels = carregar_imagens_e_labels(test_dataset_path)
    
    # Treinamento com o modelo VGG-Face
    print("Treinando modelo VGG-Face...")
    DeepFace.build_model("VGG-Face")  # Cria o modelo VGG-Face
    
    # Realiza a predição para as imagens de teste
    print("Realizando predições para o conjunto de teste...")
    predicted_labels = []
    
    for img_path in test_images:
        result = DeepFace.find(img_path=img_path, db_path=train_dataset_path, model_name='VGG-Face', enforce_detection=False)
        
        # Verificando o artista predito
        if not result[0].empty and len(result[0]) > 1:
            predicted_label = result[0].iloc[1, 0].split('/')[1].split('\\')[0]
            predicted_labels.append(predicted_label)
        else:
            predicted_labels.append("Desconhecido")  # Caso não encontre artista correspondente
    
    # Calcular métricas de avaliação
    accuracy = accuracy_score(test_labels, predicted_labels)
    precision = precision_score(test_labels, predicted_labels, average='weighted', zero_division=0)
    recall = recall_score(test_labels, predicted_labels, average='weighted', zero_division=0)
    f1 = f1_score(test_labels, predicted_labels, average='weighted', zero_division=0)
    
    # Matriz de confusão padrão
    cm = confusion_matrix(test_labels, predicted_labels, labels=np.unique(test_labels + predicted_labels))
    
    # Converter a matriz de confusão para uma versão binária (True/False)
    cm_binary = cm.astype(bool)  # Converte qualquer valor maior que 0 para True e 0 para False
    
    # Exibe a matriz binária de True/False
    cm_binary_df = pd.DataFrame(cm_binary, index=np.unique(test_labels + predicted_labels), columns=np.unique(test_labels + predicted_labels))
    print("\nMatriz de Confusão (True/False):")
    print(cm_binary_df)
    
    print(f"Acurácia: {accuracy:.4f}")
    print(f"Precisão: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    return accuracy, precision, recall, f1, cm_binary_df

if __name__ == '__main__':
    accuracy, precision, recall, f1, cm_binary_df = validar_modelo()

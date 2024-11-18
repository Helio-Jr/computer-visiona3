import os
import shutil

# Caminho para a pasta "dados" onde estão as pastas dos artistas
dados_dir = 'dados'

# Caminho para a nova pasta "dados_testes" onde as imagens serão copiadas
dados_testes_dir = 'dados_testes'

# Função para copiar as últimas 20 imagens de cada pasta para a nova pasta e apagar da pasta original
def copiar_e_apagar_ultimas_20_imagens():
    # Verifica se a pasta de testes já existe, senão cria
    if not os.path.exists(dados_testes_dir):
        os.makedirs(dados_testes_dir)
    
    # Percorre todas as pastas dentro de "dados" (que são os artistas)
    for artista in os.listdir(dados_dir):
        artista_pasta = os.path.join(dados_dir, artista)
        
        # Verifica se é um diretório (pasta do artista)
        if os.path.isdir(artista_pasta):
            # Cria uma subpasta dentro de "dados_testes" com o nome do artista
            artista_pasta_teste = os.path.join(dados_testes_dir, artista)
            if not os.path.exists(artista_pasta_teste):
                os.makedirs(artista_pasta_teste)
            
            # Pega todas as imagens da pasta do artista
            imagens = [img for img in os.listdir(artista_pasta) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Ordena as imagens por nome (assumindo que o nome seja 001.jpg, 002.jpg, etc.)
            imagens.sort()  # Isso funciona porque as imagens têm números de 001 a 100, ordenando lexicograficamente
            
            # Pega as últimas 20 imagens
            ultimas_20_imagens = imagens[-20:]
            
            # Copia as últimas 20 imagens para a pasta de testes e remove da pasta original
            for imagem in ultimas_20_imagens:
                origem = os.path.join(artista_pasta, imagem)
                destino = os.path.join(artista_pasta_teste, imagem)
                
                # Copia a imagem para a pasta de testes
                shutil.copy(origem, destino)
                
                # Remove a imagem da pasta original
                os.remove(origem)
            
            print(f"20 últimas imagens copiadas e removidas para o artista {artista}.")

if __name__ == '__main__':
    copiar_e_apagar_ultimas_20_imagens()
    print("Processo concluído!")

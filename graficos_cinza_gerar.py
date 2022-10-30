import os
import glob
from platform import system
from typing import List
from PIL import Image

# Agir de acordo com o sistema operacional
if system() == 'Windows':
    sep = chr(92)
else:
    sep = '/'
if not os.path.exists('graphics_cinza'):
    os.makedirs('graphics_cinza')


def get_files_png_and_gen_dirs(dirpath: str):
    files_paths = []
    for filename in glob.glob(os.path.join(dirpath, '*')):

        # Aplicar a função recursivamente em subdiretórios, adicionando os arquivos do mesmo
        files_paths.extend(get_files_png_and_gen_dirs(filename))

        # Converter de graphics/* para graphics_cinza/*
        new_path = filename
        new_path = new_path.split(sep)
        new_path = dirpath + '_cinza' + sep + sep.join(new_path[1:])

        if filename.endswith('.png'):
            # Adicionar todos os arquivos png a lista
            files_paths.append(filename)
        else:
            # Criar os diretórios de output
            if not os.path.exists(new_path):
                os.makedirs(new_path)

    return files_paths


# Detectar arquivos png
path = 'graphics/'
files: List[str] = get_files_png_and_gen_dirs(path)

for image_path in files:
    # Transformar cada imagem em uma versão cinza
    img = Image.open(image_path)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # Transformar cada pixel em uma média dos componentes de cores, mantendo a transparencia
            (red, green, blue, alpha) = pixels[i, j]
            media = int((red + green + blue)/3)
            pixels[i, j] = (media, media, media, alpha)

    # Salvar a nova imagem
    image_path = image_path.split(sep)
    image_path = 'graphics_cinza' + sep + sep.join(image_path[1:])
    print(image_path)
    img.save(image_path, 'png')

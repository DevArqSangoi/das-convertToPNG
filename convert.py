import os
from PIL import Image, ExifTags
import tkinter as tk
from tkinter import filedialog

def selecionar_pasta(mensagem):
    root = tk.Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title=mensagem)
    return pasta

def corrigir_orientacao(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img

def converter_para_png(pasta_origem, pasta_destino):
    for arquivo in os.listdir(pasta_origem):
        nome_arquivo, extensao = os.path.splitext(arquivo)
        if extensao.lower() in ['.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp']:
            print(f"Convertendo {arquivo} para PNG...")
            img = Image.open(os.path.join(pasta_origem, arquivo))
            img = corrigir_orientacao(img)
            img.save(os.path.join(pasta_destino, f"{nome_arquivo}.png"), "PNG")
            print(f"{arquivo} convertido com sucesso para {nome_arquivo}.png")

if __name__ == "__main__":
    pasta_origem = selecionar_pasta("Selecione a pasta de origem das fotos")
    pasta_destino = selecionar_pasta("Selecione a pasta de destino das fotos convertidas")
    
    if pasta_origem and pasta_destino:
        print("Iniciando a conversão...")
        converter_para_png(pasta_origem, pasta_destino)
        print("Conversão concluída!")
    else:
        print("Por favor, selecione as pastas de origem e destino.")
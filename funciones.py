from pathlib import Path
import sys
import os
import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import messagebox

import cv2
import pandas as pd
from puntos import *
import numpy as np
import imutils
from win32api import GetSystemMetrics
import easyocr
from pdf2image import convert_from_path

# Instrucciones para saber el tamaño de la pantalla
printAncho = GetSystemMetrics(0)
printAlto = GetSystemMetrics(1)

#poppler = r'C:\Users\ASUS1\Downloads\Release-22.12.0-0\poppler-22.12.0\Library\bin'
poppler = r'Release-22.12.0-0\poppler-22.12.0\Library\bin'

def selectFilesConfig():
    filename = fd.askopenfilename(
        filetypes=(
        ("Archivos PDF", "*.pdf"),
        ("Todos los archivos", "*.*")),
        initialdir=Path(sys.executable).parent
    )
    if filename:
        showinfo(title='Archivo selecionado', message=filename)
        pages = convert_from_path(filename, 200, poppler_path=poppler)
        for i in range(len(pages)):
            imagen = pages[i].save('paga'+ str(i) +'.jpg', 'JPEG')
        
        reader = easyocr.Reader(["es"], gpu=False)
        image = cv2.imread('Paga0.jpg') # Lee la imagen
        ancho = image.shape[1] # Calcula ancho
        alto= image.shape[0] # Calcula alto
        img = imutils.resize(image, height=printAlto) # Redimensiona deacuerdo al alto de la pantalla
        relacion =(alto/img.shape[0]) # Obtiene la relacion de la imagen original
        puntos = tomarPuntos("Imágen Puntos",img, (0,0,255)) # Toma los punto de configuración
        puntos1 = np.array(puntos)
        rel = np.int16(puntos1*relacion)
        column =["x1", "y1"]
        
        df = pd.DataFrame(columns=column)
        x =[]
        y =[]
        for i, dato in enumerate (rel):
            x.append(dato[0])
            y.append(dato[1]) 

        df['x1'] = x
        df['y1'] = y
        df.to_csv('default.csv', header=True, index=False, encoding="utf-8")
        
    else:
        showinfo(title='Archivo selecionado', message= "No seleccionó ningun archivo")

def selectFile(folderSelect, fileName, fileSave):
    sourceDir = os.path.join(folderSelect, fileName) # selecciona el path de cada archivo a procesar
    datos =[]
    datos.append(fileName) # Guarda en la primera columna el nombre del archivo que esta procesando
    pages = convert_from_path(sourceDir, 200, poppler_path=poppler)
    for i in range(len(pages)):
        imagen = pages[i].save('paga'+ str(i) +'.jpg', 'JPEG')
    
    reader = easyocr.Reader(["es"], gpu=True)
    image = cv2.imread('Paga0.jpg') # Lee la imagen que esta procesando

    dfConfig =pd.read_csv('default.csv', sep=',') # Lee el archivo con los puntos
    col =[]
    for i in range(int(len(dfConfig)/2)+1): # verifica cuantos puntos hay(datos a extraer)
        col.append("dato"+ str(i))
    dfPrueba =pd.DataFrame(columns=col) # Crea un DF temporal
    dfCopy = dfConfig
    # Este while extrae todos los segmentos de la imagen en donde estan los datos
    while len(dfCopy) > 1: # desde el Df toma las filas 0 y 1 para extrer el dato
        rel =np.array([[dfCopy.iloc[0][0], dfCopy.iloc[0][1]], [dfCopy.iloc[1][0], dfCopy.iloc[1][1]]])  
        dfCopy.drop([0,1], axis=0, inplace=True) # Elimina las 2 primeras filas    
        dfCopy= dfCopy.reset_index(drop=True) # resetea el DF para eliminar 2 primeros indices
        imageOut = image[rel[0][1]:rel[1][1], rel[0][0]:rel[1][0]] # Extra el segmento de la imagen a procesar  
        result = reader.readtext(imageOut, paragraph=False)
        for res in result: # procesa el segmento de la imágen
            if res[2] >= 0.5:
                datos.append(res[1])
   
    file1 = pd.read_csv(fileSave) # Lee el archivo deon se guarda
    file1.loc[len(file1.index)] = datos # Aqui se guarda en la ultima posición del DF   
    file1.to_csv(fileSave, header=True, index=False, encoding = 'utf-8') # Guarda




def selectFolder():
    messagebox.showinfo(message="Elija el directorio que \ncontiene los archivos a procesar", title="Elegir directorio")
    folder_selected = fd.askdirectory(title= "Seleccione un directorio") # Abre un directorio
    folder_selected = folder_selected.replace('/', os.sep) # cambia el separador de la ruta
    messagebox.showinfo(message="Ahora elija donde guardar el archivo \ncon los datos procesados y asigne un nombre", title="Guardar archivo")
    fileSave =fd.asksaveasfilename(defaultextension='.csv',
    filetypes=[("Archivos .csv", '*.csv'), ("Todos",".*")], title="Guardar archivo") # Elige dode quiere guardar El archivo se salida

    dfConfig =pd.read_csv('default.csv', sep=',') # Lee el archivo donde estan los puntos
    col =[]
    for i in range(int(len(dfConfig)/2)+1): # Calcula cuantos puntos hay(cuantos datos debe extraer)
        col.append("dato"+ str(i)) # Asigna un nombre para cada columna del DF

    df=pd.DataFrame(columns=col) # Crea un DF con el nombre de las columnas
    df.to_csv(fileSave, header=True, index=False,  encoding = 'utf-8') # Guarda el archivo donde se almacenara la info
    if folder_selected:
        
        contenido = os.listdir(folder_selected) # carga los nombres de los archivos
        listPdf = []
        for fichero in contenido: # selecciona solo los archivos con estensión .pdf
            if os.path.isfile(os.path.join(folder_selected, fichero)) and fichero.endswith('.pdf'):
                listPdf.append(fichero)

        if len(listPdf) > 0: # Si hay archivos en la carpeta
            for file in listPdf: # Recorre todos los archivos
                selectFile(folder_selected, file, fileSave) # Llama cada archivo para procesarlo

    
    
    
    
import cv2 as cv
import os
import numpy as np
from time import time

dataRuta = r'.\Data'
listaData = os.listdir( dataRuta )
#print('data',listaData)
ids = []
rostrosData = []
id = 0
tiempoInicial = time()
for fila in listaData:
    rutacompleta = dataRuta+'/'+fila
    print("Iniciando lectura....")

    for archivo in os.listdir(rutacompleta):
        print("Imagenes: ",fila+'/'+archivo)
        ids.append(id)
        rostrosData.append(cv.imread(rutacompleta+'/'+archivo,0))
    
    id=id+1
    tiempofinalLectura = time()
    tiempoTotalLectura = tiempofinalLectura - tiempoInicial
    print("Tiempo Total de lectura: ", tiempoTotalLectura)        

entrenamientoEigenFaceRecognizer=cv.face.EigenFaceRecognizer_create()

print('Iniciando el entrenamiento....espere:')
entrenamientoEigenFaceRecognizer.train(rostrosData, np.array(ids))
Tiempofinalentrenamiento = time()
tiempoTotalEntrenamiento = Tiempofinalentrenamiento-tiempofinalLectura

print("Tiempo de entrenamiento total:",tiempoTotalEntrenamiento)
entrenamientoEigenFaceRecognizer.write('entrenamientoEigenFaceRecognizer.xml')
print('Entrenamiento Finalizado')
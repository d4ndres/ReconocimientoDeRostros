import cv2 as cv
import os
import numpy as np
from time import time
import imutils

dataRuta=r'.\Data'
listaData = os.listdir(dataRuta)
entrenamientoEigenFaceRecognizer = cv.face.EigenFaceRecognizer_create()
entrenamientoEigenFaceRecognizer.read('entrenamientoEigenFaceRecognizer.xml')
ruidos = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
camara = cv.VideoCapture(0)

while True:
    respuesta, captura = camara.read()
    if respuesta == False:break
    captura = imutils.resize(captura,width=640)

    camara.set(cv.CAP_PROP_BRIGHTNESS, 0)
    camara.set(cv.CAP_PROP_CONTRAST, 45)
    camara.set(cv.CAP_PROP_SATURATION, 70)
    captura1 = captura.copy()    
    grises = cv.cvtColor(captura,cv.COLOR_BGR2GRAY)
    idcaptura = grises.copy()
    cara = ruidos.detectMultiScale(grises, 1.3 ,5)
    
    for(x,y,e1,e2) in cara:
        rostrocapturado = idcaptura[y:y+e2 , x:x+e1]
        rostrocapturado = cv.resize(rostrocapturado, (160,160),interpolation=cv.INTER_CUBIC)
        resultado = entrenamientoEigenFaceRecognizer.predict(rostrocapturado)
        cv.putText(captura1,'{}'.format(resultado) , (x,y-5), 1,1.3 ,(0,255,0), 1,cv.LINE_8)
        if resultado[1]<1300:
            cv.putText(captura1,'No encontrado' , (x,y-20), 2,1.1 ,(0,255,0), 1,cv.LINE_8)
            cv.rectangle(captura1,(x,y), (x+e1,y+e2),(255,100,0),5)
        else:
            cv.putText(captura1,'{}'.format(listaData[resultado[0]]) , (x,y-20), 2,0.7 ,(30,150,255), 1,cv.LINE_8)
            cv.rectangle(captura1,(x,y), (x+e1,y+e2),(255,100,0),5)


    cv.imshow("RECONOCIMIENTO FINAL",captura1)    
    cv.imshow("Resultados",captura)    
    if(cv.waitKey(1)==ord('s')):break   
camara.release()
cv.destroyAllWindows()
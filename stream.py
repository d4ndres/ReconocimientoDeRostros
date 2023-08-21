import cv2 as cv
import numpy as np
import os
from time import time

def encodingTomaDeDatos( name, times):
    ruta = './static/Data'
    if name != 'default' and name:
        ruta += f'/{name}' 

    lastTimeElement = 0
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    else:
        lastTimeElement = len( os.listdir(ruta) )

    cap = cv.VideoCapture(0)

    face_detector = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    muestras = 0

    while True:
        successes, frame = cap.read()
        
        copyFrame = frame.copy()
        if successes and muestras < times:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            # Dibujar rectangulos en la cara
            for (x,y,w,h) in faces:
                cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

                if len( faces ) == 1:
                    muestras += 1
                    rostroCapturado = copyFrame[y:y+h,x:x+w]
                    rostroCapturado = cv.resize(rostroCapturado, (160, 160), interpolation=cv.INTER_CUBIC)
                    cv.imwrite( f'{ruta}/image{muestras + lastTimeElement }.jpg', rostroCapturado )

            # Escribe en la esquina superior izquierda el numero de muestras
            cv.putText(frame, f'{name}: {muestras}/{times}' , (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        ( flag, encodedImage ) = cv.imencode(".jpg", frame )
        
        # print( "Muestras: ", muestras )

        if flag:
            yield( 
                b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' 
                + bytearray(encodedImage) 
                + b'\r\n'
                )
            
    cap.release()


def entrenamientoNN():
    ruta = './static/Data'
    listaDePersonas = os.listdir(ruta)
    
    entradas = []
    grupoDeSalida = []

    grupo = 0
    print("Recopilacion de modelos")
    for name in listaDePersonas:
        routeDirModel = f'{ruta}/{name}'

        for fileName in os.listdir(routeDirModel):
            routeFile = f'{routeDirModel}/{fileName}'
            image = cv.imread(routeFile, cv.IMREAD_GRAYSCALE)
            entradas.append(image)
            grupoDeSalida.append(grupo)
        grupo += 1


    print("Inicio entrenamiento")
    # face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer = cv.face.EigenFaceRecognizer_create()
    face_recognizer.train(entradas, np.array(grupoDeSalida))
    face_recognizer.write('entrenamientoEigenFaceRecognizer.xml')
    print("Fin entrenamiento")



def encodingReconocimiento():
    ruta = './static/Data'
    listaDePersonas = os.listdir(ruta)
    face_recognizer = cv.face.EigenFaceRecognizer_create()
    face_recognizer.read('entrenamientoEigenFaceRecognizer.xml')

    face_detector = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

    cap = cv.VideoCapture(0)

    while True:
        successes, frame = cap.read()        
        if successes:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            copyGray = gray.copy()
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

                rostroCapturado = copyGray[y:y+h,x:x+w]
                rostroCapturado = cv.resize(rostroCapturado, (160, 160), interpolation=cv.INTER_CUBIC)
                
                #( valor grupal, precisión 0 - 10000 )
                ( grupo, precision ) = face_recognizer.predict(rostroCapturado)
                precision = precision / 100
                cv.putText(frame, f'{precision}%' , (x,y-5), 1,1.3 ,(0,255,0), 1,cv.LINE_8)
                cv.putText(frame, str( listaDePersonas[grupo] ) , (x,y-20), 2,0.7 ,(30,150,255), 1,cv.LINE_8)
        

        ( flag, encodedImage ) = cv.imencode(".jpg", frame )
        if flag:
            yield( 
                b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' 
                + bytearray(encodedImage) 
                + b'\r\n'
                )
            
    cap.release()

                


        


        
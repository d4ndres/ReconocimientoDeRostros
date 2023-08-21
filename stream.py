import cv2 as cv
import os

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
    cap.set(cv.CAP_PROP_BRIGHTNESS, 22)
    cap.set(cv.CAP_PROP_CONTRAST, 35)
    cap.set(cv.CAP_PROP_SATURATION, 75)
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
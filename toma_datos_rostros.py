import cv2 as cv
import os
import imutils

#modelo='Harwey, Eileen'
modelo = str(input('Ingrese el nombre de la persona para tomar datos.. >'))
ruta1  = r'.\Data'
rutacompleta = ruta1 +'/'+ modelo

# LEER EL FACE ID PNG 
imagen_superpuesta = cv.imread("face1.png")
filasL, columnasL, _ = imagen_superpuesta.shape
imagen_superpuesta = cv.resize(imagen_superpuesta,(717,537))

# Binarizar el face id
logo_gris = cv.cvtColor(imagen_superpuesta, cv.COLOR_BGR2GRAY)
retm, mascara = cv.threshold(logo_gris,92,255,cv.THRESH_BINARY)
mascara_inv = cv.bitwise_not(mascara)
# Operaciones
logo_frente = cv.bitwise_and(imagen_superpuesta,imagen_superpuesta,mask=mascara_inv)

if not os.path.exists(rutacompleta):
    os.makedirs(rutacompleta)

# Clasificador de cascadas, ruidos
ruidos = cv.CascadeClassifier("haarcascade_frontalface_default.xml") 
camara = cv.VideoCapture(0)
#camara=cv.VideoCapture('ElonMusk.mp4')

id=0
count = 0
while True:

    # numero maximo de muestras
    if count == 20:
        break
    count += 1

    respuesta, captura = camara.read()
    if respuesta == False:break
    
    captura = imutils.resize( captura, width=1024)
    
    
    # Ajustar los valores de enfoque, contraste y saturación
    camara.set(cv.CAP_PROP_BRIGHTNESS, 22)
    camara.set(cv.CAP_PROP_CONTRAST, 35)
    camara.set(cv.CAP_PROP_SATURATION, 75)
    captura1 = captura.copy()
    alto, ancho = captura1.shape[:2]
    inicio_x = int(ancho * (1 - 0.7) / 2)
    fin_x = int(ancho * (1 + 0.7) / 2)
    inicio_y = int(alto * (1 - 0.7) / 2)
    fin_y = int(alto * (1 + 0.7) / 2)
    roi=captura1[inicio_y:fin_y, inicio_x:fin_x]
    
    #combinar imagenes
    frame_fondo = cv.bitwise_and(roi,roi,mask=mascara)
    res = cv.add(frame_fondo,logo_frente)
    captura1[inicio_y:fin_y, inicio_x:fin_x]=res
    #

    grises = cv.cvtColor(captura,cv.COLOR_BGR2GRAY)
    idcaptura = captura.copy() #Copia todas las propiedades de la captura
    
    cara = ruidos.detectMultiScale(grises,1.5,3)
    
    for(x,y,e1,e2) in cara:
        cv.rectangle(captura,(x,y),(x+e1,y+e2), (0,255,0) , 2)
        rostrocapturado = idcaptura[y:y+e2 , x:x+e1]
        rostrocapturado = cv.resize(rostrocapturado, (160,160),interpolation=cv.INTER_CUBIC)
        cv.imwrite(rutacompleta+'/imagen_{}.jpg'.format(id), rostrocapturado)
        id=id+1
  
    cv.imshow("CAPTURA DE IMAGENES",captura)
    cv.imshow("Resultado FINAL",captura1)


    if(cv.waitKey(1)==ord('s')):break   

camara.release()
cv.destroyAllWindows()
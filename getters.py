
import os

def getDictData():
    nameDir = "./static/Data"
    nombresCarpetas = [nombre for nombre in os.listdir(nameDir)]
    
    dataImage = {}
    for nombre in nombresCarpetas:
        ruta = nameDir + "/" + nombre
        dataImage[nombre] = [ "Data/" + nombre + "/" + nombreImagen for nombreImagen in os.listdir(ruta)]
    return dataImage

def getListData(name):
    nameDir = "./static/Data/" + name
    return [ "Data/" + name + "/" + nombreImagen for nombreImagen in os.listdir(nameDir)]

def deleteListRoutes( listRoutes ):
    for route in listRoutes:
        os.remove( './static/'+route)
    return True
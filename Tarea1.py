import threading as th

def leerArchivo():
    with open("file0.data",'r') as archivo: #Para que funcione, el archivo debe estar en el mismo directorio en donde se esta ejecutando 
        read = archivo.readlines()
    sillasE,barberos,sillasB = map(int, read[0].split())
    clientes = []
    for i in read[1:]:
        clientes.append(list(map(int, i.split())))
    return sillasE,barberos,sillasB,clientes









sillasE,barberos,sillasB,clientes = leerArchivo()

print(sillasE, "",barberos,"",sillasB)
print(clientes)
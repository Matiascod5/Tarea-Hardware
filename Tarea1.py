import threading as th
import time as t 
import random as r

def leerArchivo():
    with open("file10.data",'r') as archivo: #Para que funcione, el archivo debe estar en el mismo directorio en donde se esta ejecutando 
        read = archivo.readlines()
    sillasE,barberos,sillasB = map(int, read[0].split())
    clientes = []
    for i in read[2:]:
        clientes.append(list(map(int, i.split())))
    return sillasE,barberos,sillasB,clientes


sillasE,barberos,sillasB,clientes = leerArchivo()
#num_clientes =  len(clientes)

print(sillasE, "",barberos,"",sillasB)
print(clientes)

#sem_entra_cliente = th.Semaphore(num_clientes)
sem_sillasE = th.Semaphore(sillasE)
sem_Barberos = th.Semaphore(barberos)
sem_sillasB = th.Semaphore(sillasB)
sem_listoParaCorte = th.Semaphore(0)
sem_clienteAtendido = th.Semaphore(0)
sem_mostrar = th.Semaphore(1)


#Variables globales
g_sillasE = sillasE
g_sillasB = sillasB
g_barberos = barberos


def Cortarpelo(num_cliente):
    global g_sillasE
    global g_sillasB
    global g_barberos

    #Entra un cliente
    sem_mostrar.acquire()
    print(f"entra cliente {num_cliente} a barberia\n")
    sem_mostrar.release()

    t.sleep(r.randrange(3))
    
    #Se sienta un cliente
    sem_sillasE.acquire()
    g_sillasE = g_sillasE - 1
    numSilla_espera = sillasE - g_sillasE
    sem_mostrar.acquire()
    print(f"cliente {num_cliente} usa silla de espera {numSilla_espera}\n")
    sem_mostrar.release()
    
    #Se sienta un cliente en una silla de barbero
    sem_sillasB.acquire()
    g_sillasB = g_sillasB - 1
    g_sillasE = g_sillasE + 1 #Aumenta el numero de sillas de espera
    numSilla_barbero = sillasB - g_sillasB
    sem_mostrar.acquire()
    print(f"cliente {num_cliente} usa silla de barbero {numSilla_barbero}\n")
    sem_mostrar.release()
    sem_sillasB.release()
    #t.sleep(r.randrange(timepoCorteCliente))

    #Barbero corta el pelo 
    sem_listoParaCorte.release()
    t.sleep(r.randrange(3))

    sem_Barberos.acquire()
    g_barberos= g_barberos- 1
    num_barbero = barberos-g_barberos
    sem_mostrar.acquire()
    print(f"barbero {num_barbero} atiende a cliente {num_cliente}\n")
    sem_mostrar.release()
    sem_Barberos.release()

    #Cliente Listo
    sem_clienteAtendido.acquire()
    g_barberos = g_barberos + 1 #Aumenta la cantidad de sillas de barberos
    g_barberos = g_barberos + 1 #Aumenta la cantidad de barberos
    sem_mostrar.acquire()
    print(f"sale cliente {num_cliente} (atendido por completo)\n")
    sem_mostrar.release()
    t.sleep(r.randrange(3))


    #t.sleep(r.randrange(3))


def Barbero():
    global g_sillasB

    while(True): #Entrada de clientes
        sem_listoParaCorte.acquire()

        sem_Barberos.acquire()
        sem_Barberos.release()

        sem_clienteAtendido.release()

        sem_mostrar.acquire()
        g_sillasB = g_sillasB + 1
        sem_mostrar.release()


th_barberos = []

for i in range(barberos):
    th_barb = th.Thread(target=Barbero)
    th_barb.setDaemon(True)
    th_barberos.append(th_barb)
    th_barb.start()


th_clientes = []
num_clientes =  len(clientes)

for j in range(num_clientes):
    th_cliente = th.Thread(target = Cortarpelo, args = [j])
    th_cliente.setDaemon(True)
    th_clientes.append(th_cliente)
    th_cliente.start()
    t.sleep(r.randrange(2))

for k in th_clientes:
    th_cliente.join()

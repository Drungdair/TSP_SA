from enum import Enum
from decimal import *
import os
import math

class Point:
    x = float
    y = float
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Tipos de instancias en TSPlib
"""
class Distance_type(Enum):
    EUC_2D = "EUC_2D"
    CEIL_2D = "CEIL_2D"
    GEO = "GEO"
    ATT = "ATT"
"""
Distance_type = ("EUC_2D","CEIL_2D","GEO","ATT")
# Arreglo de estructuras que contiene las coordenadas, Tipo Point
nodeptr = []
# Variable que indica el tipo de distancia
distance_type = Distance_type
# Matriz de distancia: distancia de nodos i a j
distance = [[]]
# Lista de vecinos mas cercanos: para cada nodo i una lista de vecinos ordenados
nn_list = [[]]
# Numero de nodos
n = int
# Nombre del archivo de instancia
name = str

def TSPlibReader(tsp_file_name):
    # Funcion: Constructor clase TSPlibReader
    # Input: Ruta al archivo de la instancia
    global nodeptr
    try:
        # Leer instancia desde un archivo
        nodeptr = read_etsp(tsp_file_name)
    except:
        print("Error: No se tiene acceso al archivo.")
        exit()
    # Obtener la matriz de distancias
    #compute_distances()
    # Generar listas de vecinos ordenados
    #compute_nn_lists()
    print(f"# instancia {name} tiene {n} nodos")

def read_etsp (tsp_file_name):
    # Funcion: lectura y parsing de instancia TSPlib
    # Input: ruta al archivo de instancia
    # Output: arreglo de coordenas
    # Comentario: archivo de instancia debe estar en formato TSPLIB
    global buf
    global distance_type
    nodeptr = []
    global name
    global n
    # Encontrado seccion de coordenadas
    found_coord_section = False

    if (tsp_file_name == None):
        print("Error: Instancia no especificada, abortando...")
        exit()

    if(not(os.access(tsp_file_name, os.R_OK))):
        print(f"Error: No se puede leer el archivo {tsp_file_name}")
        exit()
        
    print(f"# Leyendo archivo TSPlib {tsp_file_name} ... ")
    archivo = open(tsp_file_name, "r")
    linea = archivo.readline()
    while linea:
        if(linea.find("EOF") != -1):
            break
        if(found_coord_section == False):
            if(linea.startswith("NAME")):
                name = linea[linea.find(":")+2:len(linea)-1]
            elif(linea.startswith("TYPE") and linea.find("TSP") == -1):
                print("Instancia no esta en el formato TSPLIB !!")
                exit()
            elif(linea.startswith("DIMENSION")):
                n = int(linea[linea.find(":")+2 : len(linea)-1])
            else:
                if(linea.startswith("EDGE_WEIGHT_TYPE")):
                    buf = linea[linea.find(":")+2 : len(linea)-1]
                    if(buf == "EUC_2D"):
                        distance_type = Distance_type[0]
                    elif(buf == "CEIL_2D"):
                        distance_type = Distance_type[1]
                    elif(buf == "GEO"):
                        distance_type = Distance_type[2]
                    elif(buf == "ATT"):
                        distance_type = Distance_type[3]
                    else:
                        print(f"EDGE_WEIGHT_TYPE {buf} no implementado en la clase.")
                        exit()
        else:
            info_ciudad = linea.split()
            nodeptr.append(Point(float(info_ciudad[1]),float(info_ciudad[2])))
        
        if (linea.startswith("NODE_COORD_SECTION")):
            found_coord_section = True

        linea = archivo.readline()
  
    if (found_coord_section == False):
        print("Error: Ocurrio al buscar el inicio de las coordenadas !!")
        exit()

    archivo.close()
    return nodeptr

def round_distance (i, j):
    # Funcion: computa la distancia Euclidiana (redondea al siguiente entero) entre dos nodos
    # Input: indices de dos nodos
    # Output: distancia entre dos nodos
    # Comentarios: para una definicion de como calcular esta distancia vea TSPLIB
    #              la funcion round, rendondea al entero mas cercano
    #              en caso de ser 1.5 -> 2 y 2.5 -> 2
    
    diferencia_x = Decimal(f"{nodeptr[i].x}") - Decimal(f"{nodeptr[j].x}")
    diferencia_y = Decimal(f"{nodeptr[i].y}") - Decimal(f"{nodeptr[j].y}")
    distancia = round(math.sqrt(pow(diferencia_x,2) + pow(diferencia_y,2)),2)
    #print(f"Diferencia x = {diferencia_x}, Diferencia y = {diferencia_y}, Distancia = {distancia}, Redondeado = {round(distancia)}")
    return round(distancia)

def ceil_distance (i, j):
    # Funcion: computa la distancia Euclidiana (usando funcion techo) entre dos nodos
    # Input: indices de dos nodos
    # Output: distancia entre dos nodos
    # Comentarios: para una definicion de como calcular esta distancia vea TSPLIB
    #              la funcion math, redondea al entero mayor
    #              en caso de ser 1.1 -> 2 y 1.9 -> 2

    diferencia_x = Decimal(f"{nodeptr[i].x}") - Decimal(f"{nodeptr[j].x}")
    diferencia_y = Decimal(f"{nodeptr[i].y}") - Decimal(f"{nodeptr[j].y}")
    distancia = round(math.sqrt(pow(diferencia_x,2) + pow(diferencia_y,2)),2)
    return math.ceil(distancia)

#def geo_distance (i, j):
    # Funcion: computa la distancia geometrica (redondeada al siguiente entero)
    #          entre dos nodos
    # Input: indices de dos nodos
    # Output: distancia entre dos nodos
    # Comentarios: adaptada desde el codigo de concorde. Para una definicion de
    #              como calcular esta distancia vea TSPLIB



TSPlibReader("Hola mundo.tsp")

print(round_distance(1,2))
print(ceil_distance(1,2))

"""
for punto in nodeptr:
    print(f"[{punto.x}, {punto.y}]")
"""
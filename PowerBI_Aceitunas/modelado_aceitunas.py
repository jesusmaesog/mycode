import csv
from tokenize import PseudoExtras
import numpy as np
import pandas as pd
import math

#Ahora vamos a leer un archivo csv

with open('aceitunas.csv', newline='\n') as csvfile:
     reader = csv.reader(csvfile, delimiter = ",")
     for provincia, Peso, valor, unidades, mes, anyo in reader:
        print (provincia, Peso, valor, unidades, mes, anyo)

#Ahora vamos a crear los encabezamientos de la tabla en una variable llamada campos. Usamos los métodos para asignarlos y en el for creamos un diccionario con el método writerow
# del writer y así te crearía las filas.

#with open('contactos.csv', 'w', newline='\n') as csvfile:
#    campos = ['nombre', 'puesto', 'email']
#    writer = csv.DictWriter(csvfile, fieldnames = campos)
#    writer.writeheader()
#    for nombre, puesto, email in contactos:
#        writer.writerow({'nombre':nombre, 'puesto': puesto, 'email': email})
#        print (nombre, puesto, email)



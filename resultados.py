import pandas as pd
import sqlite3
import os

def escribir_archivo(archivo, contenido):
    archivo1 = open(archivo, 'w')
    archivo1.write(contenido)
    archivo1.close()

def cargar_archivo(archivo):
    archivo = open(archivo, 'r')
    data = archivo.readlines()
    archivo.close()
    for i in range(len(data)):
        data[i] = data[i].strip("\n")
        if ',' in data[i]:
            data[i] =data[i].split(',')
    return data

def crear_archivos_csv(con,letra):
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT * FROM variables where variables like "{letra}%"')
    rows = cursorObj.fetchall()
    texto2 = ''
    for row in rows:
        texto2 += str(row[1])+';'+str(row[2]) + '\n'
    escribir_archivo(f'Variable {letra.upper()}.csv',texto2)
        
def run():
    df = pd.read_csv('testout.csv')
    df.to_csv('Solucion1.csv', index=False)

    texto = cargar_archivo('Solucion1.csv')
    texto.insert(0, ['variables','valor'])

    texto1 = ''
    for i in texto:
        texto1 += i[0]+','+i[1]+'\n'

    escribir_archivo('Solucion1.csv',texto1)

    os.remove('solucion_variables.db')
    con = sqlite3.connect('solucion_variables.db')

    df = pd.read_csv('Solucion1.csv',sep=',',encoding='utf-8')
    df.to_sql('variables', con)

    variables = ['v','k','w','z','y','x','j','tetha','delta','tau']
    for i in variables:
        crear_archivos_csv(con, i)

    con.commit()
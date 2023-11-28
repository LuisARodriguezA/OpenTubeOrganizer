# librerias
# --------------------------------------------------------------------------------------
import pandas as pd
from tabulate import tabulate
# --------------------------------------------------------------------------------------
# assets
from assets import lista_indice_menu
from assets import menu
# --------------------------------------------------------------------------------------
def main():
    setup() # Hacemos un setup inicial para asegurarnos que el dataframe este bien creado
    menu() # Empezamos con el menú o "interfaz de usuario"
# --------------------------------------------------------------------------------------
def menu():
    
    # Mensage de bienvenida
    print(menu)
    
    # Chekeamos que el input del usuario sea valido antes de pasarlo
    while True:
        entrada = input("Ingresa el indice para seleccionar una opción: ")
        if entrada not in lista_indice_menu: 
            print("Entrada no valida, vuelve a intentarlo")
            continue
        break
    
    # Redirección a la función requerida
    if entrada == lista_indice_menu[0]:
        feed()
    elif entrada == lista_indice_menu[1]:
        canales()
    elif entrada == lista_indice_menu[2]:
        categorias()
    elif entrada == lista_indice_menu[3]:
        borrar()
    elif entrada == lista_indice_menu[4]:
        exit()
# --------------------------------------------------------------------------------------
def setup():
    # Intentar cargar el DataFrame desde el archivo existente
    try:
        # df = pd.read_csv('canales.csv', index_col='Nombre del canal')
        df = pd.read_csv('canales.csv')
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        df = pd.DataFrame(columns=['Nombre del canal', 'Categaoría', 'Enlace del último video'])
        # df.set_index('Nombre del canal', inplace=True)
        df.index.names = ['Indices']
        # df.columns.names= ['group']
        df.to_csv('canales.csv') # Guardar el DataFrame al final del programa o cuando se realicen cambios
# --------------------------------------------------------------------------------------
def feed():
    df = pd.read_csv('canales.csv')
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print("Bienvenido a OpenTubeOrganizer, ¿Que deseas hacer?\n a. Ver lista de subscripciones\n b. Agregar/Borrar canal\n c. Agregar/Borrar categoría\n d. Borrar información\n e. Salir")

    while True:
        entrada = input("Ingresa el indice para seleccionar una opción: ")
        if entrada not in lista_indice_menu: 
            print("Entrada no valida, vuelve a intentarlo")
            continue
        break
    
    # Redirección a la función requerida
    if entrada == lista_indice_menu[0]:
        feed()
    elif entrada == lista_indice_menu[1]:
        canales()
    elif entrada == lista_indice_menu[2]:
        categorias()
    elif entrada == lista_indice_menu[3]:
        borrar()
    elif entrada == lista_indice_menu[4]:
        exit()
# --------------------------------------------------------------------------------------
def canales():
    print("N/A")
# --------------------------------------------------------------------------------------
def categorias():
    print("N/A")
# --------------------------------------------------------------------------------------
def borrar():
    print("N/A")
# --------------------------------------------------------------------------------------
main()
# --------------------------------------------------------------------------------------
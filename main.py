# librerias
# --------------------------------------------------------------------------------------
import pandas as pd
from tabulate import tabulate
from pytube import YouTube
import os
import webbrowser
# --------------------------------------------------------------------------------------
# assets
from assets import lista_indice_menu
from assets import menu_inicial
from assets import lista_indice_feed
from assets import menu_feed
from assets import separador
lista_categorias = ['default']
# --------------------------------------------------------------------------------------
def main():
    os.system('cls')
    setup() # Hacemos un setup inicial para asegurarnos que el dataframe este bien creado
    menu() # Empezamos con el menú o "interfaz de usuario"
# --------------------------------------------------------------------------------------
def menu():
    
    # Mensage de bienvenida
    print(menu_inicial)
    
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
        while True:
            respuesta = input("Que quieres hacer (1 para agregar, 2 para borrar): ")

            if respuesta == '1':
                canales()
            elif respuesta == '2':
                borrar_canales()
            else:
                print("No entiendo esa respuesta, vuelve a intentarlo.")
                continue
            break
    elif entrada == lista_indice_menu[2]:
        categorias()
    elif entrada == lista_indice_menu[3]:
        borrar()
    elif entrada == lista_indice_menu[4]:
        exit()
# --------------------------------------------------------------------------------------
def setup():
    # Intentar cargar el DataFrame de categorías desde el archivo existente
    try:
        categorias_df = pd.read_csv('categorias.csv')
    except FileNotFoundError:
        # Si el archivo no existe, o si está vacío, crear un DataFrame con la categoría default
        categorias_df = pd.DataFrame({'Categoría': ['default']})

    # Intentar cargar el DataFrame de canales desde el archivo existente
    try:
        df = pd.read_csv('canales.csv')
        df.index.names = ['Index']
    except FileNotFoundError:
        # Si el archivo no existe, o si está vacío, crear un DataFrame vacío
        df = pd.DataFrame(columns=['Nombre del canal', 'Categoría', 'Link canal'])
        df.to_csv('canales.csv', index=False)  # Guardar el DataFrame al final del programa o cuando se realicen cambios

    # Si el DataFrame de categorías está vacío, crear uno nuevo con la categoría default
    if categorias_df.empty:
        categorias_df = pd.DataFrame({'Categoría': ['default']})

    # Guardar el DataFrame de categorías en categorias.csv
    categorias_df.to_csv('categorias.csv', index=False)
# --------------------------------------------------------------------------------------
def feed():
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']
    categorias_unicas = df['Categoría'].unique()
    os.system('cls')
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print(menu_feed)

    while True:
        entrada = input("Ingresa el indice para seleccionar una opción: ")
        if entrada not in lista_indice_feed: 
            print("Entrada no valida, vuelve a intentarlo")
            continue
        break
    
    # Redirección a la función requerida
    if entrada == lista_indice_feed[0]:
        abrir_canal()
    elif entrada == lista_indice_feed[1]:
        imprimir_una_sola_categoria()
    elif entrada == lista_indice_feed[2]:
        print("N/A")
    elif entrada == lista_indice_feed[3]:
        menu()
# --------------------------------------------------------------------------------------
def canales():
    os.system('cls')
    enlace_video_ejemplo = input("Pega el enlace de uno de los videos del canal que quieres agregar: " )
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']
    agregar_canal_desde_enlace(enlace_video_ejemplo, df)
# --------------------------------------------------------------------------------------
def categorias():
    os.system('cls')
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']

    # Cargar DataFrame de categorías desde el archivo existente
    try:
        categorias_df = pd.read_csv('categorias.csv')
        categorias_unicas = categorias_df['Categoría'].unique()
    except FileNotFoundError:
        # Si el archivo no existe, o si está vacío, crear un DataFrame con la categoría default
        categorias_df = pd.DataFrame({'Categoría': ['default']})
        categorias_unicas = ['default']

    lista_categorias = categorias_unicas.tolist()

    # Mostrar categorías actuales
    print("Categorías actuales:")
    for i, categoria in enumerate(lista_categorias):
        print(f"{i + 1}. {categoria}")

    while True:
        entrada = input("Ingresa el número de la acción que deseas realizar:\n1. Agregar categoría\n2. Quitar categoría\n3. Volver al menú principal\n")

        if entrada == '1':
            nueva_categoria = input("Ingresa el nombre de la nueva categoría: ")

            # Verificar si la nueva categoría ya existe en la lista
            if nueva_categoria in lista_categorias:
                print(f"La categoría '{nueva_categoria}' ya existe. Por favor, elige otra.")
                continue

            # Agregar la nueva categoría a la lista y al DataFrame
            lista_categorias.append(nueva_categoria)
            categorias_df = pd.concat([categorias_df, pd.DataFrame({'Categoría': [nueva_categoria]})], ignore_index=True)
            print(f"Categoría '{nueva_categoria}' agregada con éxito.")

        elif entrada == '2':
            # Mostrar categorías existentes para quitar
            print("Categorías existentes:")
            for i, categoria in enumerate(lista_categorias):
                print(f"{i + 1}. {categoria}")

            # Solicitar al usuario el índice de la categoría que desea quitar
            try:
                indice_quitar = int(input("Ingrese el número de la categoría que desea quitar: "))
            except ValueError:
                print("Por favor, ingrese un índice válido.")
                continue

            # Verificar si el índice proporcionado es válido
            if indice_quitar < 1 or indice_quitar > len(lista_categorias):
                print("Índice fuera de rango. Por favor, ingrese un índice válido.")
                continue

            categoria_a_quitar = lista_categorias[indice_quitar - 1]
            lista_categorias.remove(categoria_a_quitar)
            categorias_df = pd.DataFrame({'Categoría': lista_categorias})
            print(f"Categoría '{categoria_a_quitar}' quitada con éxito.")

            # Setear la categoría a "default" para todos los canales que tenían la categoría eliminada
            df.loc[df['Categoría'] == categoria_a_quitar, 'Categoría'] = 'default'

        elif entrada == '3':
            break
        else:
            print("Entrada no válida. Por favor, elige una opción válida.")

    # Guardar el DataFrame de categorías actualizado
    categorias_df.to_csv('categorias.csv', index=False)

    # Guardar el DataFrame de canales actualizado
    df.to_csv('canales.csv', index=False)

    # Regresar al menú principal
    menu()
# --------------------------------------------------------------------------------------
def borrar():
    os.system('cls')
    print("PILAS, VAS A BORRAR TODA TU INFORMACIÓN DE CANALES Y CATEGORÍAS, Y REINICIARÁS LA APP. ¿ESTÁS SEGURO?")
    
    if input("Escribe 'Estoy seguro' para continuar, de lo contrario escribe cualquier otra cosa: ") == "Estoy seguro":
        # Borrar archivos de canales y categorías
        try:
            os.remove("canales.csv")
            os.remove("categorias.csv")
        except FileNotFoundError:
            pass  # No hay archivos para borrar

        # Inicializar la app nuevamente
        main()
    else:
        print("Mmmm, no creo que estés seguro.")
        main()

# --------------------------------------------------------------------------------------
def agregar_canal_desde_enlace(enlace_video, df):
    os.system('cls')
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']

    # Cargar DataFrame de categorías desde el archivo existente
    try:
        categorias_df = pd.read_csv('categorias.csv')
        categorias_unicas = categorias_df['Categoría'].unique()
    except FileNotFoundError:
        # Si el archivo no existe, o si está vacío, crear un DataFrame con la categoría default
        categorias_df = pd.DataFrame({'Categoría': ['default']})
        categorias_unicas = ['default']

    try:
        # Crear un objeto YouTube utilizando el enlace del video
        yt_video = YouTube(enlace_video)

        # Obtener información del canal
        nombre_canal = yt_video.author

        print("Lista de Categorías:")
        for i, categoria in enumerate(categorias_unicas):
            print(f"{i + 1}. {categoria}")
        seleccion = int(input(f"Seleccione el índice de la categoría para el canal {nombre_canal}: ")) - 1
        categoria = categorias_unicas[seleccion]

        # Obtener la identificación del video del último video
        ultimo_video_id = yt_video.video_id

        # Verificar si el canal ya existe en el DataFrame
        if nombre_canal in df['Nombre del canal'].values:
            print(f"El canal '{nombre_canal}' ya está en la lista.")
            main()

        # Concatenar el DataFrame temporal con el DataFrame principal
        df.loc[len(df.index)] = [nombre_canal, categoria, str("https://www.youtube.com/@" + nombre_canal.lower())]

        print(f"Canal '{nombre_canal}' agregado con éxito.")
        print(df)

    except Exception as e:
        print(f"Error al agregar el canal: {str(e)}")
        respuesta = input("Regresar al menú o salir de la APP\n 1. APP\n 2. MENU\n")
        while True:
            respuesta = input("Por favor, elige una opción (1 para menu, 2 para salir): ")

            if respuesta == '1':
                menu()
            elif respuesta == '2':
                exit()
            else:
                print("No entiendo esa respuesta, vuelve a intentarlo.")
                continue
            break

    # Guardar el DataFrame actualizado
    df.to_csv('canales.csv', index=False)
    menu()

# --------------------------------------------------------------------------------------
def borrar_canales():
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']
    # Imprimir el DataFrame actual con los canales
    print("Canales actuales:")
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

    # Solicitar al usuario el índice del canal que desea borrar
    try:
        indice_borrar = int(input("Ingrese el índice del canal que desea borrar: "))
    except ValueError:
        print("Por favor, ingrese un índice válido.")
        return

    # Verificar si el índice proporcionado es válido
    if indice_borrar < 0 or indice_borrar >= len(df):
        print("Índice fuera de rango. Por favor, ingrese un índice válido.")
        menu()

    # Borrar el canal
    canal_borrado = df.loc[indice_borrar, 'Nombre del canal']
    df = df.drop(index=indice_borrar).reset_index(drop=True)

    print(f"Canal '{canal_borrado}' ha sido borrado.")
    menu()

    # Guardar el DataFrame actualizado
    df.to_csv('canales.csv', index=False)
    menu()

# --------------------------------------------------------------------------------------
def imprimir_una_sola_categoria():
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']

    # Intentar cargar el DataFrame de categorías desde el archivo existente
    try:
        categorias_df = pd.read_csv('categorias.csv')
        categorias_unicas = categorias_df['Categoría'].unique()
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame con la categoría default
        categorias_df = pd.DataFrame({'Categoría': ['default']})
        categorias_unicas = ['default']

    os.system('cls')

    # Mostrar categorías existentes
    print("Categorías existentes:")
    for i, categoria in enumerate(categorias_unicas):
        print(f"{i + 1}. {categoria}")

    # Solicitar al usuario el índice de la categoría
    while True:
        try:
            seleccion = int(input("Seleccione el índice de la categoría: ")) - 1

            # Verificar si el índice proporcionado es válido
            if seleccion < 0 or seleccion >= len(categorias_unicas):
                raise ValueError("Índice fuera de rango.")
            
            break  # Salir del bucle si no hay errores

        except ValueError as e:
            print(f"Error: {e}. Ingresa un número válido.")

    categoria_seleccionada = categorias_unicas[seleccion]

    # Verificar si la categoría seleccionada está en el DataFrame de canales
    if categoria_seleccionada not in df['Categoría'].unique():
        print(f"No hay canales en la categoría '{categoria_seleccionada}'. Volviendo al menú principal.")
        menu()

    # Imprimir un DataFrame con solo la categoría seleccionada
    print(tabulate(df[df['Categoría'] == categoria_seleccionada], headers='keys', tablefmt='psql'))
    print(separador)
    menu()

# --------------------------------------------------------------------------------------
def abrir_canal():
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']

    # Verificar si hay canales en el DataFrame
    if df.empty:
        print("No hay canales disponibles para abrir. Volviendo al menú principal.")
        menu()

    os.system('cls')

    # Mostrar los canales existentes
    print(tabulate(df, headers='keys', tablefmt='psql'))
    
    # Solicitar al usuario el índice del canal que desea abrir
    while True:
        try:
            indice_abrir = int(input("Ingrese el índice del canal que desea abrir: ")) - 1

            # Verificar si el índice proporcionado es válido
            if indice_abrir < 0 or indice_abrir >= len(df):
                raise ValueError("Índice fuera de rango.")
            
            break  # Salir del bucle si no hay errores

        except ValueError as e:
            print(f"Error: {e}. Ingresa un número válido.")

    # Obtener el enlace del canal seleccionado
    enlace_canal = df.loc[indice_abrir, 'Link canal']

    # Abrir el canal en el navegador web
    webbrowser.open(enlace_canal)

    print(f"Abriendo el canal '{df.loc[indice_abrir, 'Nombre del canal']}' en el navegador.")
    menu()
# --------------------------------------------------------------------------------------
main()
# --------------------------------------------------------------------------------------

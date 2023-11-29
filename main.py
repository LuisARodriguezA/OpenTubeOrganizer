# librerias
# --------------------------------------------------------------------------------------
import pandas as pd
from tabulate import tabulate
from pytube import YouTube
import os
# --------------------------------------------------------------------------------------
import webbrowser
firefox_path = 'C:/Program Files/Mozilla Firefox/firefox.exe'
incognito_browser = webbrowser.get(firefox_path + ' -private-window %s')
# --------------------------------------------------------------------------------------
# assets
from assets import lista_indice_menu
from assets import menu_inicial
from assets import lista_indice_feed
from assets import menu_feed
from assets import separador
from bs4 import BeautifulSoup
import requests
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
        mostrar_y_modificar_categoria()
    elif entrada == lista_indice_menu[4]:
        borrar()
    elif entrada == lista_indice_menu[5]:
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
        df = pd.read_csv('canales.csv')
        df.index.names = ['Index']
        estadisticas(df)
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
        df.loc[len(df.index)] = [nombre_canal, categoria, str("https://www.youtube.com/@" + (nombre_canal.lower())).replace(" ", "")]

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
# def imprimir_una_sola_categoria():

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

    # Filtrar el DataFrame por la categoría seleccionada
    df_filtrado = df[df['Categoría'] == categoria_seleccionada]

    # Imprimir un DataFrame con solo la categoría seleccionada
    print(tabulate(df_filtrado, headers='keys', tablefmt='psql'))
    print(separador)

    # Preguntar al usuario si desea abrir un canal o todos los canales desde la categoría filtrada
    while True:
        respuesta = input("¿Quieres abrir un canal o todos los canales desde esta categoría? (Canal/Todos/No): ").lower()
        
        if respuesta == 'canal' or respuesta == 'c':
            abrir_canal_desde_categoria(df_filtrado)
            break
        elif respuesta == 'todos' or respuesta == 't':
            abrir_todos_los_canales_desde_categoria(df_filtrado)
            break
        elif respuesta == 'no' or respuesta == 'n':
            menu()
        else:
            print("Respuesta no válida. Ingresa 'Canal', 'Todos' o 'No'.")

def abrir_todos_los_canales_desde_categoria(df_filtrado):
    for enlace_canal in df_filtrado['Link canal']:
        # Abrir cada canal en el navegador web
        incognito_browser.open(enlace_canal)

    print(f"Abriendo todos los canales de la categoría '{df_filtrado.iloc[0]['Categoría']}' en el navegador.")
    menu()
def abrir_canal_desde_categoria(df_filtrado):
    # Solicitar al usuario el índice del canal que desea abrir desde la categoría filtrada
    while True:
        try:
            indice_abrir = int(input("Ingrese el índice del canal que desea abrir: "))

            # Verificar si el índice proporcionado es válido
            if indice_abrir < 0 or indice_abrir > len(df_filtrado):
                raise ValueError("Índice fuera de rango.")
            
            break  # Salir del bucle si no hay errores

        except ValueError as e:
            print(f"Error: {e}. Ingresa un número válido.")

    # Obtener el enlace del canal seleccionado desde la categoría filtrada
    enlace_canal = df_filtrado.iloc[indice_abrir]['Link canal']

    # Abrir el canal en el navegador web
    incognito_browser.open(enlace_canal)

    print(f"Abriendo el canal '{df_filtrado.iloc[indice_abrir]['Nombre del canal']}' en el navegador.")
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
            indice_abrir = int(input("Ingrese el índice del canal que desea abrir: "))

            # Verificar si el índice proporcionado es válido
            if indice_abrir < 0 or indice_abrir > len(df):
                raise ValueError("Índice fuera de rango.")
            
            break  # Salir del bucle si no hay errores

        except ValueError as e:
            print(f"Error: {e}. Ingresa un número válido.")

    # Obtener el enlace del canal seleccionado
    enlace_canal = df.loc[indice_abrir, 'Link canal']

    # Abrir el canal en el navegador web
    incognito_browser.open(enlace_canal)

    print(f"Abriendo el canal '{df.loc[indice_abrir, 'Nombre del canal']}' en el navegador.")
    menu()

# --------------------------------------------------------------------------------------
import pandas as pd
from tabulate import tabulate
from bs4 import BeautifulSoup
import requests
from pytube import YouTube

def get_channel_links(df):
    return df['Link canal'].tolist()

def get_latest_video_statistics(channel_link):
    try:
        # Get the HTML content of the channel page
        response = requests.get(channel_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the link to the latest video on the channel page
        latest_video_link = soup.find('a', {'href': '/watch'})
        
        if latest_video_link is None:
            print(f"No se pudo encontrar el enlace al último video para el canal: {channel_link}")
            return None
        
        video_url = f'https://www.youtube.com{latest_video_link["href"]}'

        # Get video details using PyTube
        yt_video = YouTube(video_url)
        stats = {
            'Nombre del canal': yt_video.author,
            'Título del último video': yt_video.title,
            'Vistas del último video': yt_video.views,
            'Likes del último video': yt_video.likes,
            'Dislikes del último video': yt_video.dislikes,
        }
        return stats
    except Exception as e:
        print(f"Error al obtener estadísticas del último video: {str(e)}")
        return None

def estadisticas(df):
    # Total de canales en el DataFrame principal
    total_canales = len(df)

    # Total de categorías
    categorias_df = pd.read_csv('categorias.csv')
    total_categorias = len(categorias_df)

    # Cantidad de canales por categoría
    canales_por_categoria = df['Categoría'].value_counts().reset_index()
    canales_por_categoria.columns = ['Categoría', 'Canales']

    # Estadísticas del último video de cada canal
    latest_video_stats_df = pd.DataFrame(columns=['Nombre del canal', 'Título del último video', 'Vistas del último video', 'Likes del último video', 'Dislikes del último video'])
    channel_links = get_channel_links(df)

    for channel_link in channel_links:
        video_stats = get_latest_video_statistics(channel_link)
        if video_stats:
            latest_video_stats_df = latest_video_stats_df.append(video_stats, ignore_index=True)

    # Imprimir estadísticas
    print(f"Total de canales en el DataFrame principal: {total_canales}")
    print(f"Total de categorías: {total_categorias}")

    print("\nCanales por categoría:")
    print(tabulate(canales_por_categoria, headers='keys', tablefmt='psql'))

    print("\nResumen del último video de cada canal:")
    print(tabulate(latest_video_stats_df, headers='keys', tablefmt='psql'))
# --------------------------------------------------------------------------------------

def mostrar_y_modificar_categoria():
    
    try:
        # Leer el DataFrame desde el archivo CSV de canales
        df_canales = pd.read_csv('canales.csv')
        df_canales.index.names = ['Index']

        # Mostrar el DataFrame actual con los canales
        print("Canales actuales:")
        print(df_canales)

        # Solicitar al usuario el índice del canal que desea modificar
        while True:
            try:
                indice_modificar = int(input("Ingrese el índice del canal que desea modificar: "))
                if indice_modificar < 0 or indice_modificar >= len(df_canales):
                    raise ValueError("Índice fuera de rango.")
                break  # Salir del bucle si no hay errores
            except ValueError:
                print("Por favor, ingrese un índice válido.")

        # Obtener el nombre del canal y su categoría actual
        canal_modificar = df_canales.loc[indice_modificar, 'Nombre del canal']
        categoria_actual = df_canales.loc[indice_modificar, 'Categoría']

        # Mostrar información del canal seleccionado
        print(f"\nCanal seleccionado: {canal_modificar}")
        print(f"Categoría actual: {categoria_actual}")

        # Mostrar las categorías disponibles
        try:
            df_categorias = pd.read_csv('categorias.csv')
            categorias_disponibles = df_categorias['Categoría'].tolist()
        except FileNotFoundError:
            categorias_disponibles = ['default']

        print("\nCategorías disponibles:")
        for i, categoria in enumerate(categorias_disponibles):
            print(f"{i + 1}. {categoria}")

        # Solicitar al usuario la nueva categoría
        while True:
            try:
                nueva_categoria_indice = int(input("Ingrese el índice de la nueva categoría: "))
                nueva_categoria = categorias_disponibles[nueva_categoria_indice - 1]
                break  # Salir del bucle si no hay errores
            except (ValueError, IndexError):
                print("Por favor, ingrese un índice válido.")

        # Modificar la categoría del canal en el DataFrame
        df_canales.loc[indice_modificar, 'Categoría'] = nueva_categoria

        # Guardar el DataFrame actualizado en el archivo CSV de canales
        df_canales.to_csv('canales.csv', index=False)

        print(f"\nCategoría de '{canal_modificar}' modificada exitosamente a '{nueva_categoria}'.")
    except Exception as e:
        print(f"Error: {str(e)}")

# --------------------------------------------------------------------------------------
main()
# --------------------------------------------------------------------------------------

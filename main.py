lista_indice = ["a","b","c","d","e"]
initial_setup = 0
def main():
    setup()
    menu()

def menu():
    
    print("Bienvenido a OpenTubeOrganizer, ¿Que deseas hacer?\n a. Ver lista de subscripciones\n b. Agregar/Borrar canal\n c. Agregar/Borrar categoría\n d. Borrar información\n e. Salir")
    while True:
        entrada = input("Ingresa el indice para seleccionar una opción: ")
        if entrada not in lista_indice: 
            print("Entrada no valida, vuelve a intentarlo")
            continue
        break
    
    print("Entrada valida")

    if entrada == lista_indice[0]:
        feed()
    elif entrada == lista_indice[1]:
        canales()
    elif entrada == lista_indice[2]:
        categorias()
    elif entrada == lista_indice[3]:
        borrar()
    elif entrada == lista_indice[4]:
        exit()

def setup():
    if initial_setup == 0
    else:
main()
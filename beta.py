import pandas as pd

# Intentar cargar el DataFrame desde el archivo existente
try:
    df = pd.read_csv('canales.csv', index_col='Nombre del canal')
except FileNotFoundError:
    # Si el archivo no existe, crear un DataFrame vacío
    df = pd.DataFrame(columns=['Nombre del canal', 'Categoría', 'Enlace del último video'])
    df.set_index('Nombre del canal', inplace=True)

# ... Resto de tu código ...

# Guardar el DataFrame al final del programa o cuando se realicen cambios
df.to_csv('canales.csv')

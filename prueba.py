from prettytable import PrettyTable

numero_varZ = (int(input("Digite el numero de variables en Z: ")))
numero_inec = (int(input("Digite el numero de inecuaciones: ")))
num_filas = numero_inec + 1
num_colum = numero_inec + numero_varZ + 2
matriz_1 = []
matriz_2 = []
lista = []
respuestas = {}
global salidaaux
salidaaux = 1
global colum_pivote  # Definimos colum_pivote como global
colum_pivote = None  # Inicializamos colum_pivote


# Pregunta al usuario si quiere maximizar o minimizar
maximizar = input("¿Desea maximizar la función objetivo? (s/n): ").strip().lower() == 's'
def crear_matriz(matriz):
    for i in range(num_filas):
        matriz.append([])
        for j in range(num_colum):
            matriz[i].append(None)
    return matriz

def encontrar_columpiv(matriz):
    num_pivoteZ = 0
    global colum_pivote
    for j in range(num_colum):
        if matriz[num_filas - 1][j] < 0 and matriz[num_filas - 1][j] < num_pivoteZ:
            num_pivoteZ = matriz[num_filas - 1][j]
            colum_pivote = j

"""def encontrar_elemento_pivote(matriz):
    global fila_pivot
    num_menor = 1000
    for i in range(num_filas - 1):
        if matriz[i][colum_pivote]==0 or matriz[i][num_colum - 1] / matriz[i][colum_pivote] < 0:
            continue
        else:
            if i == 0:
                num_menor = matriz[i][num_colum - 1] / matriz[i][colum_pivote]
                fila_pivot = i
                elemento_pivote = matriz_1[i][colum_pivote]
            elif matriz[i][num_colum - 1] / matriz[i][colum_pivote] < num_menor:
                num_menor = matriz[i][num_colum - 1] / matriz[i][colum_pivote]
                fila_pivot = i
                elemento_pivote = matriz[i][colum_pivote]
    lista.append(fila_pivot)
    return elemento_pivote
"""
def encontrar_elemento_pivote(matriz):
    global fila_pivot, colum_pivote  # Asegúrate de definir colum_pivote como global
    num_colum = len(matriz[0])  # Asignamos el número total de columnas
    num_filas = len(matriz)  # Asignamos el número total de filas
    num_menor = float('inf')  # Inicializamos num_menor a infinito

    for i in range(num_filas - 1):  # Iteramos sobre las filas, excepto la última (Z)
        # Verificamos que la columna pivote no sea cero y que el cociente sea positivo
        if matriz[i][colum_pivote] == 0 or matriz[i][colum_pivote] <= 0:
            continue
        
        # Calculamos el cociente
        cociente = matriz[i][num_colum - 1] / matriz[i][colum_pivote]
        
        # Actualizamos si encontramos un cociente menor
        if cociente < num_menor:
            num_menor = cociente
            fila_pivot = i
            elemento_pivote = matriz[i][colum_pivote]

    # Si no se encontró un elemento pivote, se puede manejar como se desee (ej: imprimir mensaje)
    if 'elemento_pivote' not in locals():
        print("No se encontró un elemento pivote válido.")
        return None

    return elemento_pivote

def fila_entrante(matriznueva,matrizvieja):
    for j in range(num_colum):
        matriznueva[fila_pivot][j] = matrizvieja[fila_pivot][j] / elemento_pivote


def reorganizar_matriz(matriznueva):
    for i in range(num_filas):
        for j in range(num_colum):
            if i != fila_pivot:
                matriz_2[i][j] = matriz_1[i][j]-(matriz_1[i][colum_pivote]*matriz_2[fila_pivot][j])

def hay_negativos(matriznueva):
    negativo = None
    for j in range(num_colum-1):
        if matriznueva[num_filas-1][j] < 0:
            salidaaux = 1
            negativo = matriznueva[num_filas-1][j]
        elif negativo == None:
            salidaaux = 0
    return salidaaux

def imprimir_matriz(matriz):
    table = PrettyTable()

    # Crear los encabezados de la tabla
    headers = []

    # Agregar nombres de las columnas para las variables de decisión (x1, x2, ...)
    for j in range(1, numero_varZ + 1):
        headers.append(f"x{j}")

    # Agregar columnas para las variables slack (S1, S2, ...)
    for j in range(1, numero_inec + 1):
        headers.append(f"S{j}")

    headers.append("RHS")  # Columna para los términos independientes (derecha de la desigualdad)

    table.field_names = [" "] + headers  # Agregar espacio para las etiquetas de las filas

    # Llenar las filas de la tabla
    for i in range(num_filas):
        # Etiquetas para las filas
        if i < numero_inec:
            row_label = f"X{i + 1}"  # Etiquetas de las restricciones (S1, S2, ...)
        elif i == num_filas - 1:
            row_label = "Z"  # Etiqueta para la función objetivo
        
        # Llenar los valores de la fila
        row = [row_label]  # Comienza con la etiqueta de la fila
        for j in range(1, num_colum):  # Ajustamos el rango para que coincida con los encabezados
            value = matriz[i][j]
            
            # Formatear los valores numéricos para que tengan dos decimales
            if isinstance(value, (int, float)):
                row.append(f"{value:.2f}")
            else:
                row.append(value)
        
        # Asegurarse de que el número de valores en 'row' coincida con 'headers'
        if len(row) == len(headers) + 1:  # Se suma 1 por la columna extra de etiquetas de filas
            table.add_row(row)
        else:
            print(f"Error: la fila tiene {len(row)} valores, pero se esperaban {len(headers) + 1}")

    # Alinear las columnas al centro
    table.align = "c"

    # Ajustar el ancho de las columnas
    table.hrules = True  # Añadir reglas horizontales entre filas para mayor claridad

    print(table)
    
def limpiar_matriz(matriznueva, matrizvacia):
    for i in range(num_filas):
        for j in range(num_colum):
            matriznueva[i][j]=matrizvacia[i][j]

for i in range(num_filas):
    if i < num_filas-1:
        respuestas["S" + str(i+1)]= 0
    else:
        respuestas["Z"] = 0

matriz_1= crear_matriz(matriz_1)
matriz_2= crear_matriz(matriz_2)


print("PROGRAMA METODO SIMPLEX")
for i in range(num_filas):
    for j in range(num_colum):
        if j == 0 and i != num_filas - 1:
            matriz_1[i][j] = 0
        elif j == 0 and i == num_filas - 1:
            matriz_1[i][j] = 1
        elif 0 < j <= numero_varZ and i != num_filas - 1:
            matriz_1[i][j] = int(
                input("Digite el coeficiente de la variable " + str(j) + " de la ecuacion " + str(i + 1) + ": "))
        elif j == num_colum - 1 and i != num_filas - 1:
            matriz_1[i][j] = float(input("Digite el coeficiente al que esta igualado la ecuacion " + str(i + 1) + ": "))
        elif 0 < j <= numero_varZ and i == num_filas - 1:
            matriz_1[i][j] =int(input("Digite el coeficiente de la variable " + str(j) + " de la funcion Z: "))
            matriz_1[i][j] = matriz_1[i][j]*(-1)
        elif j == num_colum - 1 and i == num_filas - 1:
            matriz_1[i][j] = 0
        elif  numero_varZ < j < num_colum-1:
            if i== j - numero_varZ-1:
                matriz_1[i][j] = 1
            else:
                matriz_1[i][j] = 0
# Multiplicar toda la fila Z por -1 si no se maximiza
if not maximizar:
    for j in range(1, numero_varZ + 1):  # Multiplicamos los coeficientes de Z
        matriz_1[num_filas - 1][j] *= -1


colum_pivote = 0
while salidaaux == 1:
    imprimir_matriz(matriz_1)
    encontrar_columpiv(matriz_1)
    elemento_pivote = encontrar_elemento_pivote(matriz_1)
    fila_entrante(matriz_2, matriz_1)
    reorganizar_matriz(matriz_2)
    salidaaux = hay_negativos(matriz_1)
    print(str(salidaaux))
    print(elemento_pivote)
    for i in range(num_filas):
        if i == fila_pivot:
            try:
                respuestas["X" + str(i + 1)] = respuestas.pop("S" + str(i + 1))
            except:
                respuestas["X" + str(i + 1)] = matriz_2[i][num_colum - 1]
        elif i == num_filas - 1:
            respuestas["Z"] = matriz_2[i][num_colum - 1]

    for i in range(num_filas):
        for j in range(len(lista)):
            if i == lista[j]:
                respuestas["X" + str(i + 1)] = matriz_2[i][num_colum - 1]

    for i in range(num_filas):
        for j in range(num_colum):
            matriz_1[i][j]=matriz_2[i][j]
    for i in range(num_filas):
        for j in range(num_colum):
            matriz_2[i][j]= None

print("Respuestas: ")
for key, value in respuestas.items():
    # Formateamos la salida para mostrar los valores correctamente
    if key == "Z":
        print(f"{key} = {value:.2f}")
    else:
        print(f"{key} = {value:.2f}")



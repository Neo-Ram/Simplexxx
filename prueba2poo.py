from prettytable import PrettyTable

class Simplex:
    def __init__(self, numero_varZ, numero_inec, maximizar):
        self.numero_varZ = numero_varZ
        self.numero_inec = numero_inec
        self.num_filas = numero_inec + 1
        self.num_colum = numero_inec + numero_varZ + 2
        self.matriz_1 = []
        self.matriz_2 = []
        self.respuestas = {}
        self.lista = []
        self.salidaaux = 1
        self.colum_pivote = None
        self.fila_pivot = None
        self.maximizar = maximizar

        # Inicialización de las matrices y respuestas
        self.crear_matriz(self.matriz_1)
        self.crear_matriz(self.matriz_2)
        for i in range(self.num_filas):
            if i < self.num_filas - 1:
                self.respuestas[f"S{i + 1}"] = 0
            else:
                self.respuestas["Z"] = 0

    def crear_matriz(self, matriz):
        for i in range(self.num_filas):
            matriz.append([None] * self.num_colum)

    def encontrar_columpiv(self):
        num_pivoteZ = 0
        for j in range(self.num_colum):
            if self.matriz_1[self.num_filas - 1][j] < 0 and self.matriz_1[self.num_filas - 1][j] < num_pivoteZ:
                num_pivoteZ = self.matriz_1[self.num_filas - 1][j]
                self.colum_pivote = j

    def encontrar_elemento_pivote(self):
        num_menor = float('inf')
        self.fila_pivot = None  # Inicializamos la fila pivote como None
        self.elemento_pivote = None  # Asegúrate de inicializar elemento_pivote aquí
        for i in range(self.num_filas - 1):
            if self.matriz_1[i][self.colum_pivote] == 0 or self.matriz_1[i][self.colum_pivote] <= 0:
                continue
            cociente = self.matriz_1[i][self.num_colum - 1] / self.matriz_1[i][self.colum_pivote]
            if cociente < num_menor:
                num_menor = cociente
                self.fila_pivot = i
                self.elemento_pivote = self.matriz_1[i][self.colum_pivote]
        if self.elemento_pivote is None:  # Verificar si no se encontró un pivote
            print("No se encontró un elemento pivote válido.")
            return None
        return self.elemento_pivote

    def fila_entrante(self):
        for j in range(self.num_colum):
            self.matriz_2[self.fila_pivot][j] = self.matriz_1[self.fila_pivot][j] / self.elemento_pivote

    def reorganizar_matriz(self):
        for i in range(self.num_filas):
            for j in range(self.num_colum):
                if i != self.fila_pivot:
                    self.matriz_2[i][j] = self.matriz_1[i][j] - (self.matriz_1[i][self.colum_pivote] * self.matriz_2[self.fila_pivot][j])

    def hay_negativos(self):
        negativo = None
        for j in range(self.num_colum - 1):
            if self.matriz_1[self.num_filas - 1][j] < 0:
                self.salidaaux = 1
                negativo = self.matriz_1[self.num_filas - 1][j]
            elif negativo is None:
                self.salidaaux = 0
        return self.salidaaux

    def imprimir_matriz(self):
        table = PrettyTable()
        headers = []

        for j in range(1, self.numero_varZ + 1):
            headers.append(f"x{j}")

        for j in range(1, self.numero_inec + 1):
            headers.append(f"S{j}")

        headers.append("RHS")

        table.field_names = [" "] + headers

        for i in range(self.num_filas):
            row_label = f"X{i + 1}" if i < self.numero_inec else "Z"
            row = [row_label]
            for j in range(1, self.num_colum):
                value = self.matriz_1[i][j]
                row.append(f"{value:.2f}" if isinstance(value, (int, float)) else value)

            if len(row) == len(headers) + 1:
                table.add_row(row)
            else:
                print(f"Error: la fila tiene {len(row)} valores, pero se esperaban {len(headers) + 1}")

        table.align = "c"
        table.hrules = True
        print(table)

    def limpiar_matriz(self):
        for i in range(self.num_filas):
            for j in range(self.num_colum):
                self.matriz_2[i][j] = None

    def ejecutar_simplex(self):
        for i in range(self.num_filas):
            for j in range(self.num_colum):
                if j == 0 and i != self.num_filas - 1:
                    self.matriz_1[i][j] = 0
                elif j == 0 and i == self.num_filas - 1:
                    self.matriz_1[i][j] = 1
                elif 0 < j <= self.numero_varZ and i != self.num_filas - 1:
                    self.matriz_1[i][j] = int(input(f"Digite el coeficiente de la variable {j} de la ecuacion {i + 1}: "))
                elif j == self.num_colum - 1 and i != self.num_filas - 1:
                    self.matriz_1[i][j] = float(input(f"Digite el coeficiente al que esta igualada la ecuacion {i + 1}: "))
                elif 0 < j <= self.numero_varZ and i == self.num_filas - 1:
                    self.matriz_1[i][j] = int(input(f"Digite el coeficiente de la variable {j} de la funcion Z: ")) * (-1)
                elif j == self.num_colum - 1 and i == self.num_filas - 1:
                    self.matriz_1[i][j] = 0
                elif self.numero_varZ < j < self.num_colum - 1:
                    self.matriz_1[i][j] = 1 if i == j - self.numero_varZ - 1 else 0

        if not self.maximizar:
            for j in range(1, self.numero_varZ + 1):
                self.matriz_1[self.num_filas - 1][j] *= -1

        while self.salidaaux == 1:
            self.imprimir_matriz()
            self.encontrar_columpiv()
            self.encontrar_elemento_pivote()
            self.fila_entrante()
            self.reorganizar_matriz()
            self.salidaaux = self.hay_negativos()
            self.actualizar_respuestas()

            for i in range(self.num_filas):
                for j in range(self.num_colum):
                    self.matriz_1[i][j] = self.matriz_2[i][j]
            self.limpiar_matriz()

        print("Respuestas:")
        for key, value in self.respuestas.items():
            print(f"{key} = {value:.2f}")

    def actualizar_respuestas(self):
        for i in range(self.num_filas):
            if i == self.fila_pivot:
                try:
                    self.respuestas[f"X{i + 1}"] = self.respuestas.pop(f"S{i + 1}")
                except:
                    self.respuestas[f"X{i + 1}"] = self.matriz_2[i][self.num_colum - 1]
            elif i == self.num_filas - 1:
                self.respuestas["Z"] = self.matriz_2[i][self.num_colum - 1]

        for i in range(self.num_filas):
            for j in range(len(self.lista)):
                if i == self.lista[j]:
                    self.respuestas[f"X{i + 1}"] = self.matriz_2[i][self.num_colum - 1]


if __name__ == "__main__":
    numero_varZ = int(input("Digite el numero de variables en Z: "))
    numero_inec = int(input("Digite el numero de inecuaciones: "))
    maximizar = input("¿Desea maximizar la función objetivo? (s/n): ").strip().lower() == 's'

    simplex = Simplex(numero_varZ, numero_inec, maximizar)
    simplex.ejecutar_simplex()

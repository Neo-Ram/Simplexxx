from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from fastapi import File, UploadFile
# Inicializamos FastAPI
app = FastAPI()

class ProblemData(BaseModel):
    maximizar: bool
    coeficientes: list[float]
    restricciones: list[list[float]]  # Lista de restricciones, como una lista

@app.post("/simplex")
#Metodo que recibe parametros como JSON
async def resolver_simplex(data: ProblemData):
    try:
        simplex = Simplex(data.maximizar, data.coeficientes, data.restricciones)
        resultados = simplex.ejecutar_simplex()
        return {"resultados": resultados}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/simplex/file")
#Metodo que recibe parametros de un txt
async def resolver_simplex_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Leer el contenido del archivo
        data = contents.decode('utf-8').strip()  # Decodificar y quitar espacios
        lines = data.split('\n')  # Separar líneas
        
        # Procesar la primera línea para obtener la maximización y coeficientes
        first_line = lines[0].split(',')
        maximizar = first_line[0].strip().lower() == 'true'
        coeficientes = list(map(float, first_line[1:]))  # Convertir a float

        # Aqui procesa las líneas restantes para obtener las restricciones
        restricciones = []
        for line in lines[1:]:
            if line.strip():  # Ignora líneas vacías
                restricciones.append(list(map(float, line.split(','))))

        # Llama a la clase Simplex con los datos procesados
        simplex = Simplex(maximizar, coeficientes, restricciones)
        resultados = simplex.ejecutar_simplex()
        
        return {"resultados": resultados}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/")
def root():
    return {"message": "API funcionando"}

class Simplex:
    def __init__(self, maximizar: bool, coeficientes: List[float], restricciones: List[List[float]]):
        self.numero_varZ = 3  # Número fijo de variables
        self.numero_inec = 3  # Número fijo de restricciones
        self.coeficientes = coeficientes  # Coeficientes de la función objetivo
        self.restricciones = restricciones  # Lista de listas para restricciones
        self.num_filas = self.numero_inec + 1
        self.num_colum = self.numero_inec + self.numero_varZ + 2
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
        self.fila_pivot = None
        self.elemento_pivote = None
        for i in range(self.num_filas - 1):
            if self.matriz_1[i][self.colum_pivote] == 0 or self.matriz_1[i][self.colum_pivote] <= 0:
                continue
            cociente = self.matriz_1[i][self.num_colum - 1] / self.matriz_1[i][self.colum_pivote]
            if cociente < num_menor:
                num_menor = cociente
                self.fila_pivot = i
                self.elemento_pivote = self.matriz_1[i][self.colum_pivote]
        if self.elemento_pivote is None:
            raise ValueError("No se encontró un elemento pivote válido.")
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

    def limpiar_matriz(self):
        for i in range(self.num_filas):
            for j in range(self.num_colum):
                self.matriz_2[i][j] = None

    def ejecutar_simplex(self):
        # Inicializa la matriz utilizando los coeficientes y restricciones 
        self.matriz_1 = [[0] * self.num_colum for _ in range(self.num_filas)]
        
        # Rellenar la matriz con los coeficientes de Z y las restricciones
        for i in range(self.num_filas - 1):
            for j in range(self.numero_varZ):
                self.matriz_1[i][j] = self.restricciones[i][j]
            self.matriz_1[i][self.num_colum - 1] = self.restricciones[i][-1]  # (RHS)

        # Coeficientes de la función objetivo
        for j in range(self.numero_varZ):
            self.matriz_1[self.num_filas - 1][j] = -self.coeficientes[j]  # Maximización o minimización
        
        # Verifica si es un problema de maximización o minimización
        if not self.maximizar:
            for j in range(self.numero_varZ):
                self.matriz_1[self.num_filas - 1][j] *= -1

        while self.salidaaux == 1:
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

        # Devuelve las respuestas finales en formato JSON
        return self.respuestas

    def actualizar_respuestas(self):
        for i in range(self.num_filas):
            if i == self.fila_pivot:
                try:
                    self.respuestas[f"X{i + 1}"] = self.respuestas.pop(f"S{i + 1}")
                except:
                    self.respuestas[f"X{i + 1}"] = self.matriz_2[i][self.num_colum - 1]
            elif i == self.num_filas - 1:
                self.respuestas["Z"] = self.matriz_2[i][self.num_colum - 1]


import heapq
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------- PARTE 1: Lectura y construcción de datos ----------

def crear_Archivo():
    with open("ciudades.txt", "w") as archivo:
        archivo.write("Guayaquil, Mitad del Mundo, 435.1\n")
        archivo.write("Quito, Cuenca, 460.3\n")
        archivo.write("Napo, Loja, 586.9\n")
        archivo.write("Ibarra, Baños de Agua Santa, 308.5\n")
        archivo.write("Manta, Tena, 567.7\n")
        archivo.write("Otavalo, Latacunga, 203\n")
        archivo.write("Santo Domingo, Manta, 246\n")
        archivo.write("Carchi, Quito, 184.5\n")
        archivo.write("Puyo, Riobamba, 136.4\n")
        archivo.write("Guayaquil, Machala, 183\n")

def leer_datos():
    rutas = []
    with open("ciudades.txt", "r") as archivo:
        for linea in archivo:
            L_partida, L_destino, distancia = linea.strip().split(",")
            rutas.append((L_partida.strip(), L_destino.strip(), float(distancia.strip())))
    return rutas

def lista_adyacencia_para_dijkstra(rutas):
    grafo = {}
    for origen, destino, distancia in rutas:
        if origen not in grafo:
            grafo[origen] = {}
        if destino not in grafo:
            grafo[destino] = {}

        grafo[origen][destino] = {'distancia': distancia, 'costo': distancia}
        grafo[destino][origen] = {'distancia': distancia, 'costo': distancia}
    return grafo

def matriz_ciudades(rutas):
    ciudades = []
    for p, d, _ in rutas:
        if p not in ciudades:
            ciudades.append(p)
        if d not in ciudades:
            ciudades.append(d)

    n = len(ciudades)
    matriz = [[float('inf') for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matriz[i][i] = 0.0

    for p, d, distancia in rutas:
        i = ciudades.index(p)
        j = ciudades.index(d)
        matriz[i][j] = distancia
        matriz[j][i] = distancia
    return ciudades, matriz

def mostrar_matriz(ciudades, matriz):
    print("\nMatriz de costos (Distancias en km):")
    etiquetas = [c[:5].ljust(6) for c in ciudades]
    encabezado = "      " + "".join(etiqueta for etiqueta in etiquetas)
    print(encabezado)
    for i, fila in enumerate(matriz):
        linea = ciudades[i][:5].ljust(6)
        for valor in fila:
            if valor == float('inf'):
                linea += "x     "
            else:
                linea += f"{valor:<6.1f}"
        print(linea)

# ---------- PARTE 2: Dijkstra ----------

def _dijkstra(inicio, tipo_costo='costo'):
    global grafo
    if inicio not in grafo:
        return {}, {}

    distancias = {nodo: float('inf') for nodo in grafo}
    predecesores = {nodo: None for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        costo_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, datos in grafo[nodo_actual].items():
            costo_arista = datos[tipo_costo]
            nuevo_costo = costo_actual + costo_arista

            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino))

    return distancias, predecesores

# ---------- PARTE 3: Funciones de consulta y actualización ----------

def consultar_ruta_optima(origen, destino, tipo_costo='costo'):
    global grafo
    if origen not in grafo or destino not in grafo:
        return [], "Una o ambas ciudades no existen en el grafo."

    distancias, predecesores = _dijkstra(origen, tipo_costo)

    if distancias[destino] == float('inf'):
        return [], f"No hay una ruta disponible de '{origen}' a '{destino}'."

    ruta = []
    actual = destino
    while actual:
        ruta.append(actual)
        actual = predecesores[actual]
    ruta.reverse()

    costo_total = distancias[destino]
    mensaje = f"Ruta: {' -> '.join(ruta)}\nCosto total ({tipo_costo}): {costo_total:.2f}"
    return ruta, mensaje

def agregar_o_actualizar_ciudad(nombre_ciudad):
    global grafo
    if nombre_ciudad not in grafo:
        grafo[nombre_ciudad] = {}
        return f"Ciudad '{nombre_ciudad}' agregada."
    else:
        return f"Ciudad '{nombre_ciudad}' ya existe."

def agregar_o_actualizar_conexion(origen, destino, distancia, costo):
    global grafo
    if origen not in grafo:
        agregar_o_actualizar_ciudad(origen)
    if destino not in grafo:
        agregar_o_actualizar_ciudad(destino)

    grafo[origen][destino] = {'distancia': distancia, 'costo': costo}
    grafo[destino][origen] = {'distancia': distancia, 'costo': costo}
    return f"Conexión entre '{origen}' y '{destino}' actualizada."

# ---------- INTERFAZ GRÁFICA ----------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutas Turísticas Óptimas")
        self.root.geometry("500x400")

        ttk.Button(root, text="Consultar Ruta Óptima", command=self.ventana_ruta).pack(pady=10)
        ttk.Button(root, text="Agregar/Actualizar Ciudad", command=self.ventana_ciudad).pack(pady=10)
        ttk.Button(root, text="Agregar/Actualizar Conexión", command=self.ventana_conexion).pack(pady=10)
        ttk.Button(root, text="Mostrar Ciudades", command=self.mostrar_ciudades).pack(pady=10)
        ttk.Button(root, text="Mostrar Conexiones", command=self.mostrar_conexiones).pack(pady=10)
        ttk.Button(root, text="Salir", command=root.quit).pack(pady=10)

    def ventana_ruta(self):
        win = tk.Toplevel(self.root)
        win.title("Ruta Óptima")

        tk.Label(win, text="Origen:").grid(row=0, column=0)
        tk.Label(win, text="Destino:").grid(row=1, column=0)

        origen = ttk.Combobox(win, values=list(grafo.keys()))
        destino = ttk.Combobox(win, values=list(grafo.keys()))
        origen.grid(row=0, column=1)
        destino.grid(row=1, column=1)

        tipo = tk.StringVar(value="costo")
        ttk.Radiobutton(win, text="Costo", variable=tipo, value="costo").grid(row=2, column=0)
        ttk.Radiobutton(win, text="Distancia", variable=tipo, value="distancia").grid(row=2, column=1)

        def calcular():
            _, info = consultar_ruta_optima(origen.get(), destino.get(), tipo.get())
            messagebox.showinfo("Resultado", info)

        ttk.Button(win, text="Consultar", command=calcular).grid(row=3, column=0, columnspan=2, pady=10)

    def ventana_ciudad(self):
        ciudad = simpledialog.askstring("Ciudad", "Nombre de la ciudad:")
        if ciudad:
            resultado = agregar_o_actualizar_ciudad(ciudad.strip())
            messagebox.showinfo("Resultado", resultado)

    def ventana_conexion(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Conexión")

        tk.Label(win, text="Origen:").grid(row=0, column=0)
        tk.Label(win, text="Destino:").grid(row=1, column=0)
        tk.Label(win, text="Distancia:").grid(row=2, column=0)
        tk.Label(win, text="Costo:").grid(row=3, column=0)

        origen = tk.Entry(win)
        destino = tk.Entry(win)
        distancia = tk.Entry(win)
        costo = tk.Entry(win)

        origen.grid(row=0, column=1)
        destino.grid(row=1, column=1)
        distancia.grid(row=2, column=1)
        costo.grid(row=3, column=1)

        def agregar():
            try:
                d = float(distancia.get())
                c = float(costo.get())
                res = agregar_o_actualizar_conexion(origen.get().strip(), destino.get().strip(), d, c)
                messagebox.showinfo("Éxito", res)
            except ValueError:
                messagebox.showerror("Error", "Distancia y costo deben ser numéricos.")

        ttk.Button(win, text="Agregar Conexión", command=agregar).grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_ciudades(self):
        texto = "\n".join(grafo.keys()) or "No hay ciudades."
        messagebox.showinfo("Ciudades", texto)

    def mostrar_conexiones(self):
        texto = ""
        for o, destinos in grafo.items():
            for d, datos in destinos.items():
                texto += f"{o} -> {d}: (Distancia: {datos['distancia']}, Costo: {datos['costo']})\n"
        messagebox.showinfo("Conexiones", texto or "No hay conexiones registradas.")

# ---------- INICIALIZACIÓN ----------

crear_Archivo()
rutas = leer_datos()
grafo = lista_adyacencia_para_dijkstra(rutas)

root = tk.Tk()
app = App(root)
root.mainloop()

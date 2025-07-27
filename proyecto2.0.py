
import heapq

def _dijkstra(inicio, tipo_costo='costo'):
    """
    Implementación del algoritmo de Dijkstra 
    """
    global grafo
    if inicio not in grafo:
        return {}, {}

    distancias = {nodo: float('inf') for nodo in grafo}
    predecesores = {nodo: None for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]  # (costo_acumulado, nodo)

    while cola_prioridad:
        costo_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, datos_conexion in grafo[nodo_actual].items():
            costo_arista = datos_conexion[tipo_costo]
            nuevo_costo = costo_actual + costo_arista

            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino))
    return distancias, predecesores


#Punto 4 

#Consultar el costo y la ruta óptima entre dos ciudades

def consultar_ruta_optima(origen, destino, tipo_costo='costo'):
    
    global grafo
    if origen not in grafo or destino not in grafo:
        print("Una o ambas ciudades no existen en el grafo.")
        return None, None

    distancias, predecesores = _dijkstra(origen, tipo_costo)

    if distancias[destino] == float('inf'):
        print(f"No hay una ruta disponible de '{origen}' a '{destino}'.")
        return None, None

    ruta = []
    actual = destino
    while actual:
        ruta.append(actual)
        actual = predecesores[actual]
    ruta.reverse()

    costo_total = distancias[destino]
    print(f"\nRuta óptima de '{origen}' a '{destino}' (por {tipo_costo}):")
    print(f"  Ruta: {' -> '.join(ruta)}")
    print(f"  Costo total ({tipo_costo}): {costo_total}")
    return ruta, costo_total

#Agregar nuevas ciudades o actualizar las existentes

def agregar_o_actualizar_ciudad(nombre_ciudad):
    """
    Agrega una nueva ciudad/punto turístico o verifica su existencia.
    """
    global grafo
    if nombre_ciudad not in grafo:
        grafo[nombre_ciudad] = {}
        print(f"Ciudad '{nombre_ciudad}' agregada.")
    else:
        print(f"Ciudad '{nombre_ciudad}' ya existe.")

def agregar_o_actualizar_conexion(origen, destino, distancia, costo):
    """
    Agrega o actualiza una conexión (arista) entre dos ciudades/puntos.
    Asegura que ambas ciudades existan en el grafo.
    """
    global grafo
    if origen not in grafo:
        agregar_o_actualizar_ciudad(origen)
    if destino not in grafo:
        agregar_o_actualizar_ciudad(destino)

    grafo[origen][destino] = {'distancia': distancia, 'costo': costo}
    # Asumimos rutas bidireccionales
    grafo[destino][origen] = {'distancia': distancia, 'costo': costo}
    print(f"Conexión de '{origen}' a '{destino}' (Distancia: {distancia}, Costo: {costo}) actualizada/agregada.")


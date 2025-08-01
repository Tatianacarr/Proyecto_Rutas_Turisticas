import heapq

# ---------- Estructuras ----------

grafo = {}
seleccion_cliente = []

zonas_turisticas = {
    "Costa": {
        "Guayas": ["Guayaquil", "Playas"],
        "Manabí": ["Manta", "Puerto López"]
    },
    "Sierra": {
        "Pichincha": ["Quito", "Mitad del Mundo"],
        "Tungurahua": ["Baños de Agua Santa"],
        "Imbabura": ["Otavalo", "Ibarra"]
    },
    "Oriente": {
        "Napo": ["Tena"],
        "Pastaza": ["Puyo"]
    }
}
# ---------- Usuario Administrador ----------

usuarios_predefinidos = [
    {
        "nombre": "Karen Lozano",
        "identificacion": "1234567890",
        "edad": "20",
        "correo": "adminkaren@gmail.com",
        "contrasena": "Admin1234",
        "rol": "Administrador"
    }
]

# ---------- Funciones Básicas ----------

def crear_Archivo():
    with open("ciudades.txt", "w") as archivo:
        archivo.write("Guayaquil, Mitad del Mundo, 435.1, 50\n")
        archivo.write("Quito, Cuenca, 460.3, 60\n")
        archivo.write("Napo, Loja, 586.9, 70\n")
        archivo.write("Ibarra, Baños de Agua Santa, 308.5, 40\n")
        archivo.write("Manta, Tena, 567.7, 65\n")
        archivo.write("Otavalo, Latacunga, 203, 30\n")
        archivo.write("Santo Domingo, Manta, 246, 35\n")
        archivo.write("Carchi, Quito, 184.5, 25\n")
        archivo.write("Puyo, Riobamba, 136.4, 20\n")
        archivo.write("Guayaquil, Machala, 183, 28\n")


def leer_datos():
    rutas = []
    with open("ciudades.txt", "r") as archivo:
        for linea in archivo:
            L_partida, L_destino, distancia, costo = linea.strip().split(",")
            rutas.append((L_partida.strip(), L_destino.strip(), float(distancia.strip()), float(costo.strip())))
    return rutas


def lista_adyacencia_para_dijkstra(rutas):
    grafo_local = {}
    for origen, destino, distancia, costo in rutas:
        if origen not in grafo_local:
            grafo_local[origen] = {}
        if destino not in grafo_local:
            grafo_local[destino] = {}

        grafo_local[origen][destino] = {'distancia': distancia, 'costo': costo}
        grafo_local[destino][origen] = {'distancia': distancia, 'costo': costo}
    return grafo_local


def _dijkstra(inicio, tipo_costo='costo'):
    global grafo
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

def consultar_ruta_optima(origen, destino, tipo_costo='costo'):
    distancias, predecesores = _dijkstra(origen, tipo_costo)
    if distancias[destino] == float('inf'):
        return [], f"No hay ruta disponible de {origen} a {destino}."
    ruta = []
    actual = destino
    while actual:
        ruta.append(actual)
        actual = predecesores[actual]
    ruta.reverse()
    costo_total = distancias[destino]
    mensaje = f"Ruta: {' -> '.join(ruta)}\nCosto total ({tipo_costo}): {costo_total:.2f}"
    return ruta, mensaje

# ---------- Validación y Usuarios ----------

def validar_contrasena(contrasena):
    tiene_mayuscula = any(c.isupper() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    return len(contrasena) >= 8 and tiene_mayuscula and tiene_numero

def registro_usuario():
    nombre = input("Ingrese su nombre y apellido: ")
    identificacion = input("Ingrese su identificación: ")
    edad = input("Ingrese su edad: ")
    usuario = input("Ingrese su correo electrónico: ")
    contrasena = input("Ingrese una contraseña segura: ")
    while not validar_contrasena(contrasena):
        print("Debe tener al menos 8 caracteres, una mayúscula y un número.")
        contrasena = input("Ingrese una contraseña segura: ")
    rol = ""
    while rol not in ["Administrador", "Cliente"]:
        rol = input("Rol (Cliente): ").strip()
    with open("usuarios.txt", "a") as f:
        f.write(f"{nombre},{identificacion},{edad},{usuario},{contrasena},{rol}\n")
    print("Registro exitoso. Inicie sesión.")

def iniciar_sesion():
    while True:
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        # Para la entrada de los usuarios con valores ya predefinidos
        for user in usuarios_predefinidos:
            if usuario == user["correo"] and contrasena == user["contrasena"]:
                print("Inicio de sesión exitoso.")
                return user["rol"], user["nombre"].split()[0]

        # Verificar en archivo
        try:
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")
                    if len(datos) >= 6 and datos[3] == usuario and datos[4] == contrasena:
                        print("Inicio de sesión exitoso.")
                        return datos[5], datos[0].split()[0]
        except FileNotFoundError:
            print("El archivo 'usuarios.txt' no existe.")
            return None, None

        print("Credenciales incorrectas. Inténtalo de nuevo.\n")


# ---------- Algoritmos ----------

def burbuja(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j].lower() > lista[j+1].lower():
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def seleccion(lista):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if lista[j].lower() < lista[min_idx].lower():
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista

def busqueda_lineal(lista, objetivo):
    return any(item.lower() == objetivo.lower() for item in lista)

def busqueda_binaria(lista, objetivo):
    lista = sorted(lista, key=lambda x: x.lower())
    inicio, fin = 0, len(lista)-1
    while inicio <= fin:
        mid = (inicio + fin) // 2
        if lista[mid].lower() == objetivo.lower():
            return True
        elif lista[mid].lower() < objetivo.lower():
            inicio = mid + 1
        else:
            fin = mid - 1
    return False

# ---------- Menús ----------

def menu_administrador():
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Agregar/Actualizar Ciudad o Conexión")
        print("2. Listar ciudades ordenadas")
        print("3. Buscar ciudad")
        print("4. Eliminar ciudad")
        print("5. Guardar en rutas.txt")
        print("6. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            o = input("Origen: ")
            d = input("Destino: ")
            dist = float(input("Distancia: "))
            costo = float(input("Costo: "))
            if o not in grafo:
                grafo[o] = {}
            if d not in grafo:
                grafo[d] = {}
            grafo[o][d] = {'distancia': dist, 'costo': costo}
            grafo[d][o] = {'distancia': dist, 'costo': costo}
        elif opcion == "2":
            lista = burbuja(list(grafo.keys())) if input("1. Burbuja 2. Selección: ") == "1" else seleccion(list(grafo.keys()))
            print("Ordenadas:", ", ".join(lista))
        elif opcion == "3":
            ciudad = input("Ciudad a buscar: ")
            existe = busqueda_lineal(list(grafo.keys()), ciudad) if input("1. Lineal 2. Binaria: ") == "1" else busqueda_binaria(list(grafo.keys()), ciudad)
            print("Encontrado" if existe else "No encontrado")
        elif opcion == "4":
            c = input("Ciudad a eliminar: ")
            if c in grafo:
                del grafo[c]
                for otros in grafo.values():
                    if c in otros:
                        del otros[c]
                print("Eliminado.")
        elif opcion == "5":
            with open("rutas.txt", "w") as f:
                for o, destinos in grafo.items():
                    for d, datos in destinos.items():
                        f.write(f"{o}, {d}, {datos['distancia']}, {datos['costo']}\n")

            print("Guardado en rutas.txt.")
        elif opcion == "6":
            break

def mostrar_arbol_zonas():
    print("\n--- ZONAS DISPONIBLES EN EL MAPA ---")
    for zona, provincias in zonas_turisticas.items():
        print(f"[{zona}]")
        for prov, lugares in provincias.items():
            disponibles = [lugar for lugar in lugares if lugar in grafo]
            if disponibles:
                print(f"  - {prov}: " + ", ".join(disponibles))


def seleccionar_ciudades():
    while True:
        ciudad = input("Ciudad a visitar (ENTER para terminar): ").strip()
        if ciudad == "":
            break
        if ciudad in grafo:
            seleccion_cliente.append(ciudad)
            print(f"'{ciudad}' añadida.")
        else:
            print("Ciudad no registrada.")

def listar_ciudades_seleccionadas():
    if not seleccion_cliente:
        print("No hay ciudades seleccionadas.")
        return
    ordenadas = burbuja(seleccion_cliente.copy()) if input("1. Burbuja 2. Selección: ") == "1" else seleccion(seleccion_cliente.copy())
    print("Ordenadas:", ", ".join(ordenadas))

def actualizar_o_eliminar_ciudad():
    if not seleccion_cliente:
        print("No hay ciudades seleccionadas.")
        return
    print("Seleccionadas:", seleccion_cliente)
    nombre = input("Ciudad a modificar: ")
    if nombre not in seleccion_cliente:
        print("No encontrada.")
        return
    accion = input("Actualizar (A) o Eliminar (E): ").upper()
    if accion == "E":
        seleccion_cliente.remove(nombre)
    elif accion == "A":
        nueva = input("Nuevo nombre: ")
        if nueva in grafo:
            i = seleccion_cliente.index(nombre)
            seleccion_cliente[i] = nueva
        else:
            print("Ciudad no registrada.")

def guardar_seleccion_cliente(nombre_cliente):
    if not seleccion_cliente:
        print("Nada que guardar.")
        return
    with open(f"rutas-{nombre_cliente.lower()}.txt", "w") as f:
        for c in seleccion_cliente:
            f.write(c + "\n")
    print("Guardado.")

def menu_cliente(nombre_cliente):
    while True:
        print("\n--- MENÚ CLIENTE ---")
        print("1. Ver mapa")
        print("2. Consultar ruta óptima")
        print("3. Explorar zonas")
        print("4. Seleccionar ciudades")
        print("5. Listar ciudades seleccionadas")
        print("6. Modificar selección")
        print("7. Guardar selección")
        print("8. Cerrar sesión")
        
        op = input("Opción: ").strip()

        if op == "1":
            if not grafo:
                print("No hay rutas registradas.")
            else:
                print("\n--- MAPA DE CONEXIONES ---")
                for o, destinos in grafo.items():
                 for d, datos in destinos.items():
                  print(f"{o} -> {d}: {datos['distancia']} km | ${datos['costo']} USD")


        elif op == "2":
            o = input("Origen: ").strip()
            d = input("Destino: ").strip()
            if o not in grafo or d not in grafo:
                print("Una o ambas ciudades no están registradas.")
            else:
                tipo = input("¿Buscar por 'costo' o 'distancia'?: ").strip().lower()
                if tipo not in ['costo', 'distancia']:
                    print("Tipo inválido. Solo se permite 'costo' o 'distancia'.")
                else:
                    _, info = consultar_ruta_optima(o, d, tipo)
                    print(info)

        elif op == "3":
            mostrar_arbol_zonas()

        elif op == "4":
            seleccionar_ciudades()

        elif op == "5":
            listar_ciudades_seleccionadas()

        elif op == "6":
            actualizar_o_eliminar_ciudad()

        elif op == "7":
            guardar_seleccion_cliente(nombre_cliente)

        elif op == "8":
            print("Sesión cerrada.")
            break

        else:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 8.")


# ---------- MAIN ----------

if __name__ == "__main__":
    crear_Archivo()
    rutas = leer_datos()
    grafo = lista_adyacencia_para_dijkstra(rutas)

    while True:
        print("\n--- BIENVENIDO AL SISTEMA ---")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            rol, nombre = iniciar_sesion()
            if rol == "Administrador":
                menu_administrador()
            elif rol == "Cliente":
                menu_cliente(nombre)
        elif opcion == "2":
            registro_usuario()
        elif opcion == "3":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

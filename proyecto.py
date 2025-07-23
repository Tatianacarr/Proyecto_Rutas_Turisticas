#1) leer datos de ciudades/puntos turisticos, distancias y costos desde un archivo.

def crear_Archivo():
    with open("ciudades.txt","w") as archivo:
        archivo.write("Guayaquil, Mitad del Mundo, 435.1\n")
        archivo.write("Quito, Cuenca, 460.3\n")
        archivo.write("Napo, Loja, 586.9\n")
        archivo.write("Ibarra, Baños de Agua Santa, 308.5\n")
        archivo.write("Quito, Esmeraldas, 317.5\n")

def leer_datos():
    rutas=[]
    with open("ciudades.txt","r") as archivo:    
        for linea in archivo:
            L_partida, L_destino, distancia = linea.strip().split(",")
            rutas.append((L_partida.strip(), L_destino.strip(), float(distancia)))
    return rutas

#2) construir una matriz de costos basada en las distancias entre ciudades/puntos turisticos.
                         
def matriz_ciudades(rutas):
    ciudades=[]
    for p, d, ruta in rutas:
        if p not in ciudades:
            ciudades.append(p)
        if d not in ciudades:
            ciudades.append(d)

    n=len(ciudades)
    matriz=[[float('inf') for columna in range(n)] for fila in range(n)]
    
    for i in range(n):
        matriz[i][i]=0

    for p, d, distancia in rutas:
        i=ciudades.index(p)
        j=ciudades.index(d)
        matriz[i][j]=distancia
        matriz[j][i]=distancia
    return ciudades, matriz

def mostrar_matriz(ciudades, matriz):
    print("Matriz de costos (Distancias en km): ")
    
    encabezado="      "
    for ciudad in ciudades:
        encabezado += f"{ciudad[:5]:<8} "
    print(encabezado)

    for i, fila in enumerate(matriz):
        linea=f"{ciudades[i][:5]:<6} "
        for valor in fila:
            if valor == float('inf'):
                linea += f"{'x':<8}"
            else:
                linea+=f"{valor:<8.1f}"
        print(linea)

#llamado a las funciones 
crear_Archivo()
rutas=leer_datos()
ciudades, matriz = matriz_ciudades(rutas)
mostrar_matriz(ciudades, matriz)





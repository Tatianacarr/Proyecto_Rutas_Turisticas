# Registro de usuario
def registro_usuario():
    nombre = input("Ingrese su nombre y apellido: ")
    identificacion = input("Ingrese su identificación: ")
    edad = int(input("Ingrese su edad: "))
    usuario = input("Ingrese su correo electrónico: ")
    contrasena = input("Ingrese una contraseña segura: ")

    while not validar_contrasena(contrasena):
        print("La contraseña debe tener al menos 8 caracteres, una letra mayúscula y un número.")
        contrasena = input("Ingrese una contraseña segura: ")

    guardar_datos(nombre, identificacion, edad, usuario, contrasena)
    print("Registro exitoso. Puede iniciar sesión.")

# Inicio de sesión
def iniciar_sesion():
    usuario = input("Ingrese su correo electrónico: ")
    contrasena = input("Ingrese su contraseña: ")

    with open("usuarios.txt", "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if datos[3] == usuario and datos[4] == contrasena:
                print("Inicio de sesión exitoso.")
                return
    print("Usuario o contraseña incorrectos.")

# Ejecución del programa
registro_usuario()
iniciar_sesion()
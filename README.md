def guardar_datos(nombre, identificacion, edad, usuario, contrasena):
    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{nombre},{identificacion},{edad},{usuario},{contrasena}\n")

# Validar contraseña segura
def validar_contrasena(contrasena):
    tiene_mayuscula = False
    tiene_numero = False
    
    for char in contrasena:
        if char.isupper():
            tiene_mayuscula = True
        elif char.isdigit():
            tiene_numero = True
        
        if tiene_mayuscula and tiene_numero:
            break
    
    return len(contrasena) >= 8 and tiene_mayuscula and tiene_numero


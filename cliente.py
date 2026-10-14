import requests

URL = "http://localhost:5000"
sesion = requests.Session()  
LINEA = "-" * 45


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 45)
    print("        SISTEMA DE GESTIÓN DE TAREAS")
    print("=" * 45)
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Ver tareas")
    print("4. Salir")
    print("=" * 45)


def mostrar_mensaje(mensaje, exito=True):
    etiqueta = "[OK]" if exito else "[ERROR]"
    print("\n" + LINEA)
    print(f"{etiqueta} {mensaje}")
    print(LINEA)


def pedir_credenciales(titulo):
    print(f"\n--- {titulo} ---")
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    return {"usuario": usuario, "contraseña": contrasena}


def mostrar_respuesta_json(respuesta):
    datos = respuesta.json()
    mostrar_mensaje(datos["message"], datos["status"] == "success")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                respuesta = sesion.post(URL + "/registro", json=pedir_credenciales("Registro"))
                mostrar_respuesta_json(respuesta)

            elif opcion == "2":
                respuesta = sesion.post(URL + "/login", json=pedir_credenciales("Iniciar sesión"))
                mostrar_respuesta_json(respuesta)

            elif opcion == "3":
                respuesta = sesion.get(URL + "/tareas")
                if respuesta.status_code == 200:
                    mostrar_mensaje("Acceso concedido. Respuesta del servidor (HTML):")
                    print(respuesta.text)
                    print(LINEA)
                else:
                    mostrar_respuesta_json(respuesta)

            elif opcion == "4":
                print("\n¡Hasta luego!\n")
                break

            else:
                mostrar_mensaje("Opción no válida. Elegí un número del 1 al 4.", False)

        except requests.exceptions.ConnectionError:
            mostrar_mensaje("No se pudo conectar al servidor. ¿Está corriendo servidor.py?", False)


if __name__ == "__main__":
    main()
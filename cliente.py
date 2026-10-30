import socket
import json
import webbrowser
import os

HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea(accion, usuario, contraseña):
    datos = {
        "accion": accion,
        "usuario": usuario,
        "contraseña": contraseña
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(datos).encode('utf-8'))
            
            data = s.recv(2048)
            respuesta = json.loads(data.decode('utf-8'))
            
            status = respuesta.get("status")
            print(f"\n[Status {status}] {respuesta}")
    except ConnectionRefusedError:
        print("\nError: No me pude conectar al servidor de sockets.")

while True:
    print("\n--- Menú Cliente Sockets ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Ver tareas (HTML)")
    print("4. Salir")
    opcion = input("Elegí una opción: ").strip()

    if opcion == "1":
        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()
        enviar_tarea("registro", usuario, contraseña)

    elif opcion == "2":
        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()
        enviar_tarea("login", usuario, contraseña)

    elif opcion == "3":
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(json.dumps({"accion": "ver_tareas"}).encode('utf-8'))
                data = s.recv(2048)
                respuesta = json.loads(data.decode('utf-8'))
                
                if respuesta.get("status") == 200:
                    html_content = respuesta.get("html")
                    ruta_archivo = os.path.abspath("temp_tareas.html")
                    
                    with open(ruta_archivo, "w", encoding="utf-8") as f:
                        f.write(html_content)
                        
                    print("\nAbriendo la respuesta del servidor en el navegador...")
                    webbrowser.open(f"file:///{ruta_archivo}")
        except ConnectionRefusedError:
            print("\nError: No me pude conectar al servidor de sockets.")

    elif opcion == "4":
        break
    else:
        print("Opción incorrecta.")
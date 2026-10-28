import socket
import concurrent.futures
import time

def procesar_tarea(conexion, direccion):
    print(f"Nueva conexión aceptada desde {direccion}")
    try:
        # Recibe la tarea del cliente
        datos = conexion.recv(1024).decode('utf-8')
        if datos:
            print(f"Worker procesando tarea: {datos}")
            time.sleep(2) # Simula el tiempo de procesamiento
            
            # Envía el resultado
            resultado = f"Tarea '{datos}' finalizada correctamente."
            conexion.sendall(resultado.encode('utf-8'))
    except Exception as e:
        print(f"Error en el procesamiento: {e}")
    finally:
        conexion.close()

def iniciar_servidor():
    host = '127.0.0.1'
    puerto = 65432
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()
    print(f"Servidor escuchando en {host}:{puerto}...")

    # Define el pool de hilos para los workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            conexion, direccion = servidor.accept()
            # Deriva la conexión al pool de hilos
            executor.submit(procesar_tarea, conexion, direccion)

if __name__ == '__main__':
    iniciar_servidor()
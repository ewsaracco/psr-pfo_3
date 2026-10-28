import socket

def enviar_tarea(tarea):
    host = '127.0.0.1'
    puerto = 65432

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, puerto))
        print(f"Enviando petición: {tarea}")
        cliente.sendall(tarea.encode('utf-8'))
        
        # Espera y recibe el resultado
        resultado = cliente.recv(1024).decode('utf-8')
        print(f"Respuesta del servidor: {resultado}")
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        cliente.close()

if __name__ == '__main__':
    enviar_tarea("Generar reporte de tráfico de red")
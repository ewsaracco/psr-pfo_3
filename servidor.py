import socket
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "tareas.db"
HOST = '127.0.0.1'
PORT = 65432

def init_db():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def procesar_tarea(datos):
    """Lógica de negocio ejecutada por los workers"""
    accion = datos.get("accion")
    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    try:
        if accion == "registro":
            if not usuario or not contraseña:
                return {"status": 400, "error": "Faltan datos"}
            password_hasheada = generate_password_hash(contraseña)
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (usuario, password_hasheada))
            conexion.commit()
            return {"status": 201, "mensaje": "Usuario registrado exitosamente"}

        elif accion == "login":
            if not usuario or not contraseña:
                return {"status": 400, "error": "Faltan datos"}
            cursor.execute("SELECT password FROM usuarios WHERE usuario = ?", (usuario,))
            resultado = cursor.fetchone()
            if resultado and check_password_hash(resultado[0], contraseña):
                return {"status": 200, "mensaje": "Inicio de sesión exitoso"}
            else:
                return {"status": 401, "error": "Credenciales inválidas"}
                
        elif accion == "ver_tareas":
            html = "<h1>Bienvenido al sistema de Gestión de Tareas</h1><p>Sistema Distribuido por Sockets funcionando correctamente.</p>"
            return {"status": 200, "html": html}
            
        else:
            return {"status": 400, "error": "Acción no reconocida"}
            
    except sqlite3.IntegrityError:
        return {"status": 409, "error": "El usuario ya existe"}
    finally:
        conexion.close()

def worker_cliente(conn, addr):
    """Función que ejecuta cada worker en el ThreadPool"""
    print(f"[WORKER] Atendiendo conexión de {addr}")
    try:
        data = conn.recv(2048)
        if data:
            datos_json = json.loads(data.decode('utf-8'))
            resultado = procesar_tarea(datos_json)
            conn.sendall(json.dumps(resultado).encode('utf-8'))
    except Exception as e:
        print(f"[WORKER ERROR] {e}")
    finally:
        conn.close()

def iniciar_servidor():
    init_db()
    with ThreadPoolExecutor(max_workers=5) as executor:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Servidor distribuido escuchando en {HOST}:{PORT}")
            
            while True:
                conn, addr = s.accept()
                executor.submit(worker_cliente, conn, addr)

if __name__ == '__main__':
    iniciar_servidor()
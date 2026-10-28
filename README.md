# PFO 3: Sistema Distribuido (Cliente-Servidor)

## Descripción
Este repositorio contiene la resolución de la Práctica Final Obligatoria (PFO) 3.

El proyecto cubre:
1. El diseño teórico de la arquitectura completa (balanceador, workers, colas de mensajes y almacenamiento).
2. La implementación en Python de un prototipo funcional de comunicación concurrente.

## Estructura del Proyecto
* **servidor.py**: Servidor principal que utiliza la librería `socket` y un `ThreadPoolExecutor`. Recibe las peticiones y las deriva a un pool de hilos, simulando el comportamiento de múltiples servidores workers operando en paralelo.
* **cliente.py**: Nodo emisor que se conecta al servidor por TCP, envía la carga útil de la tarea y espera la confirmación de procesamiento.

> **Nota sobre el Diagrama:** El diseño arquitectónico completo (que modela la integración de Nginx, RabbitMQ, PostgreSQL y S3) se entrega como un archivo de imagen adjunto por fuera de este documento, cumpliendo con la separación de entregables solicitada en la consigna.

## Requisitos de Ejecución
* Python 3.x
* No se requieren librerías externas (se utiliza únicamente la librería estándar de Python).

## Instrucciones de Uso

1. Abrir una terminal en el directorio raíz del proyecto e iniciar el servidor ejecutando:
   `python servidor.py`
   *(El servidor quedará a la escucha en el puerto local 65432).*

2. Abrir una nueva terminal (manteniendo el servidor en ejecución) y lanzar el cliente con:
   `python cliente.py`

3. Para comprobar la concurrencia y el funcionamiento del pool de hilos, se pueden abrir múltiples terminales adicionales y ejecutar `cliente.py` de forma casi simultánea.
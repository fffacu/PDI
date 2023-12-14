# Python chat grupal con sockets
import socket
import select
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Ingresar el ip del wifi
IP_address = "10.0.4.232"

# Puerto de conexion del socket para los clientes
Port = 9099
 
#Hace bind a la ip y el puerto, el cliente debe de conectarse al mismo IP y puerto 
server.bind(("0.0.0.0", Port))

#escucha para 100 conexiones activas.
server.listen(100) 

list_of_clients = []

def clientthread(conn, addr):
    conn.send(b"Ingresa tu nombre: ")  # Solicita al cliente que ingrese su nombre
    nombre = conn.recv(2048).decode("utf-8")  # Recibe el nombre del cliente
    welcome_message = f"Bienvenido {nombre}!"  # Mensaje de bienvenida personalizado
    conn.send(bytes(welcome_message, "utf-8"))

    while True:
        try:
            message = conn.recv(2048)
            if message:
                sys.stdout.write("<" + nombre + "> " + message.decode("utf-8"))  # Usa stdout para evitar saltos de línea
                sys.stdout.flush()  # Limpia el buffer de salida

                # Llamada de broadcast para la función enviar mensaje a todos
                message_to_send = "<" + nombre + "> " + message.decode("utf-8")
                broadcast(message_to_send, conn)
            else:
                remove(conn)
                break

        except:
            continue

#Usando la siguiente funcion transmitimos el mensaje a todos clientes
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(bytes(message, "utf-8"))  
            except:
                clients.close()
                # Si la conexión se pierde, se remueve el cliente
                remove(clients)


#La siguiente funcion simplemente elimina el objeto de la lista que se creó al principio del programa

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)

    # Imprime la dirección IP de los clientes conectados
    sys.stdout.write(addr[0] + " connected")
    sys.stdout.flush()

    threading.Thread(target=clientthread, args=(conn, addr)).start()

server.close()

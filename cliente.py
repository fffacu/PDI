from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import messagebox
import configparser

def receive():
    while True:
        try:
            mensaje = client_socket.recv(BUFSIZ).decode("utf8")
            mensaje_list.insert(tkinter.END, mensaje)
        except OSError:
            break

def send(event=None):
    mensaje = mi_ms.get()
    mi_ms.set("")
    client_socket.send(bytes(mensaje, "utf8"))
    mensaje_list.insert(tkinter.END, mensaje)

def show_help():
    help_text = (
        "Bienvenido a la aplicación.\n"
        "Para usar la aplicación, sigue estos pasos:\n"
        "1. Ingresa el mensaje en la parte inferior.\n"
        "2. Presiona el botón 'ENVIAR' o presiona Enter para enviar el mensaje.\n"
        "3. Los mensajes recibidos se mostrarán en la lista superior.\n\n"
        "Nota: Asegúrate de encender el servidor antes de comenzar a chatear."
    )
    messagebox.showinfo("Ayuda", help_text)

# Configuración por defecto
IP_server = "10.0.4.232"  # Establecer la dirección IP fija
Puerto = 9099
BUFSIZ = 1024
Ventana_ancho = 800
Ventana_alto = 600
Chat_ancho = 50
Chat_alto = 25

top = tkinter.Tk()
top.title("UDL QRO GRUPO 7001")
top.geometry(f"{Ventana_ancho}x{Ventana_alto}")

messages_frame = tkinter.Frame(top)
mi_ms = tkinter.StringVar()
mi_ms.set("")
scrollbar = tkinter.Scrollbar(messages_frame)

mensaje_list = tkinter.Listbox(messages_frame, height=Chat_alto, width=Chat_ancho, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
mensaje_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mensaje_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=mi_ms)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="ENVIAR", command=send)
send_button.pack()

help_button = tkinter.Button(top, text="Ayuda", command=show_help)
help_button.pack()

ADDR = (IP_server, Puerto)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

top.mainloop()

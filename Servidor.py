from cryptography.fernet import Fernet
import socket #Se importa la lbreria para usar Socket
import threading #Se importa la lbreria para usar hilos Socket

HEADER = 64 # Se define los numeros de bits que se recibiran
PORT = 5505 #El puerto por el cual se comunicaran
SERVER = '192.168.0.18' #La IP del servidor, que sera la de la raspberry
ADDR = (SERVER, PORT) #Se crea una tupla, para definir la direccion
FORMAT = 'utf-8' #El formato de los mensajes
DISCONNECT_MESSAGE = "!DISCONNECT" #El mensaje que permitira desconectar y acabar la sesion
#####
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se crea el socket, donde AF_INET hace referencia al tipo de direccion
                                                        #y SOCK_STREAM hace referencia a que necesitamos el socket para realizar stream
server.bind(ADDR) #Se vinculan la direccion y el puerto al cual se estara realizando la comunicacio

def handle_client(conn, addr): #Se define para establecer la comunicacion de mensajes con el cliente
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected: #Mientras connected exista
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:# Si existe mensaje, se decodifica
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            f=Fernet(msg)
            msg=f.decrypt(msg)

            if msg == DISCONNECT_MESSAGE: #Si el mensaje es el de desconexion, se acaba la sesion y se desconecta
                connected = False

            
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT)) #Se envia un mensaje de confirmacion al cliente de que se recibio el mensaje

    conn.close()


def start(): #Se define para iniciar la sesion con el cliente
    server.listen() #Se coloca al servidor en modo LISTEN para escuchar al cliente
    print(f"[LISTENING] Server is listening on address {ADDR}")
    while True:
        conn, addr = server.accept()#espera una conexion en la direccion y la acepta
        #Se declara un hilo cada vez que existe una conexion
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #Se imprime cuantas veces exite una conexion
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()




cursor.commit()

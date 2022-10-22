import socket #Se importa la lbreria para usar Socket
from getmac import get_mac_address as gma #Se importa la libreria para extraer la MAC ADDRESS

vocals=['A','E','I','O','U'] #Se crea un array con las vocales que seran enviadas al servidor
number=[1,2,3,4,5,6,7,8,9,10] #Se crea un array con los numero que seran enviadas al servidor
HEADER = 64 # Se define los numeros de bits que se recibiran
PORT = 5505 #El puerto por el cual se comunicaran
FORMAT = 'utf-8' #El formato de los mensajes
DISCONNECT_MESSAGE = "!DISCONNECT" #El mensaje que permitira desconectar y acabar la sesion
SERVER = '192.168.0.18' #La IP del servidor, que sera la de la raspberry
ADDR = (SERVER, PORT) #Se crea una tupla, para definir la direccion

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Se crea el socket, donde AF_INET hace referencia al tipo de direccion
                                                        #y SOCK_STREAM hace referencia a que necesitamos el socket para realizar stream
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) #Se codifica el mensaje en el Formato definido
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)#se codifica el largo del mensaje
    send_length += b' ' * (HEADER - len(send_length))# Se le da el largo al mensaje al largo definido. Ademas b'' hace referencia a la representacion en byte
    client.send(send_length) #Se envia el largo
    client.send(message) #Se envia el mensaje
    print(client.recv(2048).decode(FORMAT))

send("Hola Servidor") #Se utiliza la funcion send para enviar el mensaje
send("Esta es mi MAC ADDRESS") #Se utiliza la funcion send para enviar el mensaje
send(gma()) #Se envia la MAC ADDRESS

send("Estas son las Vocales") #Se utiliza la funcion send para enviar el mensaje
for i in vocals: #Se recorre el array vocals
    send(i) #Se utiliza la funcion send para enviar el mensaje
send ("Estos son los numeros del 1 al 10")#Se utiliza la funcion send para enviar el mensaje
for j in number: #Se recorre el array number
    send(str(j)) #Se utiliza la funcion send para enviar el mensaje tranformando los numeros a string con str

send(DISCONNECT_MESSAGE) #Se envia el mensaje de desconexion

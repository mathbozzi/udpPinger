import sys
from socket import *
from time import time, ctime
from array import *
from statistics import *

N = 10   # numero de mensagens a serem enviadas
dataRtt = [] # vetor com os dados de rtt que chegaram
lostRtt = [] # vetor com os dados de rtt que foram perdidos

if (len(sys.argv) != 3):
    print("Digite: UDPPingClient.py <server_host> <server_port>")
    sys.exit()

# usuario digita o nome ate 30 caracteres
name = ''.rjust(31, '#')
while len(name) >= 30:
    name = input('Digite seu nome(ate 30 caracteres): \n')

# pegando os dados do argv com o IP e porta do servidor
serverHost, serverPort = sys.argv[1:]
clientSocket = socket(AF_INET, SOCK_DGRAM)  # Inicialização do socket
clientSocket.settimeout(1)  # definindo tempo de excessao

# definindo o laço de quantas mensagens serão enviadas pelo cliente
for i in range(N):
    initTime = time()  # define tempo de inicio
    message = str(i+1).zfill(5) + "0" + \
        str(initTime)[11:15] + name.rjust(30, '#') # mensagem segundo o protocolo especificado

    try:
        clientSocket.sendto(message.encode('utf-8'),
                            (serverHost, int(serverPort)))  # enviando a msg para o servidor
        msgRetornada, serverAddress = clientSocket.recvfrom(1024) # esperando a resposta

        endTime = time() # tempo da mensagem retornada (se o servidor respondeu)
        rtt = ((endTime - initTime)*1000) # rtt
        if rtt > 1:
            print("Pacote perdido\n")   # pacote perdido
            lostRtt.append(rtt)        # vetor do tempo das mensagens atrasadas
        else:
            msgretornada = msgRetornada.decode()  # mensagem retornada decodificada
            print(msgretornada) 
            print("RTT: %.3f ms\n" % rtt) 
            dataRtt.append(rtt)            # vetor com tempo das mensagens que chegaram a tempo

    except timeout:
        print("%i Pacote perdido\n" % (i+1))   # pacote perdido 

clientSocket.close() 

# abaixo é feito a formatação da saída, com os calculos adequados
if(len(dataRtt) > 0):
    print(N, ' packets transmitted,', len(dataRtt), 'received, ',
          (100 - ((len(dataRtt)/N)*100)), '% packet loss, time ', sum(dataRtt)+sum(lostRtt))
    print('Rtt min ', min(dataRtt))  # minimo rtt
    print('Avg ', sum(dataRtt)/len(dataRtt))  # media
    print('Rtt max ', max(dataRtt))  # maximo rtt
    print('Mdev ', stdev(dataRtt))  # desvio padrao
else:
    print('100% packet loss')

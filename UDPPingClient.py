import sys
from socket import *
from time import time, ctime
from array import *
from statistics import *

N = 10
dataRtt = []
lostRtt = []

if (len(sys.argv) != 3):
    print("Digite: UDPPingClient.py <server_host> <server_port>")
    sys.exit()

name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
while len(name) >= 30:
    name = input('Digite seu nome(ate 30 caracteres): \n')

# Preparing the socket
serverHost, serverPort = sys.argv[1:]
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(N):
    startTime = time()
    message = str(i+1) + " 0" + " tmtm " + name

    try:
        # Sending the message and waiting for the answer
        clientSocket.sendto(message.encode('utf-8'),
                            (serverHost, int(serverPort)))
        msgRetornada, serverAddress = clientSocket.recvfrom(1024)

        # Checking the current time and if the server answered
        endTime = time()
        rtt = ((endTime - startTime)*1000)
        if rtt > 1:
            print("Pacote perdido\n")
            lostRtt.append(rtt)
        else:
            msgretornada = msgRetornada.decode()
            print(msgretornada)
            print("RTT: %.3f ms\n" % rtt)
            dataRtt.append(rtt)

    except timeout:
        print("Pacote perdido\n")

clientSocket.close()

if(len(dataRtt) > 0):
    print(N, ' packets transmitted,', len(dataRtt), 'received, ',
          (100 - ((len(dataRtt)/N)*100)), '% packet loss, time ', sum(dataRtt)+sum(lostRtt))
    print('rtt min ', min(dataRtt))  # minimo rtt
    print('avg ', sum(dataRtt)/len(dataRtt))  # media
    print('rtt max ', max(dataRtt))  # maximo rtt
    print('mdev ', pstdev(dataRtt))  # desvio populacional
    # print('mdev ',stdev(dataRtt))
else:
    print('100% packet loss')

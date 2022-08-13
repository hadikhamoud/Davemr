import socket
 
HOST = "localhost"
PORT = int(input("enter port number: "))
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def JavaToDict(data):

    dat = data.replace('\n','|')
    dat = dat.split('|')
    dic = {}
    for i in range(0,len(dat)-2,2):
        dic[dat[i]] = float(dat[i+1])/10000
    return dic


# sock.sendall(b"Hello\n")
# data = sock.recv(1024)
# print ("1)", data)
run = True
while run:
    n = input('what do you want to send: ')
    n+='\n'
    bn = bytes(n,'utf-8')
    sock.sendall(bn)
    data = sock.recv(1024)
    dic = JavaToDict(data.decode('utf-8'))
    print(dic)
    if n =='end\n':
        sock.close()
    data =b''
    # dic = {}

 












# # if ( data == "olleH\n" ):
# #     sock.sendall(b"Bye\n")
# #     data = sock.recv(1024)
# #     print("2)", data)
 
# #     if (data == "eyB}\n"):
# #         sock.close()
# #         print("Socket closed")

















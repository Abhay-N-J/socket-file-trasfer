import socket
import ssl
import os
import sys

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

dir_path = "./SERVER/" 

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server Started at ', HOST)
    with context.wrap_socket(s, server_side=True) as ssl_socket:
        while True:
            try:
                conn, (ip, port) = ssl_socket.accept()
                with conn:
                    conn.settimeout(10)
                    print("Connected by", ip, " ", port)
                    data = conn.recv(1024)
                    if data.decode() == 'SYN':
                        conn.send(b'ACK')
                    elif data.decode() == 'Dir':
                        data = conn.recv(1024).decode()
                        if data != 'False':     
                            dir_path =  "./SERVER/" + data
                        else:
                            dir_path = "./SERVER/"
                        if len(dir_path) > 9 and dir_path[9] == '/':
                            dir_path = dir_path[:9] + dir_path[10:]
                        if(dir_path[-1] != '/'):
                            dir_path += '/'
                        # print("dir path ", dir_path)
                        if os.path.exists(dir_path):
                            dirs = os.listdir(dir_path)
                            conn.sendall(",".join(dirs).encode())
                        else:
                            os.makedirs(dir_path)
                            dirs = f'Made a directory with path => {dir_path}'
                            conn.sendall(dirs.encode())
                        # print(dirs)
                        print('Path = ', dir_path)
                    
                    elif data.decode() == 'Send' or data.decode() == 'Take':
                        flag = data.decode()
                        data = conn.recv(1024).decode()   
                        if data != 'False':     
                            dir_path =  "./SERVER/" + data  
                        else:
                            dir_path = "./SERVER/"
                        if len(dir_path) > 9 and dir_path[9] == '/':
                            dir_path = dir_path[:9] + dir_path[10:]
                        if(dir_path[-1] != '/'):
                            dir_path += '/'
                        if os.path.exists(dir_path):
                            conn.sendall(b'True')
                            print('Path = ', dir_path)
                            # conn.sendall("".join(dirs).encode())
                            filename = conn.recv(1024).decode()
                            print('File =', filename)
                             
                            if flag == 'Take':
                                with open(dir_path + filename, 'wb') as f:
                                    while True:
                                        data = conn.recv(1024)
                                        if(data == b'DONE'):
                                            break
                                        f.write(data)
                                print("Recieved")
                                conn.sendall(b'File sent successfully')
                            
                            elif flag == 'Send':
                                size = os.path.getsize(dir_path + filename)
                                conn.sendall(str(size).encode())
                                print(dir_path + filename)
                                with open(dir_path + filename, 'rb') as f:
                                    data = f.read(1024)
                                    while data:
                                        conn.sendall(data)
                                        data = f.read(1024)
                                conn.sendall(b'DONE')
                                print("Sent")
                            conn.sendall(b'File recieved successfully')
                        
                        else:
                            conn.sendall(b'False')            
                    
                    else:
                        conn.sendall(b'Not correct protocol')
                print('Connection Disconnected')        
                            
            except KeyboardInterrupt as k:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(k, exc_type, fname, exc_tb.tb_lineno)
                ssl_socket.close()
                s.close()
                print('Closed.. Disconnected') 
                break
            
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(e, exc_type, fname, exc_tb.tb_lineno)
                print('Error.. Disconnected') 
    



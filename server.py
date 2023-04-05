import socket
import ssl
import os

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
<<<<<<< HEAD

dir_path = "./SERVER/" 
=======
>>>>>>> b37b4ab (First Commit)

dir_path = "./SERVER/" 

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
    s.bind((HOST, PORT))
    s.listen()
    with context.wrap_socket(s, server_side=True) as ssl_socket:
        try:
            while True:
                conn, addr = ssl_socket.accept()
                with conn:
                    print("Connected by", addr)
                    data = conn.recv(1024)
                    
                    if data.decode() == 'Dir':
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
                            dirs = os.listdir(dir_path)
                            conn.sendall(",".join(dirs).encode())
                        else:
                            dirs = f'Made a directory with path => {dir_path}'
                            conn.sendall(dirs.encode())
                            os.mkdir(dir_path)
                        print(dirs)
                        # print(",".join(dirs).encode())
                        print(dir_path)
                            # print("OVER")
                    
<<<<<<< HEAD
                    elif data.decode() == 'Send' or data.decode() == 'Take':
=======
                   
                    else:
>>>>>>> b37b4ab (First Commit)
                        flag = data.decode()
                        data = conn.recv(1024).decode()   
                        if data != 'False':     
                            dir_path =  "./SERVER/" + data  
                        if len(dir_path) > 9 and dir_path[9] == '/':
                            dir_path = dir_path[:9] + dir_path[10:]
                        if(dir_path[-1] != '/'):
                            dir_path += '/'
                        if os.path.exists(dir_path):
                            conn.sendall(b'True')
                            print(dir_path)
                            # conn.sendall("".join(dirs).encode())
                            filename = conn.recv(1024).decode()
                            print(filename)
<<<<<<< HEAD
                             
                            if flag == 'Take':
                                size = int(conn.recv(1024).decode()) // 1024
                                print(size)
                                count = size // 100
                                with open(dir_path + filename, 'wb') as f:
                                    while True:
                                        data = conn.recv(1024)
                                        if(data == b'DONE'):
                                            break
                                        f.write(data)
                                        if size % count == 0:                                        
                                            print('#',end="") 
                                        size -= 1
                                print("END")
                                conn.sendall(b'File sent successfully')
=======
                            if flag == 'Take':
                                with open(dir_path + filename, 'wb') as f:
                                    while True:
                                        data = conn.recv(1024)
                                        if(data.decode() == 'DONE'):
                                            break
                                        f.write(data)
                                        conn.sendall(b'File sent successfully')
>>>>>>> b37b4ab (First Commit)
                            
                            elif flag == 'Send':
                                print(dir_path + filename)
                                with open(dir_path + filename, 'rb') as f:
                                    data = f.read(1024)
<<<<<<< HEAD
                                    # if size % count == 0:                                        
                                    #     print('#',end="") 
                                    #     size -= 1
                                    
=======
>>>>>>> b37b4ab (First Commit)
                                    while data:
                                        conn.sendall(data)
                                        data = f.read(1024)
                                conn.sendall(b'DONE')
                            conn.sendall(b'File recieved successfully')
                        
                        else:
                            conn.sendall(b'False')            
<<<<<<< HEAD
                    
                    else:
                        conn.sendall(b'Not correct protocol')
=======
                        
>>>>>>> b37b4ab (First Commit)
                        
                        
        except Exception as e:
            print(e)
            conn.close()
            ssl_socket.close()
            s.close()



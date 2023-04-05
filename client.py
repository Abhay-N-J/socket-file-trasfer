
import socket
import ssl
import os
from tkinter import *
from tkinter import filedialog

<<<<<<< HEAD

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432       # The port used by the server

=======
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432       # The port used by the server

>>>>>>> b37b4ab (First Commit)
client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client_context.check_hostname = False
client_context.load_verify_locations(cafile="server.crt")


def select_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, END)
    file_entry.insert(0, file_path)

def select_dir():
    dir_path = dir_input.get()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
            with client_context.wrap_socket(s, server_hostname=HOST) as ssl_socket:
                ssl_socket.connect((HOST, PORT))
                ssl_socket.send(b'Dir')
                if dir_path == '':
                    ssl_socket.send(b'False')
                else:
                    ssl_socket.send(dir_path.encode())
                dirs = ssl_socket.recv(1024).decode()
                if len(dirs) == 0:
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, "Empty Directory")
                elif dirs[0] != 'M':
                    dirs = dirs.split(",")
                    print(dirs)
                    dir_text.delete(1.0, END)
                    for i in dirs:
                        dir_text.insert(1.0, i + '\n')
                else:
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, dirs)
                    

def upload():
    filename = file_entry.get()
<<<<<<< HEAD
    size = os.path.getsize(filename)
=======
>>>>>>> b37b4ab (First Commit)
    filename_1 = ""
    for i in filename[::-1]:
        if i == '/':
            break
        filename_1 += i
    filename_1 = filename_1[::-1]
    
    dir_path = dir_input.get()
    # if dir_path == '':
    #     dir_text.delete(1.0,END)
    #     dir_text.insert(1.0, 'Enter something')
        
    # else:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
            with client_context.wrap_socket(s, server_hostname=HOST) as ssl_socket:
                ssl_socket.connect((HOST, PORT))
                ssl_socket.sendall(b'Take')
                if dir_path == '':
                    ssl_socket.sendall(b'False')
                else:
                    ssl_socket.sendall(dir_path.encode())
                    
                flag = ssl_socket.recv(1024).decode()
                if bool(flag):
                    ssl_socket.sendall(filename_1.encode())
<<<<<<< HEAD
                    ssl_socket.sendall(str(size).encode())
=======
>>>>>>> b37b4ab (First Commit)
                    with open(filename, 'rb') as f:
                        data = f.read(1024)
                        while data:
                            ssl_socket.sendall(data)
                            data = f.read(1024)
                    ssl_socket.sendall(b'DONE')
                    # print(ssl_socket.recv(1024).decode())
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, ssl_socket.recv(1024).decode())
                else:
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, f'File path => {dir_path} is wrong')
    except Exception as e:
        print(e)


def download():
    filename = file_entry.get()
<<<<<<< HEAD
    # size = os.path.getsize(filename)
=======
>>>>>>> b37b4ab (First Commit)
    filename_1 = ""
    for i in filename[::-1]:
        if i == '/':
            break
        filename_1 += i
    filename = filename_1[::-1]
    
    dir_path = dir_input.get()
    # if dir_path == '':
    #     dir_text.delete(1.0,END)
    #     dir_text.insert(1.0, 'Enter something')
    # else:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
            with client_context.wrap_socket(s, server_hostname=HOST) as ssl_socket:
                ssl_socket.connect((HOST, PORT))
                ssl_socket.sendall(b'Send')
                if dir_path == '':
                    ssl_socket.sendall(b'False')
                else:
                    ssl_socket.sendall(dir_path.encode())
                flag = ssl_socket.recv(1024).decode()
                if bool(flag):
                    print(filename)
                    ssl_socket.sendall(filename.encode())
<<<<<<< HEAD
                    # ssl_socket.sendall(str(size).encode())
=======
>>>>>>> b37b4ab (First Commit)
                    if not os.path.exists('./Downloads'):
                        os.mkdir('./Downloads')
                    with open('./Downloads/' + filename, 'wb') as f:
                        data = ssl_socket.recv(1024)
                        while data:
                            if data == b'DONE':
                                break
                            f.write(data)
                            data = ssl_socket.recv(1024)
                    # ssl_socket.sendall(b'Recieved')
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, ssl_socket.recv(1024).decode())
                else:
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, f'File path => {dir_path} is wrong')
                    
    except Exception as e:
        print(e)


root = Tk()
root.title('Secure File Transfer Application')

file_label = Label(root, text='File:')
file_label.grid(row=0, column=0)

file_entry = Entry(root)
file_entry.grid(row=0, column=1)

file_button = Button(root, text='Select file', command=select_file)
file_button.grid(row=0, column=2)

dir_label = Label(root, text='Enter the path')
dir_label.grid(row=1, column=0)

dir_input = Entry(root)
dir_input.grid(row=1, column=1)

dir_button = Button(root, text='Search/Enter', command=select_dir)
dir_button.grid(row=1, column=2)

dir_text = Text(root, height=10, width=22)
dir_text.grid(row=2, column=1)

upload_button = Button(root, text='Upload', command=upload)
upload_button.grid(row=3, column=0)

download_button = Button(root, text='Download', command=download)
download_button.grid(row=3, column=2)


root.mainloop()

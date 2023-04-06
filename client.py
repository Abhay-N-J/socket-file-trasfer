import socket
import ssl
import os
import sys
from tkinter import *
import time
from tkinter import filedialog


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432       # The port used by the server

client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client_context.check_hostname = False
client_context.load_verify_locations(cafile="server.crt")

socket.setdefaulttimeout(10)

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
    size = os.path.getsize(filename)
    filename_1 = ""
    for i in filename[::-1]:
        if i == '/':
            break
        filename_1 += i
    filename_1 = filename_1[::-1]
    
    dir_path = dir_input.get()
    
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
                    bar_length = 100
                    step_size = max(size // 100, 1)
                    progress = 0
                    i = 0
                    with open(filename, 'rb') as f:
                        data = f.read(1024)
                        while data:
                            ssl_socket.sendall(data)
                            if i % step_size == 0:
                                progress += 1
                                percent = progress / 100
                                hashes = '#' * int(percent * bar_length)
                                spaces = ' ' * (bar_length - len(hashes))
                                string = "Loading: [{}] {} ".format(hashes + spaces, str(int(percent * 100)))
                                dir_text.delete(1.0, END)
                                dir_text.insert(1.0, string)
                            i += 1
                            data = f.read(1024)
                    ssl_socket.sendall(b'DONE')
                    dir_text.insert(END, ssl_socket.recv(1024).decode())
                else:
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, f'File path => {dir_path} is wrong')
                    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)


def download():
    filename = file_entry.get()
    filename_1 = ""
    for i in filename[::-1]:
        if i == '/':
            break
        filename_1 += i
    filename = filename_1[::-1]
    
    dir_path = dir_input.get() 
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
                    size = int(ssl_socket.recv().decode())
                    bar_length = 100
                    step_size = max(size // 100, 1)
                    progress = 0
                    i = 0
                    if not os.path.exists('./Downloads'):
                        os.mkdir('./Downloads')
                    with open('./Downloads/' + filename, 'wb') as f:
                        data = ssl_socket.recv(1024)
                        while data:
                            if data == b'DONE':
                                break
                            f.write(data)
                            if i % step_size == 0:
                                progress += 1
                                percent = progress / 100
                                hashes = '#' * int(percent * bar_length)
                                spaces = ' ' * (bar_length - len(hashes))
                                string = "Loading: [{}] {}\n".format(hashes + spaces, str(int(percent * 100)))
                                dir_text.delete(1.0, END)
                                dir_text.insert(1.0, string)
                            i += 1
                            data = ssl_socket.recv(1024)
                    dir_text.insert(END, ssl_socket.recv(1024).decode())
                else:
                    dir_text.delete(1.0, END)
                    dir_text.insert(1.0, f'File path => {dir_path} is wrong')
                    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)

def ip():
    
    def exit_func():
        
        try:    
            HOST = ip_entry.get()
            PORT = int(port_entry.get())
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
                with client_context.wrap_socket(s, server_hostname=HOST) as ssl_socket:
                        ssl_socket.connect((HOST, PORT))
                        ssl_socket.send(b"SYN")
                        ssl_socket.settimeout(10)
                        if ssl_socket.recv() == b'ACK':
                            second_window.destroy()
                            root.deiconify()
                        else:
                            text.grid(row=2,column=0, columnspan=2)
                            text.delete(1.0, END)
                            text.insert(1.0, "IP or PORT wrong\n" + e)
                            
        except Exception as e:
                print(e)
                text.grid(row=2,column=0, columnspan=2)
                text.delete(1.0, END)
                text.insert(1.0, "IP or PORT wrong\n" + str(e))
                    
    root.withdraw()
    
    second_window = Toplevel()
    second_window.protocol("WM_DELETE_WINDOW",lambda: root.destroy())
    
    ip_label = Label(second_window, text="Enter the IP address of the server")
    ip_label.grid(row=0, column=0)
    
    ip_entry = Entry(second_window)
    ip_entry.grid(row=0, column=1)
    
    port_label = Label(second_window, text='Enter the PORT of the server')
    port_label.grid(row=1, column=0)
    
    port_entry = Entry(second_window)
    port_entry.grid(row=1, column=1)
    
    text = Text(second_window, height=5, width=44)
    text.grid(row=2, column=0, columnspan=2)
    text.grid_forget()
    
    enter_button = Button(second_window, text='Enter', command=exit_func)
    enter_button.grid(row=3, column=0)
    


root = Tk()
root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

root.title('Secure File Transfer Application')

file_label = Label(root, text='File:')
file_label.grid(row=0, column=0)

file_entry = Entry(root, width=44)
file_entry.grid(row=0, column=1)

file_button = Button(root, text='Select file', command=select_file)
file_button.grid(row=0, column=2)

dir_label = Label(root, text='Enter the path')
dir_label.grid(row=1, column=0)

dir_input = Entry(root, width=44)
dir_input.grid(row=1, column=1)

dir_button = Button(root, text='Search/Enter', command=select_dir)
dir_button.grid(row=1, column=2)

dir_text = Text(root, width=66, height=20)
dir_text.grid(row=2, column=0, columnspan=3)

upload_button = Button(root, text='Upload', command=upload)
upload_button.grid(row=3, column=0)

download_button = Button(root, text='Download', command=download)
download_button.grid(row=3, column=2)

ip_button = Button(root, text='Go back', command=ip)
ip_button.grid(row=4, column=1)


ip()

root.mainloop()


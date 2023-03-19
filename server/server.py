import pyautogui
import socket
import asyncio
import PIL.Image, PIL.ImageFile, PIL.ImageTk
import os
import threading
from io import BytesIO
from win32api import GetSystemMetrics, NameDisplay

s = socket.socket()

print('  > Starting server')
#get screen res
res_x = int(GetSystemMetrics(0) / 2)
res_y = int(GetSystemMetrics(1) / 2)
print(f'  > Using display with resolution {GetSystemMetrics(0)} x {GetSystemMetrics(1)}, and streaming at {res_x} x {res_y}')
port = 22371
#bind to a port
s.bind(('', port))
print(f'  > Server running at {port}')
print('  > Listening for connection...')
#listen for a connection
s.listen(1)

c, addr = s.accept()
print(f'  > Got connection form {addr}')

#server class
class server:
    size = 102400
    #get pressed key
    def key_loop(self):
        while True:
            try:
                #send it 
                key = c.recv(512).decode()
                print(key)
                pyautogui.write(key)
            except Exception as e:
                pass

    #Follow @python.coders.hub for more
    """
    def buffer_loop(self):
        while True:
            try:
                size = os.stat('img.jpeg').st_size
                size_str = str(size)
                c.send(size_str.encode())
            except Exception as e:
                print(f"  > Couldn't send dynamic buffer, sending 102400 buffer! {e}")
                c.send(size)
    """

    def screen_loop(self):
        while True:
            try:
                #take screenshot
                frame = pyautogui.screenshot()
                frame = frame.resize((res_x, res_y))
                frame_ = BytesIO()
                frame.save(frame_, format="JPEG", optimize = True, quality = 25)
                frame = PIL.Image.open(frame_)

                #frame = open(frame_, 'rb')

                #encode frame
                frame_.seek(0)
                
                bytes = bytearray(frame_.read())

                c.send(bytes)
            except Exception as e:
                print(f"  > Something went wrong! {e}")

    def __init__(self):
        print("a")
        threading.Thread(target=self.key_loop).start()
        #threading.Thread(target=self.buffer_loop).start()
        threading.Thread(target=self.screen_loop).start()
    
#run server class
server()
input()

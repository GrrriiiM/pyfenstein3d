import os
import tkinter as tk
import time
import asyncio
from threading import Thread
from engine import Server
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.server = Server()
        
        self.player = self.server
        
        self.master = master
        #self.master.configure(bg="#004040")
        self.master.title("Pyfenstein3d")
        self.master.wm_geometry("640x480")
        self.master.configure(bg="#004040")
        self.canvas = tk.Canvas(self.master, bg="white", width=640, height=480)
        self.canvas.pack()
        self.image = Image.open(f"{os.path.dirname(__file__)}/imgs/walls.png")
        self.image1 = ImageTk.PhotoImage(self.image.resize((400, 400), Image.NEAREST, box=(0,0,64,64)))
        self.image2 = self.canvas.create_image(10, 10, anchor=tk.NW, image=self.image1)
        self.image3 = ImageTk.PhotoImage(self.image.resize((50, 50), Image.NEAREST, box=(65,65,128,128)))
        self.image4 = self.canvas.create_image(10, 10, anchor=tk.NW, image=self.image3)
        
        # asyncio.run(self.start_game())
        self.master.after(0, self.animation)

        # self.frame_count = 0;
        # loop = asyncio.new_event_loop()
        # t = Thread(target=self.start_background_loop, args=(loop,), daemon=True)
        # t.start()
        # asyncio.run_coroutine_threadsafe(self.frame(), loop)

        self.server.start_game();
        
        # self.__loop = asyncio.get_event_loop();
        # self.__loop.run_until_complete(self.frame())

        print("iniciou")
    
    def start_background_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def frame(self):
        while True:
            self.frame_count = self.frame_count + 1
            print(self.frame_count)
            await asyncio.sleep(1)

    def animation(self):
        track = 0
        while True:
            if track == 0:
               for i in range(0,51):
                    time.sleep(0.025)
                    self.canvas.move(self.image4, 1, 0)
                    self.canvas.update()
               track = 1

            else:
               for i in range(0,51):
                    time.sleep(0.025)
                    self.canvas.move(self.image4, -1, 0)
                    self.canvas.update()
               track = 0

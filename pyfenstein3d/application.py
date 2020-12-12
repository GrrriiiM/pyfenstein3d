import os
import tkinter as tk
import time
import asyncio
from threading import Thread
from engine import Server
from engine import FieldOfView
from engine.config import RAY_COUNT
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.server = Server()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "maps_pattern/map_1_level_1.txt"))
        self.server.load_map_file(file_path)
        
        
        
        self.master = master
        #self.master.configure(bg="#004040")
        self.master.title("Pyfenstein3d")
        self.master.wm_geometry("640x480")
        self.master.configure(bg="#004040")
        self.canvas = tk.Canvas(self.master, bg="white", width=640, height=480)
        self.canvas.pack()
        self.walls_image = Image.open(f"{os.path.dirname(__file__)}/imgs/walls.png")
        self.image1 = ImageTk.PhotoImage(self.walls_image.resize((400, 400), Image.NEAREST, box=(0,0,64,64)))
        # # self.image2 = 
        # self.canvas.create_image(10, 10, anchor=tk.NW, image=self.image1)
        # self.image3 = ImageTk.PhotoImage(self.image.resize((50, 50), Image.NEAREST, box=(65,65,128,128)))
        # # self.image4 = 
        # self.canvas.create_image(10, 10, anchor=tk.NW, image=self.image3)
        self.ray_images = [None for r in range(RAY_COUNT)]
        self.ray_canvas_photo = [self.canvas.create_image(r, 0, anchor=tk.NW) for r in range(RAY_COUNT)]
        
        # asyncio.run(self.start_game())

        # self.master.after(0, self.animation)
        self.__frame_count = 0
        self.__thread = Thread(target=self.animation)
        self.__is_running = True
        self.__thread.start()
        

        # self.frame_count = 0;
        # loop = asyncio.new_event_loop()
        # t = Thread(target=self.start_background_loop, args=(loop,), daemon=True)
        # t.start()
        # asyncio.run_coroutine_threadsafe(self.frame(), loop)

        # self.server.start_game();
        
        # self.__loop = asyncio.get_event_loop();
        # self.__loop.run_until_complete(self.frame())

        print("iniciou")
    
    def on_closing(self):
        self.server.stop_game()
        self.__is_running = False
        self.__thread.join()
        self.master.destroy()
        

    def animation(self):
        while self.__is_running:
            # state = self.server.get_state("123")
            # if state is not None:
                # fov = cast_fov(state["fov"])
            self.__frame_count = self.__frame_count + 1
            for i in range(RAY_COUNT):
                # ray = fov.rays[i]
                self.ray_images[i] = ImageTk.PhotoImage(self.walls_image.resize((1, 400), Image.NEAREST, box=(0,0,64+i/10,64)))
                self.canvas.itemconfig(self.ray_canvas_photo[i], image=self.ray_images[i])
            self.canvas.update()
            print(self.__frame_count)
            time.sleep(1/60)
                


def cast_fov(obj) -> FieldOfView:
    return obj


import os
from pyfenstein3d.engine import Server
from pyfenstein3d.game import Command
from pyfenstein3d.game import Screen
from pyfenstein3d.game import Game
from pyfenstein3d.game import Image
os.system("cls")
print("AJUSTE AS CONFIGURACOES")
print("FONTE: CONSOLAS 10px")
print("LARGURA: 200")
print("ALTURA: 62")
input()
command = Command()
image = Image()
screen = Screen(image)
server = Server()
game = Game(command, screen, server)
game.start()

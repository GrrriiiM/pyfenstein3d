import os
from game import Game
from engine import Server
from command import Command
from screen import Screen

if __name__ == "__main__":
    os.system("cls")
    print("AJUSTE AS CONFIGURACOES")
    print("FONTE: CONSOLAS 5px")
    print("LARGURA: 300")
    print("ALTURA: 50")
    input()
    command = Command()
    screen = Screen()
    server = Server()
    game = Game(command, screen, server)
    game.start()

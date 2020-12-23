if __name__ == "__main__":
    import os
    from .engine import Server
    from .game import Command
    from .game import Screen
    from .game import Game
    os.system("cls")
    print("AJUSTE AS CONFIGURACOES")
    print("FONTE: CONSOLAS 10px")
    print("LARGURA: 200")
    print("ALTURA: 50")
    input()
    command = Command()
    screen = Screen()
    server = Server()
    game = Game(command, screen, server)
    game.start()

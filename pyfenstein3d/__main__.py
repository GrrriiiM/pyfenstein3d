if __name__ == "__main__":
    import os
    from .engine import Server
    from .game import Command
    from .game import Screen
    from .game import Game
    from .game import Image
    os.system("cls")
    print("CONFIGURACOES")
    print("- FONTE: CONSOLAS 10px")
    print("- LARGURA: 200")
    print("- ALTURA: 62")
    print()
    print("COMANDOS")
    print("- Andar para frente: W")
    print("- Andar para trás: S")
    print("- Andar para esquerda: A")
    print("- Andar para direita: D")
    print("- Virar para esquerda: Seta esquerda")
    print("- Virar para direita: Seta direta")
    print("- Atirar: Seta cima")
    print("- Abrir porta: Espaço")
    print()
    print("Pressione qualquer tecla para começar")
    input()
    command = Command()
    image = Image()
    screen = Screen(image)
    server = Server()
    game = Game(command, screen, server)
    game.start()

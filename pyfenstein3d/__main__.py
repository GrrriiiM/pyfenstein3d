if __name__ == "__main__":
    from .engine import Server
    from .game import Command
    from .game import Screen
    from .game import Game
    from .game import Image
    command = Command()
    image = Image()
    screen = Screen(image)
    server = Server()
    game = Game(command, screen, server)
    game.start()

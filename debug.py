from pyfenstein3d.engine import Server
from pyfenstein3d.game import Command
from pyfenstein3d.game import Screen
from pyfenstein3d.game import Game
from pyfenstein3d.game import Image
command = Command()
image = Image()
screen = Screen(image)
server = Server()
game = Game(command, screen, server)
game.start()

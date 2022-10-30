import src.game
import src.argumentos
import sys

# Redireciona para src/game
if __name__ == "__main__":
    src.argumentos.DEBUG = 'debug' in sys.argv
    src.game.main()

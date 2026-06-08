# main.py
# Punto de entrada. Solo arranca el motor.

from game.engine import Engine


def main():
    engine = Engine()
    engine.run()


if __name__ == '__main__':
    main()
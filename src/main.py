import sys
import os

# Ensure 'src/' is on the import path so all packages resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

from core.engine import Engine


def main():
    engine = Engine()
    engine.run()


if __name__ == "__main__":
    main()

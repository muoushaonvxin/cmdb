import os, sys

current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.dirname(current_path))
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    client = main.main_command(sys.argv)

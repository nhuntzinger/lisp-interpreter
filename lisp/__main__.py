import sys
import pathlib

from . import interpreter


if __name__ == '__main__':
    sys.setrecursionlimit(10 ** 5)  # Increase the recursion limit

    debug = '--debug' in sys.argv or '-d' in sys.argv

    if '--help' in sys.argv or '-h' in sys.argv or len(sys.argv) == 1:
        print('Usage: python3 -m lisp <filepath> [--debug]')
    else:
        path = pathlib.Path(sys.argv[1])
        interpreter = interpreter.LispInterpreter(path=path, debug=debug)
        interpreter.run_program()

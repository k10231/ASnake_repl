import time
import curses
from ASnake import build, execPy
import subprocess

import io
from contextlib import redirect_stdout
import platform

compileDict={'CPython':'Python','PyPy':'PyPy3'}
import sys
if hasattr(sys, "pyston_version_info"):
    # ^ Pyston dev's suggested this: https://github.com/pyston/pyston/issues/39
    # What scaredy cats!!
    compileTo = 'Pyston'
else:
    compileTo=compileDict[platform.python_implementation()]
del sys

def buildCode(code):
    return build(code, comment=False, optimize=False, debug=False, compileTo=compileTo, pythonVersion=3.9, enforceTyping=True)
    #return execPy(asn, fancy=False, pep=False, run=True, execTime=False, headless=False)
    # return subprocess.run(["python3", "-c", asn], capture_output=True, text=True)

def main(stdscr):

    # stdscr.nodelay(10)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.echo()
    stdout = io.StringIO()

    code = ''
    stdscr.addstr(">>> ", curses.color_pair(1))

    while True:
        c = stdscr.getch()
        y, x = stdscr.getyx()

        if c == curses.KEY_LEFT:
            if not x < 5:
                stdscr.move(y, x-1) 
            
        elif c == curses.KEY_RIGHT:
            stdscr.move(y, x+1)

        elif c in {curses.KEY_BACKSPACE, 127}:
            if not x < 4:
                stdscr.delch(y, x)
                code = code[0:-2]
            else:
                stdscr.move(y, x + 1)
        elif c in {curses.KEY_ENTER, 10, 13}:
            if c <= y:
                stdscr.clear()
                stdscr.refresh()
            else:

                stdscr.move(y+1,0)
                with redirect_stdout(stdout):
                    exec(buildCode(code))
                output=stdout.getvalue()
                stdscr.addstr(output)
                stdout = io.StringIO()
                stdscr.move(y+1+output.count('\n'),0)
                stdscr.addstr(">>> ", curses.color_pair(1))
                code = ''
                stdscr.refresh()
        else:
            code += chr(c)


    stdscr.refresh()


curses.wrapper(main)

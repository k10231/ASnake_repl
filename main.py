import time
import curses
from ASnake import build, execPy, ASnakeVersion
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

ReplVersion='v0.2.0'

# for debugging only
def file_out(write_mode, *args):
    with open("streams.txt", write_mode ,encoding = 'utf-8') as f:
        f.write(f"{args}\n")


def buildCode(code):
    return build(code, comment=False, optimize=False, debug=False, compileTo=compileTo, pythonVersion=3.9, enforceTyping=True)
    #return execPy(asn, fancy=False, pep=False, run=True, execTime=False, headless=False)
    # return subprocess.run(["python3", "-c", asn], capture_output=True, text=True)

bash_history = []

def main(stdscr):

    # stdscr.nodelay(10)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.echo()
    stdout = io.StringIO()

    code = ''
    stdscr.addstr(f"ASnake {ASnakeVersion} \nRepl {ReplVersion}\n\n")
    stdscr.addstr(">>> ", curses.color_pair(1))

    while True:
        c = stdscr.getch()
        y, x = stdscr.getyx()
        height, width = stdscr.getmaxyx()

        if c == curses.KEY_LEFT:
            if not x < 5:
                stdscr.move(y, x-1) 
            
        elif c == curses.KEY_RIGHT:
            stdscr.move(y, x+1)

        # todo 
        elif c == curses.KEY_UP:
            pass 

        elif c in {curses.KEY_BACKSPACE, 127}:
            if not x < 4:
                stdscr.delch(y, x)
                code = code[0:-1]
                file_out("w", code)
            else:
                stdscr.move(y, x + 1)

        elif c in {curses.KEY_ENTER, 10, 13}:
            if y >= height-1:
                stdscr.clear()
                stdscr.refresh()
            else:
                stdscr.move(y+1,0)
                with redirect_stdout(stdout):
                    exec(buildCode(code))
                output=stdout.getvalue()
                # file_out("w", output.split("\n"), len(output.split("\n")))
                out_arr = output.splitlines()

                for i in range(len(out_arr)):
                    y, _ = stdscr.getyx()
                    if y >= height - 1:
                        stdscr.clear()
                        stdscr.addstr(f"{out_arr[i]}\n")
                    else:
                        stdscr.addstr(f"{out_arr[i]}\n")
                    # file_out("a", out_arr[i], y)

                stdout = io.StringIO()
                # stdscr.move(y+1+output.count('\n'),0)
                stdscr.addstr(">>> ", curses.color_pair(1))
                # file_out("w", bash_history)
                code = ''
                stdscr.refresh()

        else:
            code += chr(c)

    stdscr.refresh()


curses.wrapper(main)

execGlobal=globals()

import curses
from ASnake import build, execPy, ASnakeVersion
import subprocess
import io
from contextlib import redirect_stdout

import sys
import platform
compileDict = {'CPython': 'Python', 'PyPy': 'PyPy3'}

if hasattr(sys, "pyston_version_info"):
    # ^ Pyston dev's suggested this: https://github.com/pyston/pyston/issues/39
    # What scaredy cats!!
    compileTo = 'Pyston'
else:
    compileTo = compileDict[platform.python_implementation()]
del sys, compileDict, platform

ReplVersion = 'v0.2.1'

# for debugging only
def file_out(write_mode, *args):
    with open("streams.txt", write_mode, encoding='utf-8') as f:
        f.write(f"{args}\n")

def remove_char(word, idx):
    return ''.join(x for x in word if word.index(x) != idx)


def buildCode(code):
    return build(code, comment=False, optimize=False, debug=False, compileTo=compileTo, pythonVersion=3.9,enforceTyping=True)




def main(stdscr):
    # stdscr.nodelay(10)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.echo()
    stdout = io.StringIO()

    code = ''
    stdscr.addstr(f"ASnake {ASnakeVersion} \nRepl {ReplVersion}\n\n")
    stdscr.addstr(">>> ", curses.color_pair(1))

    bash_history = ['none']
    l_idx = [len(bash_history)]

    while True:
        c = stdscr.getch()

        # notetoself: x and y are cursor position
        y, x = stdscr.getyx()
        height, width = stdscr.getmaxyx()

        if c == curses.KEY_LEFT:
            if not x < 5:
                stdscr.move(y, x - 1)

        elif c == curses.KEY_RIGHT:
            stdscr.move(y, x + 1)

        # todo -> bash history
        elif c == curses.KEY_UP:
            for i in range(x, 3, -1):
                stdscr.delch(y, i)
                
            code = ''
            if l_idx[0] >= 1:
                # bash_history[l_idx[0]-1]
                l_idx[0] -= 1 
                stdscr.addstr(bash_history[l_idx[0]])
                code += bash_history[l_idx[0]]
                file_out("a", "up-> ", l_idx[0], bash_history[l_idx[0]])

        elif c == curses.KEY_DOWN:
            for i in range(x, 3, -1):
                stdscr.delch(y, i)
                
            code = ''
            if l_idx[0] <= len(bash_history)+1:
                # bash_history[l_idx[0]]
                l_idx[0] += 1 
                stdscr.addstr(bash_history[l_idx[0]])
                code += bash_history[l_idx[0]]
                file_out("a", "down-> ", l_idx[0], bash_history[l_idx[0]])

        elif c in {curses.KEY_BACKSPACE, 127}:
            if not x < 4:                    
                stdscr.delch(y, x)
                code = remove_char(code, x-4) 

                # file_out("a", code)
            else:
                stdscr.move(y, x + 1)

        elif c in {curses.KEY_ENTER, 10, 13}:
            bash_history.append(code)
            l_idx[0] = len(bash_history)
            # file_out("a", l_idx[0], "haha")
            if y >= height - 1:
                stdscr.clear()
                stdscr.refresh()
            else:
                stdscr.move(y + 1, 0)
                with redirect_stdout(stdout):
                    exec(buildCode(code),execGlobal)

                output = stdout.getvalue()
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

if __name__ == "__main__":
    curses.wrapper(main)
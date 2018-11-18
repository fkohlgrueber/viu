import sys
import signal
from enum import Enum
from pathlib import Path
from multiprocessing import Queue
from shutil import get_terminal_size
from threading import Thread
import tty
import termios

import black
import click
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import TerminalTrueColorFormatter


class Viu:
    def __init__(self, text_raw: str):
        self._text_raw = text_raw
        self._line_offset = 0
        self._text = ""
        self._text_formatted = ""
        self._num_columns = 0
        self._shown_until_end = False

    def main(self):
        wrapper(self._main)

    def _main(self, events: Queue):
        """Main function that handles `Event` events."""
        while True:
            self._print()
            evt: Event = events.get()
            if evt is Event.QUIT:
                break
            elif evt is Event.RESIZE:
                pass
            elif evt is Event.UP:
                self._line_offset = max(0, self._line_offset - 1)
            elif evt is Event.DOWN and not self._shown_until_end:
                self._line_offset += 1

    def _format(self):
        """Format string given the current terminal width"""
        term_size = get_terminal_size()

        if self._num_columns == term_size.columns:
            return

        # format code with black
        data_str = black.format_str(self._text_raw, term_size.columns)

        # highlight with pygments
        data_str = highlight(data_str, Python3Lexer(), TerminalTrueColorFormatter(style='monokai'))

        self._text_formatted = data_str
        self._num_columns = term_size.columns

    def _print(self):
        """Prints formatted code to the terminal."""

        def move_cursor(row, col):
            return f"\033[{row};{col}H"

        term_size = get_terminal_size()

        self._format()

        # calculate new formatted text
        new_text = move_cursor(row=1, col=1)
        i = 0
        for i, line in enumerate(self._text_formatted.split("\n")[self._line_offset:]):
            if i == term_size.lines - 1:
                # end of text cannot be shown. Show colon (":") in last line
                new_text += ":"
                self._shown_until_end = False
                break
            new_text += line
            new_text += move_cursor(row=i+2, col=1)
        else:
            # end of text is printed. Show "(END)" in last line and fill empty lines before with "~".
            for n in range(i + 1, term_size.lines - 1):
                new_text += "~"
                new_text += move_cursor(row=n+2, col=1)
            new_text += f"\033[30;47m(END)\033[49m_\033[0m" + move_cursor(row=term_size.lines, col=6)
            self._shown_until_end = True

        # only rewrite if content changed
        if self._text != new_text or True:
            # clear screen
            sys.stdout.write("\033[2J")

            # write new text
            sys.stdout.write(new_text)
            sys.stdout.flush()

            self._text = new_text


class Event(Enum):
    """Used to represent user events"""
    QUIT = 1
    UP = 2
    DOWN = 3
    RESIZE = 4


def wrapper(func):
    """
    Wrapper that performs terminal setup / restore tasks.
    """
    fd = sys.stdin.fileno()

    # save original terminal attributes
    old = termios.tcgetattr(fd)

    # change attributes
    # - ECHO = False (so that keyboard input isn't printed on the terminal)
    # - ICANON = False (so that input is sent immediately instead of line-by-line)
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] &= ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, termios.TCSAFLUSH, mode)

    # enable alternative screen buffer
    sys.stdout.write("\033[?1049h")

    # event queue
    event_queue = Queue()

    # set resize handler
    signal.signal(signal.SIGWINCH, lambda *_: event_queue.put(Event.RESIZE))

    # start a thread that handles user input
    Thread(target=handle_stdin, args=(event_queue,), daemon=True).start()

    try:
        func(event_queue)
    finally:
        # restore terminal attributes
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

        # disable alternative screen buffer
        sys.stdout.write("\033[?1049l")


def handle_stdin(events: Queue):
    """Read characters from stdin and generate events.

    This function is supposed to be executed in a separate thread.
    """
    while True:
        c = sys.stdin.read(1)
        if c == "\033":  # escape
            if sys.stdin.read(1) == "[":
                c3 = sys.stdin.read(1)
                if c3 == "A":
                    events.put(Event.UP)
                if c3 == "B":
                    events.put(Event.DOWN)
        elif c == "q":
            events.put(Event.QUIT)
        elif c == "j":
            events.put(Event.DOWN)
        elif c == "k":
            events.put(Event.UP)


@click.command()
@click.argument("file")
def main(file):
    """A small less-like Python code viewer with responsive formatting.

    \b
    Usage:
    q        *  Quit
    j  DOWN  *  Scroll down one line
    k  UP    *  Scroll up one line
    """
    file_path = Path(file)
    if not file_path.exists():
        print(f"File '{file_path}' does not exist.")
        return
    Viu(file_path.read_text()).main()


if __name__ == '__main__':
    main()

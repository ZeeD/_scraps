from __future__ import annotations

from functools import partial
from tkinter import Event
from tkinter import Label
from tkinter import StringVar
from tkinter import Tk
from unicodedata import name


def handle_paste(root: Tk, string_var: StringVar, _event: Event[Tk]) -> None:
    string_var.set('\n'.join(name(char)
                             for char in root.clipboard_get()  # type: ignore
                             if char))


def handle_keypress(string_var: StringVar, event: Event[Tk]) -> None:
    if not event.char:
        return
    string_var.set(name(event.char))


def main() -> None:
    root = Tk()
    string_var = StringVar()

    root.bind("<Key>", partial(handle_keypress, string_var))
    root.bind("<<Paste>>", partial(handle_paste, root, string_var))

    Label(root, textvariable=string_var).pack()
    root.mainloop()

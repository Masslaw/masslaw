from tkinter import Tk
from tkinter import filedialog


def file_selection_dialog():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames()
    return file_paths

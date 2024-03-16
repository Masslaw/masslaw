from tkinter import Tk
from tkinter import filedialog


root = Tk()
root.withdraw()


def file_selection_dialog():
    file_paths = filedialog.askopenfilenames()
    return file_paths

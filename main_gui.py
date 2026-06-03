import threading
import tkinter as tk
from tkinter import ttk, messagebox
import backend

class SportsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Sports Dashboard")
        self.root.geometry("600x650")

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(4, weight=1)

    def setup_ui(self):
        # Setup your UI elements here
        pass
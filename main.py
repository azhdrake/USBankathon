import requests
from Chart import usbankgui
from tkinter import Tk, Label, Button
import plotly.graph_objects as go



root = Tk()
my_gui = usbankgui(root)
root.mainloop()
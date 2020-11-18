from tkinter import *
from tkinter import ttk


def calculate(*args):
    print('hello world')


root = Tk()
root.title("Hollo")

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="is equivalent to", width=40).grid(column=1, row=2, sticky=E)

ttk.Label(mainframe, text="Img Path").grid(column=2, row=1, sticky=W)
imgpath = StringVar()
ttk.Label(mainframe, textvariable=imgpath).grid(column=3, row=1, sticky=(W, E))

ttk.Label(mainframe, text="Nom").grid(column=2, row=2, sticky=W)
name = StringVar()
name_entry = ttk.Entry(mainframe, width=32, textvariable=name)
name_entry.grid(column=3, row=2, sticky=(W, E))

ttk.Label(mainframe, text="Poids").grid(column=2, row=3, sticky=W)
weight = StringVar()
weight_entry = ttk.Entry(mainframe, width=32, textvariable=weight)
weight_entry.grid(column=3, row=3, sticky=(W, E))

ttk.Label(mainframe, text="Mat. G.").grid(column=2, row=4, sticky=W)
fat = StringVar()
fat_entry = ttk.Entry(mainframe, width=32, textvariable=fat)
fat_entry.grid(column=3, row=4, sticky=(W, E))

ttk.Label(mainframe, text="Ferme").grid(column=2, row=5, sticky=W)
farm = StringVar()
farm_entry = ttk.Entry(mainframe, width=32, textvariable=farm)
farm_entry.grid(column=3, row=5, sticky=(W, E))

ttk.Label(mainframe, text="Code Postal").grid(column=2, row=6, sticky=W)
postal = StringVar()
postal_entry = ttk.Entry(mainframe, width=32, textvariable=postal)
postal_entry.grid(column=3, row=6, sticky=(W, E))

ttk.Label(mainframe, text="Ville").grid(column=2, row=7, sticky=W)
town = StringVar()
town_entry = ttk.Entry(mainframe, width=32, textvariable=town)
town_entry.grid(column=3, row=7, sticky=(W, E))

ttk.Label(mainframe, text="Lat").grid(column=2, row=8, sticky=W)
lat = StringVar()
lat_entry = ttk.Entry(mainframe, width=32, textvariable=lat)
lat_entry.grid(column=3, row=8, sticky=(W, E))

ttk.Label(mainframe, text="Lng").grid(column=2, row=9, sticky=W)
lng = StringVar()
lng_entry = ttk.Entry(mainframe, width=32, textvariable=lng)
lng_entry.grid(column=3, row=9, sticky=(W, E))

ttk.Button(mainframe, text="Next", command=calculate).grid(column=3, row=10, sticky=E)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

name_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()

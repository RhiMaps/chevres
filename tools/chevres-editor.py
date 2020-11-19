import csv
import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

IMG_W = 400
IMG_H = 400

# Set the project root path, that is the parent dir of the current script
script_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(script_path, os.pardir))

data_path = os.path.join(root_path, 'datas')
default_goat_image = os.path.join(root_path, 'images', 'chevre.png')

csv_to_save = os.path.join(data_path, 'chevres_vincent_geocoded.csv')
if len(sys.argv) == 2:
    csv_to_read = sys.argv[1]
else:
    csv_to_read = csv_to_save

all_csv_rows = []
with open(csv_to_read, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in spamreader:
        all_csv_rows.append(row)


def show_status(message=''):
    print(message)
    statusmsg.set(message)


def save_csv(*args):
    # Save current first
    all_csv_rows[photo_index] = form2row()
    show_status("Saving csv to {} ...".format(csv_to_save))
    with open(csv_to_save, 'w') as csvfiletosave:
        csv_writer = csv.writer(csvfiletosave, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
        csv_writer.writerows(all_csv_rows)
    show_status("Saved csv to {}".format(csv_to_save))


photo_index = 0


def move_photo(step):
    global photo_index
    name_entry.focus()
    all_csv_rows[photo_index] = form2row()
    photo_index = photo_index + step
    my_row = all_csv_rows[photo_index]
    show_status('Display {}'.format(my_row[1]))
    row2form(my_row)


def previous_photo(*args):
    move_photo(-1)


def next_photo(*args):
    move_photo(+1)


def geocode_row(*args):
    geolocator = Nominatim(user_agent="my_application")
    my_row = form2row()
    adress = my_row[3] + " " + my_row[4]
    show_status("Geocoding '{}' ....".format(adress))
    try:
        geocodes = geolocator.geocode(adress, exactly_one=False)
    except GeocoderTimedOut:
        geocodes = None
        sys.stderr.write(adress)
    # if you dont find
    if geocodes is None:
        # look without postcode
        geocodes = geolocator.geocode(row[3], exactly_one=False)
        # or
        if geocodes is None:
            # just give up
            show_status("Unable to geocode '{}'".format(adress))
            return
    location, (my_lat, my_lng) = geocodes[0]
    show_status("'{}' found at {} ({}, {})".format(adress, location, my_lat, my_lng))
    my_row[7] = my_lat
    my_row[8] = my_lng
    row2form(my_row)


def form2row():
    my_row = [None] * 9
    my_row[0] = imgpath.get()
    my_row[1] = name.get()
    my_row[5] = weight.get()
    my_row[6] = fat.get()
    my_row[2] = farm.get()
    my_row[3] = postal.get()
    my_row[4] = town.get()
    my_row[7] = lat.get()
    my_row[8] = lng.get()
    return my_row


def row2form(my_row):
    imgpath.set(my_row[0])
    name.set(my_row[1])
    weight.set(my_row[5])
    fat.set(my_row[6])
    farm.set(my_row[2])
    postal.set(my_row[3])
    town.set(my_row[4])
    lat.set(my_row[7])
    lng.set(my_row[8])
    image_path = os.path.join(data_path, imgpath.get())
    if not os.path.isfile(image_path):
        show_status("No such image {}".format(image_path))
        image_path = default_goat_image
    my_image = Image.open(image_path)
    my_image = my_image.resize((IMG_W, IMG_H), Image.ANTIALIAS)
    my_photo_image = ImageTk.PhotoImage(my_image)
    imglabel.configure(image=my_photo_image)
    imglabel.image = my_photo_image


root = Tk()
root.title("Hollo")

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

image = Image.open(default_goat_image)
image = image.resize((IMG_W, IMG_H), Image.ANTIALIAS)
photo_image = ImageTk.PhotoImage(image)
imglabel = ttk.Label(mainframe)
imglabel.configure(image=photo_image)
imglabel.image = photo_image
imglabel.grid(column=1, row=2, rowspan=8, sticky=E)

statusmsg = StringVar()
ttk.Label(mainframe, textvariable=statusmsg).grid(column=1, row=14, columnspan=3, sticky=(W, E))

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

ttk.Button(mainframe, text="Prev", command=previous_photo).grid(column=3, row=10, sticky=E)
ttk.Button(mainframe, text="Next", command=next_photo).grid(column=3, row=11, sticky=E)
ttk.Button(mainframe, text="Save", command=save_csv).grid(column=3, row=12, sticky=E)
ttk.Button(mainframe, text="GeoCode", command=geocode_row).grid(column=3, row=13, sticky=E)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

name_entry.focus()
root.bind("<Control-Left>", previous_photo)
root.bind("<Control-Right>", next_photo)
root.bind("<Return>", save_csv)
root.bind("<Control-g>", geocode_row)

row2form(all_csv_rows[0])
root.mainloop()

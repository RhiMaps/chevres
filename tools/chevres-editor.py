import csv
import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

try:
    from chevres_config import IMG_W, IMG_H, IMG_EXT
except ModuleNotFoundError:
    IMG_W = 600
    IMG_H = 600
    IMG_EXT = "JPG"
    pass

# Set the project root path, that is the parent dir of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

data_path = os.path.join(root_dir, 'datas')
default_goat_image = os.path.join(root_dir, 'images', 'chevre.png')

out_csv_file_name = 'chevres.csv'
out_csv_file_path = os.path.join(data_path, out_csv_file_name)


class ChevreEditor:
    root = None
    photo_index = 0
    csv_headers = []
    csv_rows = []

    imglabel = None
    statusmsg = None
    name_entry = None

    imgpath = None
    name = None
    weight = None
    fat = None
    farm = None
    postal = None
    town = None
    lat = None
    lng = None

    def init_display(self):
        self.root = Tk()
        self.root.title("Goatstor")

        mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        image = Image.open(default_goat_image)
        image = image.resize((IMG_W, IMG_H), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)
        self.imglabel = ttk.Label(mainframe)
        self.imglabel.configure(image=photo_image)
        self.imglabel.image = photo_image
        self.imglabel.grid(column=1, row=2, rowspan=8, sticky=E)

        self.statusmsg = StringVar()
        ttk.Label(mainframe, textvariable=self.statusmsg).grid(column=1, row=14, columnspan=3, sticky=(W, E))

        ttk.Label(mainframe, text="Img Path").grid(column=2, row=1, sticky=W)
        self.imgpath = StringVar()
        ttk.Label(mainframe, textvariable=self.imgpath).grid(column=3, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="Nom").grid(column=2, row=2, sticky=W)
        self.name = StringVar()
        self.name_entry = ttk.Entry(mainframe, width=32, textvariable=self.name)
        self.name_entry.grid(column=3, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="Poids").grid(column=2, row=3, sticky=W)
        self.weight = StringVar()
        weight_entry = ttk.Entry(mainframe, width=32, textvariable=self.weight)
        weight_entry.grid(column=3, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="Mat. G.").grid(column=2, row=4, sticky=W)
        self.fat = StringVar()
        fat_entry = ttk.Entry(mainframe, width=32, textvariable=self.fat)
        fat_entry.grid(column=3, row=4, sticky=(W, E))

        ttk.Label(mainframe, text="Ferme").grid(column=2, row=5, sticky=W)
        self.farm = StringVar()
        farm_entry = ttk.Entry(mainframe, width=32, textvariable=self.farm)
        farm_entry.grid(column=3, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Code Postal").grid(column=2, row=6, sticky=W)
        self.postal = StringVar()
        postal_entry = ttk.Entry(mainframe, width=32, textvariable=self.postal)
        postal_entry.grid(column=3, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Ville").grid(column=2, row=7, sticky=W)
        self.town = StringVar()
        town_entry = ttk.Entry(mainframe, width=32, textvariable=self.town)
        town_entry.grid(column=3, row=7, sticky=(W, E))

        ttk.Label(mainframe, text="Lat").grid(column=2, row=8, sticky=W)
        self.lat = StringVar()
        lat_entry = ttk.Entry(mainframe, width=32, textvariable=self.lat)
        lat_entry.grid(column=3, row=8, sticky=(W, E))

        ttk.Label(mainframe, text="Lng").grid(column=2, row=9, sticky=W)
        self.lng = StringVar()
        lng_entry = ttk.Entry(mainframe, width=32, textvariable=self.lng)
        lng_entry.grid(column=3, row=9, sticky=(W, E))

        ttk.Button(mainframe, text="Prev", command=self.previous_photo).grid(column=3, row=10, sticky=E)
        ttk.Button(mainframe, text="Next", command=self.next_photo).grid(column=3, row=11, sticky=E)
        ttk.Button(mainframe, text="GeoCode", command=self.geocode_row).grid(column=3, row=12, sticky=E)
        ttk.Button(mainframe, text="Save", command=self.save_csv).grid(column=3, row=13, sticky=E)
        ttk.Button(mainframe, text="LoadDir", command=self.load_datadir).grid(column=3, row=14, sticky=E)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.name_entry.focus()
        self.root.bind("<Control-Left>", self.previous_photo)
        self.root.bind("<Control-Right>", self.next_photo)
        self.root.bind("<Control-s>", self.save_csv)
        self.root.bind("<Control-g>", self.geocode_row)

        self.show_status("Loaded {} images".format(len(self.csv_rows)))

    def show_status(self, message=''):
        # TODO: log it instead !
        try:
            self.statusmsg.set(message)
        except AttributeError:
            pass

    def csv_has_image(self, image_path):
        if self.csv_rows:
            images_list = [row[0] for row in self.csv_rows]
            res = image_path in images_list
        else:
            res = False
        return res

    def load_datadir(self, data_dir=None, *args):
        if data_dir is None:
            data_dir = data_path
        from pathlib import Path
        self.csv_headers = ['imgpath', 'name', 'ferme', 'code', 'ville', 'poids', 'grasse', 'lat', 'lng']
        # For each image in directory add to rows
        all_images = sorted(Path(data_dir).rglob('*' + IMG_EXT))
        for image_file in all_images:
            image_path = os.path.basename(image_file)
            # add only if not already in rows
            if self.csv_has_image(image_path):
                continue
            row = [''] * 9
            row[0] = image_path
            self.csv_rows.append(row)
        self.show_status("Loaded {} images".format(len(self.csv_rows)))

    def load_csv(self, filename):
        with open(filename, 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            all_csv = list(spamreader)
            self.csv_headers = all_csv[0]
            self.csv_rows = all_csv[1:]

    def save_csv(self, *args):
        # Save current first
        try:
            self.csv_rows[self.photo_index] = self.form2row()
        except AttributeError:
            pass
        # Concatenate with headers
        final_csv = [self.csv_headers] + self.csv_rows
        self.show_status("Saving csv to {} ...".format(out_csv_file_path))
        with open(out_csv_file_path, 'w', encoding="utf-8") as csvfiletosave:
            csv_writer = csv.writer(csvfiletosave, delimiter=';',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    lineterminator='\n')
            csv_writer.writerows(final_csv)
        self.show_status("Saved csv to {}".format(out_csv_file_path))

    def move_photo(self, step):
        self.save_csv()
        self.name_entry.focus()
        my_row = None
        try:
            self.csv_rows[self.photo_index] = self.form2row()
            self.photo_index = self.photo_index + step
            my_row = self.csv_rows[self.photo_index]
        except IndexError:
            self.photo_index = 0
            my_row = self.csv_rows[self.photo_index]
        self.show_status('Display {}'.format(my_row[1]))
        self.row2form(my_row)

    def previous_photo(self, *args):
        self.move_photo(-1)

    def next_photo(self, *args):
        self.move_photo(+1)

    def geocode_row(self, *args):
        geolocator = Nominatim(user_agent="my_application")
        my_row = self.form2row()
        adress = my_row[3] + " " + my_row[4]
        self.show_status("Geocoding '{}' ....".format(adress))
        try:
            geocodes = geolocator.geocode(adress, exactly_one=False)
        except GeocoderTimedOut:
            geocodes = None
            sys.stderr.write(adress)
        # if you dont find
        if geocodes is None:
            # look without postcode
            geocodes = geolocator.geocode(my_row[3], exactly_one=False)
            # or
            if geocodes is None:
                # just give up
                self.show_status("Unable to geocode '{}'".format(adress))
                return
        location, (my_lat, my_lng) = geocodes[0]
        self.show_status("'{}' found at {} ({}, {})".format(adress, location, my_lat, my_lng))
        my_row[7] = my_lat
        my_row[8] = my_lng
        self.row2form(my_row)

    def form2row(self, ):
        my_row = [None] * 9
        my_row[0] = self.imgpath.get()
        my_row[1] = self.name.get()
        my_row[5] = self.weight.get()
        my_row[6] = self.fat.get()
        my_row[2] = self.farm.get()
        my_row[3] = self.postal.get()
        my_row[4] = self.town.get()
        my_row[7] = self.lat.get()
        my_row[8] = self.lng.get()
        return my_row

    def row2form(self, my_row):
        self.imgpath.set(my_row[0])
        self.name.set(my_row[1])
        self.weight.set(my_row[5])
        self.fat.set(my_row[6])
        self.farm.set(my_row[2])
        self.postal.set(my_row[3])
        self.town.set(my_row[4])
        self.lat.set(my_row[7])
        self.lng.set(my_row[8])
        image_path = os.path.join(data_path, self.imgpath.get())
        if not os.path.isfile(image_path):
            self.show_status("No such image {}".format(image_path))
            image_path = default_goat_image
        my_image = Image.open(image_path)
        my_image = my_image.resize((IMG_W, IMG_H), Image.ANTIALIAS)
        my_photo_image = ImageTk.PhotoImage(my_image)
        self.imglabel.configure(image=my_photo_image)
        self.imglabel.image = my_photo_image

    def run_loop(self):
        self.row2form(self.csv_rows[0])
        self.root.mainloop()


if __name__ == '__main__':

    csv_to_read = None

    if len(sys.argv) == 2:
        csv_to_read = sys.argv[1]
    else:
        csv_to_read = out_csv_file_path

    my_editor = ChevreEditor()

    if os.path.exists(csv_to_read):
        my_editor.load_csv(csv_to_read)
    else:
        my_editor.load_datadir(data_path)

    my_editor.init_display()
    my_editor.run_loop()

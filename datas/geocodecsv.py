import csv
import sys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# df = pd.read_csv('./file.csv')
# print( df )

geolocator = Nominatim(user_agent="my_application")

with open('file.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        adress = row[2] + " " + row[3]
        try:
            geocodes = geolocator.geocode(adress, exactly_one=False)
        except GeocoderTimedOut:
            sys.stderr.write(adress)
            continue
        # if you dont find
        if None == geocodes:
            # look without postcode
            geocodes = geolocator.geocode(row[3], exactly_one=False)
            # or
            if None == geocodes:
                # just give up
                location = adress
                lat = 0
                lon = 0
        location, (lat, lon) = geocodes[0]
        # print row[0]+","+ row[1]+","+ row[2]+","+ row[3]+","+ lat+","+ lon
        row.extend([str(lat), str(lon)])
        print(';'.join(row))

# address = df.nom

# for a in address:
#    result = Geocoder.geocode(a)
#    print(result[0].coordinates)

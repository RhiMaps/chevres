# chevres

Goat's cheese label map

A geolocalised collection of french goatcheeses

## See online

https://rhimaps.github.io/chevres

## Run locally

`python tools/simplehttpserver.py`
and open localhost:8000

or simply open `index.html` in you navigator

## chevres-editor.py

### installing 

#### with pip

#### with anaconda/spyder


### running with spyder

run the script on your images dir 

* either as argument on command line

    python3 chevres-editor.py /my/data/dir

* or running it inside the directory

    cp chevres-editor.py /my/data/dir
    cd /my/data/dir
    python3 chevres-editor.py 


    or through spyder


#### process

* uses existing chevres.csv
* or creates it with all existing images in dir

#### chevres-editor.py

this gui form allows to read all png images stored under the  data/ dir, and write more meta info in chevres.csv file

* run python3 chevres-editor.py
* update latests images metadata
* go back to terminal
* git add datas/ 
* git commit -m "my commit message"
* git push

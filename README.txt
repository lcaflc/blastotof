              Blastotof v1.0
              --------------

Requires:
 - python
 - python Imagining Library
 - dcraw (for raw files support)
 - exiv2 (for raw files support)
 - exiftran

Blastotof is a simple jpg photos repository presentation and browser tool. It create thumbnails himself, support a description for each photo, detailled title and different css styles per directory.

This is a python script that only need the standard python distribution. It require imagemagick if you want to convert thumbnails on the fly (done only the first time you view a directory). It must be used as a cgi script with the apache webserver for exemple. I personally use apache + mod_python in cgi handler mode, it speed up a lot the python scripts.

How it works...
the script list and walk accross a filesystem hierarchy. so simply put it in the top directory of your photo collection, made it available via a webserver and it works. (if this directory allow cgi-bin execution). You probably need to rename the index.py into index.cgi if you don't use mod_python. This is for exemple a photos repository hierarchy:

| top directory
  | index.py
  | TITLE.txt
  |-> Hollidays
  |  |-> France
  |  |  | P0001.jpg
  |  |  | P0002.jpg
  |  |  | ....
  |  |-> Canada
  |  |  | P0010.jpg
  |  |  | ....
  |-> Parties
  |  |-> Halloween
  |  |  | ....
  |  |-> Xmas
  |  |  | ....
  ...

You can use thumbnails you create for the small view, the files must be named [bigphotofilename]_tn.jpg, or let Blastotof create them. In order to create thumbnails Blastotof must be able to write to the photo directory, in most case it's not a problem because the cgi is executed with your username (all the FAI acccounts) but with apache default configuration it's not the case.

Title and photo desctiption.
The title at the top of the page is directly printed from the [directory]/TITLE.txt. Put all that you want in this file (even html code) and it will be put into the page html code.
It works the same way for the DESC.txt file. The file syntax is very simple [photofile]TAB[description], you can look at the provided DESC.txt for an exemple.

What's the problem, it's ugly...
Yes if don't use css style file you only have a minimalist black and white design. the script search for a style.css file in the current directory and use it as css template for this directory. 3 different example files are in the tarball, make a link from one of these to [directory]/style.css and this directory will use this css style. You can make more stylesheet file using the definitions provided in the default one.



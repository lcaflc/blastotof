#!/usr/bin/python

import os,sys,string,re,urllib
import cgitb
import Image

cgitb.enable()

debug       = False
version     = "3.0"
title       = "Blastotof"

stylefile   = "style.css"
readmefile  = "TITLE.txt"
cachedir    = ".cache"

dirlist     = []
toflist     = {}

A_LIST		= "list"
A_SLIDE		= "slide"
A_CLEANUP       = "cleanup"


# parse query string and return a dict
def readquerystring():
    qe={}
    if os.environ["QUERY_STRING"]:
        qs=os.environ["QUERY_STRING"].split('&')
        for i in qs:
            if i.split('=')[1] :
                qe[i.split('=')[0]] = urllib.unquote(i.split('=')[1])
    return qe

qt = readquerystring()

print "Content-Type: text/html\n"


if "path" in qt:
    qt["path"] = os.path.normpath(qt["path"])
    if qt["path"][0] == '/' or re.match("\.\.\/+.*", qt["path"]): 
        qt["path"]="./"
else:
    qt["path"] = "./"
if not "action" in qt:
    qt["action"] = A_LIST
if qt["action"] == A_SLIDE and "file" not in qt:
    print "Error must set a file"

if qt["action"] == A_CLEANUP:
    print "<h5>Cleaning up cache</h5>"
    for root, dirs, files in os.walk(cachedir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    qt["action"] = A_LIST

path = qt["path"]
if "file" in qt: file = urllib.unquote(qt["file"])
action = qt["action"]

def choose_style_file():
    # search if a style has been defined for this path
    global stylefile
    if os.path.isfile(os.path.join(path,stylefile)):
        stylefile = os.path.join(path,stylefile)
    print "<link href='%s' rel='stylesheet' type='text/css'>"%(stylefile)

def print_headers():
    print "<html>\n<head>\n<title>%s</title>"%(title)
    choose_style_file()
    print """
    <script src='jquery.js' type='text/javascript'></script>
    <script src='script.js' type='text/javascript'></script>
    </head><body>
    <div id='global'>
    """
    

def show_title():
    # get and print the readme file
    if os.path.isfile(os.path.join(path, readmefile)):
        print """
        <div id='title'>
        %s
        </div>"""%open(os.path.join(path, readmefile)).read()
    print "<div id='path'>"
    print path
    # FIXME link only if file exist
#    print "<a href=?download=%s>(download)</a>" % path
    print "</div>"


def show_dir_menu():
    # print the menu
    print """
    <div id='menu-dir'>
    <ul class='menu-li'>
    <li><a href='?'>top</a></li>
    <li><a href='?path=%s'>back</a></li>
    """%(urllib.quote(os.path.split(path)[0]))
    if len(dirlist):
        print "<li></li>"
    for i in dirlist:
        print("<li><a href='?path=%s'>%s</a></li>")%(urllib.quote(i),os.path.basename(i))
    print "</ul></div>"

def show_photo_menu():
    # get and print the readme file
    print "<div id='menu-photo'><ul id='menu-photo-list'>"
    count = 0
    for p in sortedkeysfromdict(toflist):
        print """
        <li><a href='%s'><img border=0 src='%s' alt='%s'></a></li>"""%\
        (toflist[p]["med_thumb"],
         toflist[p]["mini_thumb"],
         toflist[p]["desc"])
        count += 1
        if count == 2:
            print ""
            count = 0
    print "</div>"

def print_footer():
    print """
    <div id="footer">
    Blastotof v%s, <a href='http://glot.net'>caf@glot.net</a>
    </div>
    </div>
    </body></html>
    """%(version)

def list_files():
    # build list of directory and photos
    for f in os.listdir(path):
        if debug: print f
        pathname = os.path.join(path, f)
        if f == cachedir: continue
        if os.path.basename(pathname).startswith(".") == False:
            if os.path.isdir(pathname):
                # this is a directory !!!
                dirlist.append(os.path.normpath(pathname))
            elif os.path.isfile(pathname):
                # this is a file, is it a jpg file ?
                if re.match("(.+\.(jpg|JPG|tiff|tif)$)", f) :
                    # maybe he got a desc file associated
                    if os.path.isfile(pathname + ".txt"):
                        desc = open(pathname + ".txt").readlines()[0]
                    else:
                        desc = ""
                    tof={"path" : pathname,
                         "desc" : desc.rstrip(),
                         "thumb": create_thumb(pathname),
                         "mini_thumb": create_mini_thumb(pathname),
                         "med_thumb": create_med_thumb(pathname),
                         
                         }
                    
                    if debug : print "added this photo: " + str(tof)
                    
                    toflist[pathname] = tof

    dirlist.sort()

def sortedkeysfromdict(adict):
    keys = adict.keys();
    keys.sort()
    return keys


def create_generic_thumb(p, prefix, size):
    try:
        os.mkdir('%s/%s' % (cachedir,os.path.basename(path)))
    except OSError, e:
        pass
    thumb_file = "%s/%s/%s_%s.jpg" % (cachedir, os.path.basename(path), os.path.basename(p[:-4]), prefix)
    if not os.path.isfile(thumb_file) or os.path.getmtime(p) >= os.path.getmtime(thumb_file):
        try:
            if debug: print p, thumb_file
            im=Image.open(p)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(thumb_file, "JPEG")
        except IOError, err:
            print "Cannot create thumbnails ", p, err
    return thumb_file

def create_mini_thumb(p):
    return create_generic_thumb(p, "mini", (100, 75))

def create_med_thumb(p):
    return create_generic_thumb(p, "med", (640, 480))

def create_high_thumb(p):
    return create_generic_thumb(p, "high", (800, 600))

def create_thumb(p):
    return create_generic_thumb(p, "tn", (200, 150))


   
print_headers()
list_files()
show_title()
print "<div id='menu'>"
show_dir_menu()

if action == A_SLIDE:
    show_photo_menu()
    # fermeture de la div id=menu
    print "</div>"

    # FIXME add full size download link only if we want to
    # <a href='%s'></a>%cur["path"]
#    print("<img id='photo-show' border=0 src='%s' alt='%s'><p class='photo-text'>%s</p>\n" %(medium_thumb, cur["desc"], cur["desc"]))

# display the container and load the image we click on
    print """
    <div id='photo-big'>
    </div>
    <script type='text/javascript'>
    showImage('%s', '%s');
    </script>
    """%(toflist[file]["med_thumb"],
         toflist[file]["desc"])

elif action == A_LIST :
    # fermeture de la div id=menu
    print "</div>"
    print "<div id='photo-list'><lu id='photo-list-ul'>"
    if toflist:
        cl=1
        for p in sortedkeysfromdict(toflist):
            # if the thumbnails doesn't exist generate it
            #(current path must be writable by the user running the httpd)
            # if there is not file description generate an empty one
            print """
            <li><a valign=center href='?action=%s&path=%s&file=%s'>
            <img valign=center border=0 src='%s' alt='%s'></a>
            <p class='photo-text'>%s</p></li>\n"""%\
            (A_SLIDE,
             path,urllib.quote(p),
             toflist[p]["thumb"],
             toflist[p]["desc"],
             toflist[p]["desc"])
            # we have 4 photos, jumping to new row
            if cl%3==0: print('\n')
            cl+=1
    print "</ul></div>"

print_footer()

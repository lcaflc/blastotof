#!/usr/bin/python

import os,sys,string,re,urllib
import Image

debug       = 0
version     = "2.0"
title       = "Blastotof"

stylefile   = "style.css"
readmefile  = "TITLE.txt"
descfile    = "DESC.txt"
cachedir    = ".blastotof"

dirlist     = []
toflist     = []
desc        = {}

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
    print "</head><body>"
    print "<table width=100% align=left>"
    

def show_title():
    # get and print the readme file
    if os.path.isfile(os.path.join(path, readmefile)):
        print "<tr><td></td><td class='title-td'><h1 class='title-text'>"
        print open(os.path.join(path, readmefile)).read()
        print "</h1></td></tr>"
    print "<tr colspan=2><td colspan=2 class='menu-td' width='100%' align='center'>"
    print path#"&nbsp"
    # FIXME link only if file exist
#    print "<a href=?download=%s>(download)</a>" % path
    print "</td></tr>"


def show_dir_menu():
    print "<table width=220px>"

    # print the menu
    print "<tr><td width=220px align=right class='menu-td'><a class='menu-a' href='?'>top</a></td></tr>"
    print "<tr><td width=220px align=right class='menu-td'><a class='menu-a' href='?path=" + urllib.quote(os.path.split(path)[0]) + "'>back</a></td></tr>"
    if len(dirlist):
        print "<tr><td width=220px class='menu-td'></td></tr>"
    for i in dirlist:
        print("<tr><td width=220px class='menu-td'><a class='menu-a' href='?path=%s'>%s</a></td></tr>")%(urllib.quote(i),os.path.basename(i))
    print "</table>"

def show_photo_menu():
    # get and print the readme file
    print "<table width=220px>"
    # print the menu
    print "<tr align=right  colspan=2><td colspan=2 class='menu-td'></td></tr>"
    count = 0
    print "<tr>"
    for i in toflist:
        thumb = create_mini_thumb(i)
        print("<td align=center class='menu-td' width=70px><a href='?action=%s&path=%s&file=%s'><img border=0 src='%s' alt='%s'></a><span class='toflist-text'>%s</span></td>\n"%(A_SLIDE, path, urllib.quote(os.path.basename(i)), thumb, thumb, ""))
        count += 1
        if count == 2:
            print "</tr><tr>"
            count = 0
    print "</table>"

def print_footer():
    print "</tr>"
    print "<tr colspan=2><td colspan=2 class='menu-td' width='100%' align='right'>"
    print "Blastotof v%s, <a class='menu-a' href='http://glot.net'>caf@glot.net</a>"%(version)
    print "</td></tr></table></body></html>"

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
                # this is a file, is it a jpg file ? (and not a thunmbnail file)
                if re.match("(.+\.(jpg|JPG|tiff|tif)$)", f) :
                    if debug : print "added this photo: " + pathname
                    toflist.append(pathname)
    dirlist.sort()
    toflist.sort()

def read_desc_file():
    # build the list of photos descriptions
    global desc
    if os.path.isfile(os.path.join(path, descfile)):
        for l in open(os.path.join(path, descfile)).readlines():
            tof,ds=l.split(".jpg", 1)
            desc[path + "/" + tof + ".jpg"] = ds
    if debug: print desc	


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
    return create_generic_thumb(p, "med", (1024, 768))

def create_thumb(p):
    return create_generic_thumb(p, "tn", (200, 150))

def show_photo(prev, cur, next):
    medium_thumb = create_med_thumb(cur)
    print "<td valign=top><table><tr>"
    print("<td width=200 align=center class='toflist-td' ><a href='%s'><img border=0 src='%s' alt='%s'></a>%s</span></td>\n" %(cur,  medium_thumb, "", ""))
    print "</tr></table></td>"

   
print_headers()
list_files()
read_desc_file()
show_title()
print "<tr><td valign=top>"
show_dir_menu()
 
if action == A_SLIDE:
    prev = None
    cur  = None
    next = None
    show_photo_menu()
    print "</td>"
    for idx in range(len(toflist)):
        if os.path.basename(toflist[idx]) == file:
            cur = toflist[idx]
            if idx > 0: prev = toflist[idx-1]
            if idx < len(toflist) -1 : next = toflist[idx+1]
            show_photo(prev, cur, next)
    print_footer()

elif action == A_LIST :
    print "</td>"
    print "<td valign=top align=right><table><tr valign=top >"
    if toflist:
        cl=1
        for p in toflist:
            # if the thumbnails doesn't exist generate it
            #(current path must be writable by the user running the httpd)
            thumb_file = create_thumb(p)
            # if there is not file description generate an empty one
            if not desc.has_key(p): desc[p] = ""
            print("<td align=center valign=center class='toflist-td' width=200px><a valign=center href='?action=%s&path=%s&file=%s'><img valign=center border=0 src='%s' alt='%s'></a><span class='toflist-text'>%s</span></td>\n"%(A_SLIDE, path,urllib.quote(os.path.basename(p)),thumb_file,desc[p],desc[p]))
            # we have 4 photos, jumping to new row
            if cl%3==0: print('</tr><tr valign=top>\n')
            cl+=1
    print "</tr></table></td>"
    print_footer()

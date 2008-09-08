import os,sys,string,re,urllib

version="1.0"
title="Blastotof"

debug=0
stylefile="style.css"
readmefile="TITLE.txt"
descfile="DESC.txt"


print "Content-Type: text/html\n"
print "<html>\n<head>\n<title>%s</title>"%(title)

# get the current path from the QUERY_STRING
qs=os.environ["QUERY_STRING"]
if qs :
	if debug: print qs
	qs = urllib.unquote(qs)
	qs=os.path.normpath(qs)
	if qs[0] == '/' or re.match("\.\.\/+.*", qs): path="./"
	else : path=qs
else : path="./"

# search if a style has been defined for this path
if os.path.isfile(os.path.join(path,stylefile)):
	stylefile = os.path.join(path,stylefile)
print "<link href='%s' rel='stylesheet' type='text/css'>"%(stylefile)
print "</head><body>"

# curent path file and directory list
dirlist = []
toflist = []

# build list of directory and photos
for f in os.listdir(path):
	if debug: print f
	pathname = os.path.join(path, f)
	if os.path.isdir(pathname):
		# this is a directory !!!
		dirlist.append(os.path.normpath(pathname))
	elif os.path.isfile(pathname):
		# this is a file, is it a jpg file ? (and not a thunmbnail file)
		if re.match("^.+/(.+\.jpg$)", pathname) and not re.match("^.+/(.+\_tn.jpg$)", pathname):
			if debug : print "added this photo: " + pathname
			toflist.append(pathname)

#sort lists
dirlist.sort()
toflist.sort()
if debug:
	print dirlist
	print toflist

# get and print the readme file
print "<table><tr><td></td><td class='title-td'><h1 class='title-text'>"
if os.path.isfile(os.path.join(path, readmefile)):
	print open(os.path.join(path, readmefile)).read()
print "</h1></td></tr>"

# print the menu
print "<tr><td valign='top'><table width='200px'>"
print "<tr><td class='menu-td'><a class='menu-a' href='?./'>top</a></td></tr>"
print "<tr><td class='menu-td'><a class='menu-a' href='?./" + urllib.quote(os.path.split(path)[0]) + "'>back</a></td></tr>"
for i in dirlist:
	print("<tr><td class='menu-td'><a class='menu-a' href='?%s'>%s</a></td></tr>")%(urllib.quote(i),i)
print "</table></td><td>"

# build the list of photos descriptions
desc = {}
if os.path.isfile(os.path.join(path, descfile)):
	for l in open(os.path.join(path, descfile)).readlines():
		tof,ds=l.split("	")
		desc[path + "/" + tof] = ds
if debug: print desc	

# yeah here we go converting and printing photo list
if toflist:
	print("<table align='center'><tr align=center>")
	cl=1
	for p in toflist:
		# if the thumbnails doesn't exist generate it
		#(current path must be writable by the user running the httpd)
		if not os.path.isfile(p[:-4]+"_tn.jpg") :
			ex = "convert -size 200x150 '" + p + "' -resize 200x150 '" + p[:-4] + "_tn.jpg'"
			if debug : print ex
			os.system(ex)
		# if there is not file description generate an empty one
		if not desc.has_key(p): desc[p] = ""
		print("<td class='toflist-td' width=200px><a href='%s'><img border=0 src='%s_tn.jpg' alt='%s'></a><span class='toflist-text'>%s</span></td>\n"%(urllib.quote(p),urllib.quote(p[:-4]),desc[p],desc[p]))
		# we have 4 photos, jumping to new row
		if cl%3==0: print('</tr><tr align=center>\n')
		cl+=1
	print("</tr></table>")
print "</td></tr>"

# print footer
print "<tr><td></td><td class='menu-td' width='100%' align='right'>"
print "Blastotof v%s, <a class='menu-a' href='http://glot.net'>caf@glot.net</a>"%(version)
print "</td></tr></table></body></html>"

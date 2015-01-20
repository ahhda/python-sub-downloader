#-------------------------------------------------------------------------------
# Name      : subtitle
# Created By: Anuj Bansal
#-------------------------------------------------------------------------------

import sys, os, hashlib

try:
    import urllib.request, urllib.parse
    Ver=3
except ImportError:
    import urllib2
    Ver=2

#this hash function receives the name of the file and returns the hash code
#SubDB requires this kind of hashing

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

extension=[".mp4",".avi",".flv",".mkv"]

def download(filename):

    flag=0
    for ext in extension:
        if ext in filename:
            filename=filename.replace(ext,'')
            flag=1
            break
    if flag!=1:
    	return
    	
    filehash=get_hash(filename+ext)
    
    url = "http://api.thesubdb.com/?action=download&hash=" + filehash + "&language=en"

    agent={ 'User-Agent' : 'SubDB/1.0 (python-sub-downloader/1.0; https://github.com/ahhda/python-sub-downloader)' }

    try:
    	if Ver == 3:
        	req = urllib.request.Request(url, None, agent)
        	response = urllib.request.urlopen(req).read()
    	else:
        	req = urllib2.Request(url, '', agent)
        	response = urllib2.urlopen(req).read()
        srt=filename+'.srt'
        writefile=open(srt,'wb')
    	writefile.write(response)
    except:
    	print "Not found for", filename

dirc = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(dirc):
    #download subtitles for all files in folder
    for onefile in files:
        download(onefile)
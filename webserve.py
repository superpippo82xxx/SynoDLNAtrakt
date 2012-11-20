# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import cherrypy, os
from Cheetah.Template import Template
import datetime
from lib.themoviedb import tmdb
import urllib
import os

from synodlnatrakt import helper
from synodlnatrakt.logger import logger
from synodlnatrakt import config
from synodlnatrakt import db
from lib.tvdb_api import tvdb_api
APPDIR = os.path.dirname(os.path.abspath(__file__))
INI_FILENAME = os.path.join(APPDIR, "webserve.ini")

class Root(object):
	def index(self):
		return 'Please check your <a href="settings">settings</a><br /> or your <a href="log">logfile</a>'
	index.exposed = True
    
	def settings(self):
		return "Hello world!"
	settings.exposed = True
	index.exposed = True

	def log(self):
		logcontent = open('SynoDLNAtrakt.log').read()
		message = "<code>{0}</code>".format(logcontent)
		filename = os.path.join(APPDIR, "data/logs.tmpl")
		template = Template(file = filename)

		template.title = "SynoDLNAtrakt Logs"
		template.content = logcontent
		return str(template)  
	log.exposed = True
	index.exposed = True

	def runSyno(self):
		os.popen("python SynoDLNAtrakt.py")
	log.runSyno = True
	index.runSyno = True

	def lastviewed(self):
		myDB = db.DBConnection()
		result = myDB.select("SELECT * from scrobble ORDER BY lastviewed DESC")
		content = "<table><th>Serie</th><th>Episode</th><th>Datum</th><tr>"
		for entry in result:
			if entry["type"] == "series":
				date = datetime.datetime.fromtimestamp(float(entry["lastviewed"]))
				if not os.path.exists("data/cache/{0}.jpg".format(entry["tvdb_id"])):
					t = tvdb_api.Tvdb(banners = True)
					imagekeys = t[entry["name"]]["_banners"]["series"]["graphical"]
					imageurl = t[entry["name"]]["_banners"]["series"]["graphical"][imagekeys.keys()[0]]["_bannerpath"]
					cachedir = "data/cache/"
					name = cachedir + str(entry["tvdb_id"]) + '.jpg'
					imagedata = urllib.urlopen(imageurl).read()
					f = open(name, 'w')
					f.write(imagedata)
					f.close()
				image = "<img src='data/cache/{0}.jpg' width='250'/>".format(entry["tvdb_id"])

				
				#image = t['scrubs']['_banners']['poster']['680x1000']['35308']['_bannerpath']
				content = content + "<td>{0}</td><td>S{1}E{2}</td><td>{3}</td></tr>".format(image, entry["season"], entry["episode"], date)
				#content = content + "{0}".format(image)
			else:	
				if not os.path.exists("data/cache/{0}.jpg".format(entry["imdb_id"])):
					results = tmdb.search(entry["name"])
					cachedir = "data/cache/"
					name = cachedir + results[0]["imdb_id"] + '.jpg'
					url = results[0]["images"][0]["original"]
					imagedata = urllib.urlopen(url).read()
					f = open(name, 'w')
					f.write(imagedata)
					f.close()

				image = "<img src='data/cache/{0}.jpg' width='150' />".format(entry["imdb_id"])
				date = datetime.datetime.fromtimestamp(float(entry["lastviewed"]))
				content = content + "<td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(image, entry["year"], date)
		return content
	lastviewed.exposed = True
	log.exposed = True	

def main():
	cherrypy.quickstart(Root(), config = INI_FILENAME)


if __name__ == "__main__":
	main()
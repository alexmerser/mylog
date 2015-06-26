#coding : utf8
from utils import *
import ConfigParser
import sys

options = {}

functions = {
	'template_url' : template_url,
	'admin_url'    : admin_url,
	'C'			   : C,
	'get_upload'   : get_upload
}


def init():

	global options

	cf = ConfigParser.ConfigParser()
	cf.read(cur_dir() + 'config.ini')

	for it in cf.options("config"):
		options[it] = cf.get("config",it)

	options["pagecount"] = int(options["pagecount"])

def update(map):

	cf = ConfigParser.ConfigParser()
	cf.read(cur_dir() + 'config.ini')

	for key in map:
		options[key] = map[key].encode('utf8')
		cf.set("config",key,map[key].encode('utf8'))

	fp = open(cur_dir() + 'config.ini','w')

	cf.write(fp)

	fp.close()
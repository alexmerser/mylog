#coding : utf8
from utils import *
import ConfigParser

options = {}

functions = {
	'template_url' : template_url,
	'admin_url'    : admin_url,
	'C'			   : C
}


def init():

	global options

	cf = ConfigParser.ConfigParser()
	cf.read('config.ini')

	for it in cf.options("config"):
		options[it] = cf.get("config",it)

	options["pagecount"] = int(options["pagecount"])

def update(map):

	cf = ConfigParser.ConfigParser()
	cf.read('config.ini')

	for key in map:
		options[key] = map[key]
		cf.set("config",key,map[key])



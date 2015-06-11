#coding : utf8
from utils import *
import db

options = {
	'siteurl'	 : "http://127.0.0.1",

	'blogname'   : "Mylog",
	'nickname'   : "floyd",
	'email'      : "root#7c00.org",
	'descript'   : "要么庸俗，要么孤独。",

	'templates'  : "templates/",
	'admin' 	 : "admin/",
	'upload'     : "upload/",
	'pagecount'  : 5,

	'db_path'    : 'db/data.db',
	'split_sign' : '[split_sign]',
	'username'   : 'admin',
	'password'   : '123456'
}

functions = {
	'template_url' : template_url,
	'C'			   : C

}
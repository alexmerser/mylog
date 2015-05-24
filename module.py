#coding : utf8
import tornado.web
import config
from utils import *

import sys
import db
import os

class Header(tornado.web.UIModule):
	def render(self):
		return self.render_string(tmp_dir("header.html"))
		
class Sidebar(tornado.web.UIModule):
	def render(self):
		list = db.get_classify()
		return self.render_string(tmp_dir("sidebar.html"),classify = list)
		
class Footer(tornado.web.UIModule):
	def render(self):
		return self.render_string(tmp_dir("footer.html"))


#内置方法
class SiteURL(tornado.web.UIModule):
	def render(self,path):
		return C('siteurl') + "/static/" + path

class Config(tornado.web.UIModule):
	def render(self,key):
		return C(key)

class GetClassifyName(tornado.web.UIModule):
	def render(self,key):
		return db.get_clsfbyid(key)

#导入所有模块

sys.path.append("module")

for it in os.listdir(cur_dir() + "module"):
		name = it.split('.')[0]
		__import__(name,globals(),locals(),['*'])
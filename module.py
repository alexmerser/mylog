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
class Config(tornado.web.UIModule):
	def render(self,key):
		return C(key)

class GetClassifyName(tornado.web.UIModule):
	def render(self,key):
		return db.get_clsfbyid(key)
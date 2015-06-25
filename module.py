#coding : utf8
import tornado.web
import config
from utils import *

import sys
import db
import os


class BaseModule(tornado.web.UIModule):
	def MyRender(self,file,**args):

		args = dict(args.items()+config.functions.items())

		return self.render_string(file,**args)

class Header(BaseModule):
	def render(self):
		return self.MyRender(tmp_dir("header.html"))
		
class Sidebar(BaseModule):
	def render(self):
		list = db.get_classify()
		return self.MyRender(tmp_dir("sidebar.html"))
		
class Footer(BaseModule):
	def render(self):
		return self.MyRender(tmp_dir("footer.html"))


class Admin_Header(BaseModule):
	def render(self):
		return self.MyRender(admin_dir("header.html"))

class Admin_Sidebar(BaseModule):
	def render(self):
		return self.MyRender(admin_dir("sidebar.html"))
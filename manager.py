#coding: utf8
import tornado.web
from utils import *

# 简单的用户认证实现
class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

	def check_login(self):
		try:
			if self.get_current_user() == C('username'):
				return True
		except:
			self.set_secure_cookie("user","")
			return False

 
# 实际业务类实现
class AdminHandler(BaseHandler):
	def get(self):

		if self.check_login() == False:
			self.redirect("/admin/")
			return
		self.render(tmp_dir("admin/index.html"))

 

#管理页
class LoginHandler(BaseHandler):

	def get(self):
			self.render(tmp_dir("admin/login.html"))

	def post(self):

		try:
			user = self.get_argument("user")
			pwd = self.get_argument("pwd") 
		except:
			self.redirect("/admin/")

		if user == C('username') and pwd == C('password'):
			self.set_secure_cookie("user", user)
			self.redirect("/admin/index")

		else:
			self.redirect("/admin/")

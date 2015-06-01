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
			else:
				return False
		except:
			self.set_secure_cookie("user","")
			return False

 
# 实际业务类实现
class AdminHandler(BaseHandler):
	def get(self,page):

		if self.check_login() == False:
			self.redirect("/login")
			return

		#处理请求页面
		try:
			self.render(tmp_dir("admin/%s.html" % page))
		except:
			self.redirect("/login")

	def post(self,page):
		if self.check_login() == False:
			self.redirect("/login")
			return

		m = self.get_argument("m","none")

		if m == "add_article":
			print self.get_argument("title")
			self.redirect("/admin/index")
		else:
			self.redirect("/login")



 

#管理页
class LoginHandler(BaseHandler):

	def get(self):
			self.set_secure_cookie("user","")
			self.render(tmp_dir("admin/login.html"))

	def post(self):
		try:
			user = self.get_argument("user")
			pwd = self.get_argument("pwd") 
		except:
			self.redirect("/login")

		if user == C('username') and pwd == C('password'):
			self.set_secure_cookie("user", user)
			self.redirect("/admin/index")

		else:
			self.redirect("/login")

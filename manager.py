#coding: utf8
import tornado.web
import db
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

		#校验身份
		if self.check_login() == False:
			self.redirect("/login")
			return

		#处理请求页面
		if 1==1:
			#文章管理
			if page == "articles":
				self.render(tmp_dir("admin/%s.html" % page),articles = db.get_article())

			#更新文章
			elif page == "update":

				id = self.get_argument("id")
				self.render(tmp_dir("admin/%s.html" % page),article = db.get_atcbyid(id,True),id = id)

			#评论管理
			elif page == "comments":

				self.render(tmp_dir("admin/%s.html" % page),comments = db.get_comments())

			#留言管理
			elif page == "guests":

				self.render(tmp_dir("admin/%s.html" % page),guests = db.get_guest())

			#返回自定义页面
			else:
				self.render(tmp_dir("admin/%s.html" % page))
		else:
			self.redirect("/login")

	def post(self,page):

		#校验身份
		if self.check_login() == False:
			self.redirect("/login")
			return

		m = self.get_argument("m","none")

		#添加文章
		if m == "add_article":
			title = self.get_argument("title" ,"")
			content = self.get_argument("content","")

			if title == "" or content == "":
				self.redirect("/login")

			db.add_article(title,content)

			self.redirect("/admin/%s" % page)

		#删除文章
		elif m == "del_article":
			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")

			db.del_article(id)

			self.redirect("/admin/%s" % page)

		#修改文章
		elif m == "update_article":

			id = self.get_argument("id" ,"")

			title = self.get_argument("title" ,"")
			content = self.get_argument("content","")

			if id == "" or title == "" or content == "":
				self.redirect("/login")

			db.update_article(id,title,content)

			self.redirect("/admin/%s" % page)

		#删除评论
		elif m == "del_comments":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")

			db.del_comment(id)

			self.redirect("/admin/%s" % page)

		#删除留言
		elif m == "del_guests":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")

			db.del_guest(id)

			self.redirect("/admin/%s" % page)

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

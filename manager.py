#coding: utf8
import tornado.web
import db
from utils import *

# 简单的用户认证
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

	def MyRender(self,file,**args):

		args = dict(args.items()+config.functions.items())

		return self.render(file,**args)


 
# 后台管理实现
class AdminHandler(BaseHandler):

	def get(self,page):

		#校验身份
		if self.check_login() == False:
			self.redirect("/login")
			return

		#处理请求页面
		if 1==1:

			if page == "index":
				self.MyRender(admin_dir("%s.html" % page),classify = db.get_classify())

			#文章管理
			elif page == "articles":
				self.MyRender(admin_dir("%s.html" % page),articles = db.get_article())

			#更新文章
			elif page == "update":

				id = self.get_argument("id")
				self.MyRender(admin_dir("%s.html" % page),classify = db.get_classify(),article = db.get_atcbyid(id,True),id = id)

			#评论管理
			elif page == "comments":

				self.MyRender(admin_dir("%s.html" % page),comments = db.get_comments())

			#留言管理
			elif page == "guests":

				self.MyRender(admin_dir("%s.html" % page),guests = db.get_guest())

			#留言管理
			elif page == "links":

				self.MyRender(admin_dir("%s.html" % page),links = db.get_links())

			#分类管理

			elif page == "classify":

				self.MyRender(admin_dir("%s.html" % page),classify = db.get_classify())

			#返回自定义页面
			else:
				self.MyRender(admin_dir("%s.html" % page))
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
			classify = self.get_argument("classify","")

			if title == "" or content == "" or classify == "":
				self.redirect("/login")

			db.add_article(title,content,classify)

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


		#添加链接
		elif m == "add_links":

			url = self.get_argument("url" ,"")
			title = self.get_argument("title" ,"")

			if url == "" or title == "":
				self.redirect("/login")

			db.add_link(title,url)

			self.redirect("/admin/%s" % page)


		#删除链接
		elif m == "del_links":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")

			db.del_link(id)

			self.redirect("/admin/%s" % page)

		#添加分类
		elif m == "add_classify":

			name = self.get_argument("name" ,"")

			if name == "":
				self.redirect("/login")

			db.add_classify(name)

			print page

			self.redirect("/admin/%s" % page)


		#删除链接
		elif m == "del_classify":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")

			db.del_classify(id)

			self.redirect("/admin/%s" % page)


		else:
			self.redirect("/login")



 

#管理页
class LoginHandler(BaseHandler):

	def get(self):
			self.set_secure_cookie("user","")
			self.MyRender(admin_dir("login.html"))

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

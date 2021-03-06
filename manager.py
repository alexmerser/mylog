#coding: utf8
import tornado.web
import db
import json
import time
from utils import *

# 简单的用户认证
class BaseHandler(tornado.web.RequestHandler):

	def get_current_user(self):
		return self.get_secure_cookie("user")

	def get_current_pwd(self):
		return self.get_secure_cookie("pwd")

	def get_current_timelock(self):
		return self.get_secure_cookie("timelock")


	def check_login(self):
		try:
			if self.get_current_user() == C('username') and self.get_current_pwd() == C('password'):
				return check_timeout(self.get_current_timelock())
			else:
				return False
		except:
			self.set_secure_cookie("user","")
			self.set_secure_cookie("pwd","")
			self.set_secure_cookie("timelock","")

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

			#分类管理

			elif page == "upload":

				self.MyRender(admin_dir("%s.html" % page))


			#博客配置
			elif page == "options":

				self.MyRender(admin_dir("%s.html" % page),templates = os.listdir(cur_dir() + "templates"))

			#返回自定义页面
			else:
				#self.MyRender(admin_dir("%s.html" % page))
				self.redirect("/login")
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
				return

			db.add_article(title,content,classify)

			self.redirect("/admin/%s" % page)

		#删除文章
		elif m == "del_article":
			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")
				return

			db.del_article(id)

			self.redirect("/admin/%s" % page)

		#修改文章
		elif m == "update_article":

			id = self.get_argument("id" ,"")

			title = self.get_argument("title" ,"")
			content = self.get_argument("content","")

			if id == "" or title == "" or content == "":
				self.redirect("/login")
				return 

			db.update_article(id,title,content)

			self.redirect("/admin/%s" % page)

		#删除评论
		elif m == "del_comments":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")
				return 

			db.del_comment(id)

			self.redirect("/admin/%s" % page)

		#删除留言
		elif m == "del_guests":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")
				return

			db.del_guest(id)

			self.redirect("/admin/%s" % page)


		#添加链接
		elif m == "add_links":

			url = self.get_argument("url" ,"")
			title = self.get_argument("title" ,"")

			if url == "" or title == "":
				self.redirect("/login")
				return

			db.add_link(title,url)

			self.redirect("/admin/%s" % page)


		#删除链接
		elif m == "del_links":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")
				return

			db.del_link(id)

			self.redirect("/admin/%s" % page)

		#添加分类
		elif m == "add_classify":

			name = self.get_argument("name" ,"")

			if name == "":
				self.redirect("/login")
				return

			db.add_classify(name)

			print page

			self.redirect("/admin/%s" % page)


		#删除链接
		elif m == "del_classify":

			id = self.get_argument("id" ,"")

			if id == "":
				self.redirect("/login")
				return

			db.del_classify(id)

			self.redirect("/admin/%s" % page)

		#更新配置
		elif m == "update_options":

			map = {}

			map['blogname']  = self.get_argument("blogname" ,"")
			map['nickname']  = self.get_argument("nickname" ,"")
			map['email']     = self.get_argument("email" ,"")
			map['descript']  = self.get_argument("descript" ,"")
			map['pagecount'] = self.get_argument("pagecount" ,"")
			map['timeout'] = self.get_argument("timeout" ,"")

			config.update(map)

			self.redirect("/admin/%s" % page)

		#获取最近上传文件
		elif m == "get_upload":

			files = get_upload(10)

			self.write(json.dumps(files))

				#获取最近上传文件
		elif m == "del_upload":

			filename = self.get_argument('filename')

			del_upload(filename)


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
			self.set_secure_cookie("pwd", pwd)
			self.set_secure_cookie("timelock",GetNowTime())

			self.redirect("/admin/index")

		else:
			self.redirect("/login")

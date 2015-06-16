#coding: utf8
import tornado.ioloop
import tornado.web
import threading

from utils import *
import config
import module
import db
import manager
import api

#集中处理请求
class BaseHandler(tornado.web.RequestHandler):

	def MyRender(self,file,**args):


		id = self.get_argument("id",0)

		args = dict(args.items()+config.functions.items())
		args = dict(args.items()+get_filefunc(cur_dir()+"api.py").items())
		args['id'] = id

		return self.render(file,**args)

#处理网站入口
class MainHandler(BaseHandler):

	def get(self):

		self.MyRender(tmp_dir("index.html"))

#文章页
class ArticleHandler(BaseHandler):

	def get(self):

		self.MyRender(tmp_dir("article.html"))

	def post(self):

		m = self.get_argument("m","")
		id = self.get_argument("id","")
		name = self.get_argument("name","")
		mail = self.get_argument("mail","")
		url = self.get_argument("url","")
		content = self.get_argument("content","")

		if m == "add_comments":
			db.add_comment(id,name,mail,url,content)

		self.redirect("/article?id=%s" % id)

#留言页
class GuestHandler(BaseHandler):

	def get(self):

		self.MyRender(tmp_dir("guest.html"))

	def post(self):

		m = self.get_argument("m","")

		name = self.get_argument("name","")
		mail = self.get_argument("mail","")
		url = self.get_argument("url","")
		content = self.get_argument("content","")

		if m == "add_guests":
			db.add_guest(name,mail,url,content)

		self.redirect("/guest")

#归档页
class ArchivesHandler(BaseHandler):

	def get(self):

		self.MyRender(tmp_dir("archives.html"))

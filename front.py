#coding: utf8
import tornado.ioloop
import tornado.web
import threading

from utils import *
import config
import module
import db
import manager

#处理网站入口
class MainHandler(tornado.web.RequestHandler):

	def get(self,page = 0):
		
		articlelist = db.get_atcbypage(page)
			
		self.render(tmp_dir("index.html"),\
		articlelist = articlelist,
		pageid 	 = 0,
		frontpage = int(page) - 1,
		nextpage = int(page) + 1 if db.get_maxpages() > int(page) else 0)

#文章页
class ArticleHandler(tornado.web.RequestHandler):

	def get(self,id):
		id = int(id)
		self.render(tmp_dir("article.html"),\
		article = db.get_atcbyid(id),
		comments = db.get_commbyid(id),
		csize = len(db.get_commbyid(id)))

#页码页
class PageHandler(tornado.web.RequestHandler):

	def get(self,pageid):

		self.render(tmp_dir("index.html"),\
		pageid 	 = pageid,
		article = db.get_atcbyid(pageid))

#留言页
class GuestHandler(tornado.web.RequestHandler):

	def get(self):

		self.render(tmp_dir("guest.html"),guests = db.get_guest())

#归档页
class ArchivesHandler(tornado.web.RequestHandler):

	def get(self):
		archives = db.get_archives()
		self.render(tmp_dir("archives.html"),archives = archives,years = archives.keys())

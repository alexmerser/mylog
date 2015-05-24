#!/usr/bin/python
#coding : utf8
import tornado.ioloop
import tornado.web
import threading

from utils import *
import config
import module
import db
import manager

#处理404 500等异常
class BaseHandler(tornado.web.RequestHandler):

	def get(self):
		self.write_error(404)

	def write_error(self, status_code, **kwargs):
		if status_code == 404:
			self.render(tmp_dir("except/404.html"))
		elif status_code == 500:
			self.render(tmp_dir("except/500.html"))
		elif status_code == 403:
			self.render(tmp_dir("except/403.html"))
		elif status_code == 503:
			self.render(tmp_dir("except/503.html"))
		else:
			self.write('error:' + str(status_code))

#处理网站入口
class MainHandler(tornado.web.RequestHandler):

	def get(self):
		
		self.render(tmp_dir("index.html"),\
		articlelist = db.get_article(),
		pageid 	 = 0)

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

settings = {
	"static_path": cur_dir() + C('templates'),
	"cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
	"login_url": "/login",
	"xsrf_cookies": False,
	"ui_modules": module
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/guest", GuestHandler),
	(r"/archives", ArchivesHandler),
	(r"/article/([^/]*)", ArticleHandler),
	(r"/admin/hello", manager.AdminHandler),
	(r"/admin/", manager.LoginHandler),
	(r".*", BaseHandler),
], debug = True,**settings)

if __name__ == "__main__":
	
	if db.initdb(C('db_path')) == False:
		print 'Database Initialize Faild!'
		exit(0)

	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()
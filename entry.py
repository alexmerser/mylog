#!/usr/bin/python2.7
#coding: utf8
import tornado.ioloop
import tornado.web
import threading

from utils import *
import config
import module
import db
import front
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

settings = {
	"static_path": cur_dir() + C('templates'),
	"cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
	"login_url": "/login",
	"xsrf_cookies": False,
	"ui_modules": module
}

application = tornado.web.Application([
	(r"/", 						front.MainHandler),
	(r"/page/([^/]*)", 			front.MainHandler),
	(r"/guest", 				front.GuestHandler),
	(r"/archives", 				front.ArchivesHandler),
	(r"/article/([^/]*)", 		front.ArticleHandler),
	(r"/login", 				manager.LoginHandler),
	(r"/admin/([^/]*)", 		manager.AdminHandler),
	(r".*", 					BaseHandler),
], debug = True,**settings)

if __name__ == "__main__":
	
	if db.initdb() == False:
		print 'Database Initialize Faild!'
		exit(0)

	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()
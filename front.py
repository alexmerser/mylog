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
			
		for i in range(0,len(articlelist)):
			articlelist[i][3] = articlelist[i][3].split(' ')[0]

		self.render(tmp_dir("index.html"),\
		articlelist = articlelist,
		pageid 	 = 0,
		frontpage = int(page) - 1,
		nextpage = int(page) + 1 if db.get_maxpages() > int(page) else 0)

#文章页
class ArticleHandler(tornado.web.RequestHandler):

	def get(self,id):
		id = int(id)

		article = db.get_atcbyid(id)

		article[3] = article[3].split(' ')[0]

		self.render(tmp_dir("article.html"),\
		article = article,
		comments = db.get_commbyid(id),
		csize = len(db.get_commbyid(id)))

#留言页
class GuestHandler(tornado.web.RequestHandler):

	def get(self):

		self.render(tmp_dir("guest.html"),guests = db.get_guest())

#归档页
class ArchivesHandler(tornado.web.RequestHandler):

	def get(self):

		archives = db.get_archives()
		years = archives.keys()
		for year in years:

			for i in range(0,len(archives[year])):
				archives[year][i][3] = archives[year][i][3].split(' ')[0]

		self.render(tmp_dir("archives.html"),archives = archives,years = years)

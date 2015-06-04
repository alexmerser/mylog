#coding : utf8
import sqlite3
import time
from utils import *

g_article  = {}
g_comment  = {}
g_guest = []
g_link = []

#获得归档列表
def get_archives():

	archives = {}

	for key in g_article.keys():

		it = g_article[key]

		date = it[3]

		date = date.split("-")

		if archives.has_key(date[0]):
			archives[date[0]].append(it)
		else:
			archives[date[0]] = [it]


	archives.keys().sort()
	return archives


#获取所有文章
def get_article():
	articles = g_article.values()
	articles.sort(key = lambda x : x[0],reverse = True)

	#将元组转为列表，并切分文章内容
	for i in range(0,len(articles)):
		articles[i] = list(articles[i])
		articles[i][2] = articles[i][2].split(C('split_sign'))

	return articles

#得到最大页数 
def get_maxpages():
	return len(g_article) / C("pagecount")


#按页数获取文章
def get_atcbypage(pageid):

	articles = get_article()

	pageid = int(pageid)

	if pageid == 0:
		begin = 0
	else:
		begin = ( pageid ) * C("pagecount")

	end = (pageid + 1) * C("pagecount")

	if end > len(articles) - 1:
		end = len(articles)

	if begin > len(articles) - 1:
		return []

	articles = articles[begin:end]

	return articles


#添加文章
def add_article(title,content):

	date = GetNowTime() 

	db = connectdb()

	content = Space2Char(content)

	sql = 'insert into article values(null,"%s","%s","%s",0)' % (title,content,date)
	db.execute(sql)
	db.commit()

	closedb(db)

	init_article()

#更新文章
def update_article(id,title,content):

	date = GetNowTime() 

	db = connectdb()

	content = Space2Char(content)

	sql = 'update article set title="%s",content="%s" where id=%s' % (title,content,id)

	db.execute(sql)
	db.commit()

	closedb(db)

	init_article()

#删除文章
def del_article(id):

	db = connectdb()

	sql = 'delete from article where id=%s' % id

	db.execute(sql)
	db.commit()

	closedb(db)

	init_article()

#通过id获得文章
def get_atcbyid(id,isEdit = False):

	#将元组转为列表，合并文章内容
	atc = g_article[int(id)]

	if isEdit == False:
		atc[2] = atc[2].replace(C('split_sign'),"")

	return atc

#从id获得评论
def get_commbyid(id):
	
	if g_comment.has_key(int(id)):
		return g_comment[int(id)]
	else:
		return []

#获取所有留言
def get_comments():

	comments = []

	if len(g_comment) > 0:

		tmp = g_comment.values()[0]
		for it in tmp:
			comments.append(list(it))

	return comments

#添加评论
def add_comment(pid,name,mail,url,content):

	db = connectdb()
	date = GetNowTime() 
	sql = 'insert into comment values("%s",null,"%s","%s","%s","%s","%s")' % (pid,name,mail,url,content,date)

	db.execute(sql)
	db.commit()

	closedb(db)

	init_guest()

#删除评论
def del_comment(id):

	db = connectdb()

	sql = 'delete from comment where id=%s' % id

	db.execute(sql)
	db.commit()

	closedb(db)

	init_comment()

#获得留言
def get_guest():

	return g_guest

#添加留言
def add_guest(name,mail,url,content):

	db = connectdb()
	date = GetNowTime() 
	sql = 'insert into guest values(null,"%s","%s","%s","%s","%s")' % (name,mail,url,content,date)

	db.execute(sql)
	db.commit()

	closedb(db)

	init_guest()

#删除留言
def del_guest(id):

	db = connectdb()

	sql = 'delete from guest where id=%s' % id

	db.execute(sql)
	db.commit()

	closedb(db)

	init_guest()

#获取链接
def get_links():
	return g_link

#添加链接
def add_link(title,url):

	db = connectdb()

	sql = 'insert into link values(null,%s,%s)' % (title,url)

	db.execute(sql)
	db.commit()

	closedb(db)

	init_link()


#删除链接
def del_link(id):

	db = connectdb()

	sql = 'delete from link where id=%s' % id

	db.execute(sql)
	db.commit()

	closedb(db)

	init_link()



#数据库初始化相关
def init_article():

	global g_article
	
	db = connectdb()

	g_article = {}

	result = db.execute("select * from article")
	for row in result:

		row = list(row)
		row[2] = Char2Space(row[2])
		g_article[int(row[0])] = row

	closedb(db)

#初始化评论
def init_comment():

	global g_comment
	
	db = connectdb()

	g_comment = {}

	result = db.execute("select * from comment")

	for row in result:
		if g_comment.has_key(int(row[0])):
			g_comment[int(row[0])].append(row)
		else:
			g_comment[int(row[0])] = [row]

	closedb(db)

#初始化留言
def init_guest():

	global g_guest
	
	db = connectdb()

	g_guest = []

	result = db.execute("select * from guest")

	for row in result:
		g_guest.append(row)
	
	closedb(db)


#初始化留言
def init_link():

	global g_link
	
	db = connectdb()

	g_link = []

	result = db.execute("select * from link")

	for row in result:
		g_link.append(row)
	
	closedb(db)

#打开和关闭数据库链接
def connectdb():
	
	return sqlite3.connect(cur_dir()+C("db_path"))
	
def closedb(db):
	
	db.close()

#初始化数据库
def initdb():

	try:
		init_article()
		init_comment()
		init_guest()
		init_link()

		return True
	except:
		return False


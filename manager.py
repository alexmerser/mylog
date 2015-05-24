#coding: utf8
import tornado.web
from utils import *

# 简单的用户认证实现
 
# BaseHandler 基类覆写 get_current_user
# 覆写后 RequestHandler 的current_user成员会有值(稍后解释实现源码)
# 这里简单地判断请求带的 secure cookie 是否带有 user属性的值
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
    	return self.get_secure_cookie("user")

    def check_login(self):
        if not self.current_user:
            return False
        else:
            return True

 
# 实际业务类实现
class AdminHandler(BaseHandler):
	def get(self):
		if self.check_login() == False:
			self.redirect("/admin")
			return

		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("Hello, " + name)
 

#管理页
class LoginHandler(BaseHandler):

    def get(self):
            self.render(tmp_dir("login.html"))

    def post(self):
		self.set_secure_cookie("user", self.get_argument("user"))
		self.redirect("/admin/hello")
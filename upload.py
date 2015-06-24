#coding: utf8

import tornado.ioloop
import tornado.web
import os
from utils import *

class UploadFileHandler(tornado.web.RequestHandler):

	def get(self,file = ""):

		if file == "":
			self.redirect("/")

		#Content-Type这里我写的时候是固定的了，也可以根据实际情况传值进来
		self.set_header ('Content-Type', 'application/octet-stream')
		self.set_header ('Content-Disposition', 'attachment; filename='+file)

		#读取的模式需要根据实际情况进行修改
		with open(cur_dir() + C('upload')+file, 'rb') as f:
			while True:
				data = f.read(1000)
				if not data:
					break
				self.write(data)

		#记得有finish哦
		self.finish()

	def post(self,file = ""):

		print 123

		upload_path = cur_dir() + C('upload')  

		#提取表单中‘name’为‘file’的文件元数据
		file_metas=self.request.files['file']	
		for meta in file_metas:

			filename=meta['filename']
			filepath=os.path.join(upload_path,filename)

			#有些文件需要已二进制的形式存储，实际中可以更改
			with open(filepath,'wb') as up:	  
				up.write(meta['body'])

			self.write('finished!')
前端设计手册
===

目录结构
---
Templates

	├─css             (存放样式文件)
	├─except          (存放HTTP异常页面)
	├─images          (存放静态图片)
	├─js              (存放JS脚本)
	├─archives.html   (存档页面)
	├─article.html    (文章页面)
	├─guest.html      (留言页面)
	├─index.html      (首页/文章列表页)
	├─footer.html     (底部模板)
	├─header.html     (头部模板)
	└─favicon.ico     (网站图标)

约定
---
**1.获取静态页面**

如引用js、css、jpg等文件，使用模板`{{ static_url(path) }}`来转换为静态路径，如下代码

	<link type="text/css" rel="stylesheet" href="css/style.css" />

应该表示为

	<link type="text/css" rel="stylesheet" href="{{ static_url("css/style.css") }}" />

**2.页面模板**

为避免代码重写，提供头部和底部两个模块对象。使用如下代码引用。

	{% module Header() %}
	{% module Footer() %}

该模块引用功能为将读取footer.html和header.html到页面引用位置。

**3.HTTP异常页面**

现提供403、404、500和503异常的处理页面。例如404页面，命名为[ 404.html ]放置在except目录下即可。

**4.变量引用方法**

每个模板页将提供相关功能变量在前端引用。如 [ article.html ] 页面，提供表示文章内容的数组变量[ article ]，在前端页面中引用方法为。

	<div class="article">{{ article[1] }}</div>

变量类型和python的数据类型一致，一般为变量、列表、字典三种。后文中变量说明将以如下格式表示。

	变量名[类型]
	{
		说明
		使用方法
	}

例如index.html提供的pageid当前页ID变量。描述为

	pageid[整数]
	{
		当前页ID变量

		<a>当前页数 ：{{ pageid }}</a>
	}

模板变量
---
**index.html**

	articles[二维列表]
	{
		文章列表，一级列表为文章，二级列表为文章内容

		{% for it in articles %}
			文章ID{% raw it[0] %}</br>
			文章标题{% raw it[1] %}</br>
			文章内容{% raw it[2] %}</br>
			发表时间{% raw it[3] %}</br>
		{% end %}
	}

	pageid[整数]
	{
		当前页ID变量

		<a>当前页数 ：{{ pageid }}</a>
	}

	frontpage[整数]
	{
		上一页ID

		{% if frontpage >= 0 %}
			<a href="/page/{{ frontpage }}">上一页</a>
		{% end %}
	}

	nextpage[整数]
	{
		下一页ID

		{% if nextpage > 0 %}
			<a href="/page/{{ nextpage }}">下一页</a>
		{% end %}
	}

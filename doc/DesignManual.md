前端设计手册
===

<ul>
<li>
	<a href="#结构">结构</a>
	<ul>
		<li><a href="#1文件">1.文件</a></li>
		<li><a href="#2路由">2.路由</a></li>
	</ul>
</li>
<li>
	<a href="#约定">约定</a>
	<ul>
		<li><a href="#1获取静态文件">1.获取静态文件</a></li>
		<li><a href="#2页面模板">2.页面模板</a></li>
		<li><a href="#3HTTP异常页面">3.HTTP异常页面</a></li>
		<li><a href="#4内置函数使用方法">4.内置函数使用方法</a></li>
		<li><a href="#5获取配置信息">5.获取配置信息</a></li>
	</ul>
</li>
<li>
	<a href="#函数">函数</a>
	<ul>
		<li><a href="#get_atcbypage">get_atcbypage</a></li>
		<li><a href="#get_atcbyid">get_atcbyid</a></li>
		<li><a href="#get_guest">get_guest</a></li>
		<li><a href="#get_years">get_years</a></li>
		<li><a href="#get_commbyid">get_commbyid</a></li>
		<li><a href="#get_maxpages">get_maxpages</a></li>
		<li><a href="#get_frontpage">get_frontpage</a></li>
		<li><a href="#get_nextpage">get_nextpage</a></li>
	</ul>
</li>
<li>
	<a href="#接口">接口</a>
	<ul>
		<li><a href="#1提交评论">1.提交评论</a></li>
		<li><a href="#2提交留言">2.提交留言</a></li>
	</ul>
</li>
</ul>

结构
---

###1.文件###

模板存放在templates目录下，以模板名保存的目录当中，可以存放多个模板，在后台-》系统配置中可以设置使用哪一个模板。

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

###2.路由###

请求URL和页面之间的对应关系如下。

	"/", 				-》	index.html
	"/page", 			-》	index.html
	"/guest", 			-》	guest.html
	"/archives", 		-》	archives.html
	"/article", 		-》	article.html


约定
---
###1.获取静态文件###

如引用js、css、jpg等文件，使用模板`{{ template_url(path) }}`来转换为静态路径，如下代码

	<link type="text/css" rel="stylesheet" href="css/style.css" />

应该表示为

	<link type="text/css" rel="stylesheet" href="{{ template_url("css/style.css") }}" />

###2.页面模板###

为避免代码重写，提供头部和底部两个模块对象。使用如下代码引用。

	{% module Header() %}
	{% module Footer() %}

该模块引用功能为将读取footer.html和header.html到页面引用位置。

###3.HTTP异常页面###

现提供403、404、500和503异常的处理页面。例如404页面，命名为[ 404.html ]放置在except目录下即可。

###4.内置函数使用方法###

模板将提供相关获取数据的功能函数在前端引用。如在[ article.html ] 页面，需要获取文章内容，则可以使用[ get_atcbyid ],函数来完成，在前端页面中使用方法为。

		{% for it in get_atcbyid(id) %}
			文章ID{% raw it[0] %}</br>
			文章标题{% raw it[1] %}</br>
			文章内容{% raw it[2] %}</br>
			发表时间{% raw it[3] %}</br>
		{% end %}

变量类型和python的数据类型一致，一般为变量、列表、字典三种。使用方法可惨遭Tornado模板使用方法。

###5.获取配置信息###

内置了函数C，可以来博客获取配置信息。以获取博客名称举例，调用方法为`{{ C("blogname") }}`。
其他配置信息描述如下

	blogname =》  博客名称
	nickname =》  作者名称
	email    =》  作者邮件
	descript =》  博客描述


内置函数
---
###get_atcbypage###

	描述：通过页数得到文章列表
	参数：页数ID
	原形：get_atcbypage(id)
	返回：返回一个列表，每个子项为一个列表，按序依次为ID，标题，内容，时间，分类ID

###get_atcbyid###

	描述：通过文章ID得到文章
	参数：文章ID
	原形：get_atcbyid(id)
	返回：返回一个列表，包含文章内容，按序依次为ID，标题，内容，时间，分类ID

###get_guest###

	描述：得到全部留言
	原形：get_guest()
	返回：返回一个列表，每个子项为一个列表，按次序为ID，昵称，邮件，URL，内容，时间

###get_years###

	描述：得到存档年限
	原形：get_years()
	返回：返回一个列表，依序为已有文章年数。

###get_commbyid###

	描述：通过ID得到评论
	原形：get_commbyid(id)
	参数：评论ID
	返回：返回一个列表，按次序为ID，昵称，邮件，URL，内容，时间

###get_maxpages###

	描述：得到最大页数
	原形：get_maxpages()
	返回：整数，最大页数

###get_frontpage###

	功能：得到上一页页数
	参数：当前页数
	原形：get_frontpage(id)
	返回：整数，上一页页数

###get_nextpage###

	功能：得到下一页页数
	参数：当前页数
	原形：get_nextpage(id)
	返回：整数，下一页页数

接口
---

###1.提交评论###

	URL: /article?id={{ 文章id }}
	类型: POST
	参数:
		m         -> "add_comments"
		id        -> 文章ID
		name      -> 昵称
		mail      -> 邮件
		url       -> url
		content   -> 内容

###2.提交留言###

	URL: /guest
	类型: POST
	参数:
		m         -> "add_guests"
		name      -> 昵称
		mail      -> 邮件
		url       -> url
		content   -> 内容


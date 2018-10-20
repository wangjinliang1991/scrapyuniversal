# 通用爬虫

## 以中华网为例

### 目标：抓取新闻列表的所有分页的新闻详情，包括标题、正文、时间、来源等信息

### 项目梳理

* 新建项目、创建Spider
> CrawlSpider,scrapy提供的通用Spider,命令
```scrapy genspider -t crawl china tech.china.com```
Spider内容多了rules属性的定义,Rule管理爬取规则，包含提取和跟进页面的设置，第一个参数是LinkExtractor,默认回调函数不是parse,
而是parse_item

* 定义Rule,实现解析函数 
> 先将start_urls修改为起始链接，然后Spider开始爬取start_urls的每一个链接，得到Response之后，Spider根据Rule提取
页面内的超链接，去生成进一步的Request

> 起始为新闻列表页，下一步提取每条新闻的详情页的链接 链接都在class为con_item的div节点里，用LinkExtractor的
restrict_xpaths属性指定，Spider从该区域提取所有超链接生成Request,但是每篇文章的导航中有其他的超链接标签，真正的
超链接路径以article开头，用正则匹配赋值给allow参数，对应页面就是详情页，是需要解析的，callback到parse_item  

> 另外要让当前页面分页功能，提取下一页的链接，在ID为pageStyle的节点内，直接用LinkExtractor的restrict_xpaths属性
指定提取的链接，不用提取页面详情信息，不需要callback，下一页如果匹配成功，要像上述情况分析，加一个follow参数True
，代表继续跟进匹配分析，follow可以不加，默认

> 实现页面翻页和详情页的抓取了

* 解析页面
> 先定义Item,字段包括新闻标题、链接、正文、发布时间、来源、站点名称，站点名称赋值中华网，通用爬虫，所以需要字段区别站点名

> 如果和之前一样提取内容，调用response变量的xpath()等方法即可，parse_item()实现，把每条新闻信息提取成一个NewsItem对象

> 这种提取方式不规整，对Item的提取，用模块Item Loader,通过add_xpath()\add_css()\add_value()等方式实现配置化提取，改写
parse_item() 定义ItemLoader的子类，名为ChinaLoader  ChinaLoader继承了Newsloader类， 定义通用的Out Porcessor为TakeFirst,
相当于之前定义的extract_first()方法的功能，返回第一个非空值  ChinaLoader中定义text_out和source_out字段，使用
Compose Porcessor，是用给定的多个函数组合构造的Processor,有两个参数，Join也是一个Processor可以把列表拼合成一个字符串，
第二个参数为匿名参数，将字符串的头尾空白字符去掉，从而将列表形式的提取结果转化为去除头尾空白的字符串 

* 通用配置抽取
> 如果扩展其他站点，仍需要创建新的CrawlSpider，定义站点的Rule，单独实现parse_item()方法。许多代码是重复的，如
CrawkSpider的变量、方法名几乎一样，可以新建通用Spider，将name\allowed_domains等抽取，在Spider初始化时赋值即可
命令```scrapy genspidet -t crawl universal universal```将之前Spide内的属性抽离配置成Json,名为china.josn,放到
configs文件夹，和spiders文件夹并列

> json代码说明：第一个字段spider为Spider的名称，universal，后面是站点描述，站点名、类型、首页等，随后的settings是
该Spider特有的settings配置，随后是spider的一些属性，start_urls、allowed_domains、rules等，rules也可单独定义为rules.py
做成配置文件，实现Rule的分离

> 启动爬虫，需要从该配置文件中读取动态加载到Spider，需要定义读取JSON文件的方法get_config()到utils文件中

> 定义入口文件run.py，放到根目录下，启动Spider 运行入口run(),先获取命令行的参数赋值为name，就是JSON文件的名称，也就是要
爬取网站的名称，先利用get_config()方法传入该名称读取刚才定义的配置文件，获取爬取使用的spider的名称、配置文件中的
settings配置，再把获取的settings配置和项目全局的settings配置合并，新建CrawlerProcess传入爬取使用的配置，调用
crawl()和start()方法启动爬取

> 在universal中，新建__init__方法初始化配置，赋值start_urls,allowed_domains,rules等属性，rules属性另外读取rules.py配置
实现基础配置，再讲剩下的解析部分也配置抽离出来，变量包括Item Loader类的选用、Item类的选用、Item Loader方法参数的定义

> 配置JSON文件中，class和loader属性分别代表Item和Item Loader所用的类，定义attrs属性定义每个字段的提取规则，如
title定义的每一项都有method属性，代表使用的提取方法，xpath代表调用Item Loader的add_xpath()方法，args即参数，add_xpath()
的第二个参数，即xpath表达式，针对datetime,还用了一次正则，定义re参数传递正则

> 最后，是加载配置到parse_item()方法，首先获取item的配置信息，然后获取class的配置，初始化Item Loader，遍历Item
的各个属性依次提取，判断method字段，调用对应处理方法

> 此外，start_urls的配置，某些情况，也需要动态配置，一种直接配置URL列表，一种调用方法生成，如果动态生成，调用方法传参数

   

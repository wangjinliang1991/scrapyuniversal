from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, Join

# ChinaLoader继承了Newsloader类， 定义通用的Out Porcessor为TakeFirst,相当于之前定义的extract_first()方法的功能
class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

# 定义text_out和source_out字段，使用Compose Porcessor，有两个参数，Join也是一个Processor可以把列表拼合成一个字符串，第二个参数
# 为匿名参数，将字符串的头尾空白字符去掉，从而将列表形式的提取结果转化为去除头尾空白的字符串
class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
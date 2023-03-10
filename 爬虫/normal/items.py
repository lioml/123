# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class biliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=scrapy.Field()#游戏id
    name=scrapy.Field()#游戏名
    type=scrapy.Field()#游戏类型
    tag=scrapy.Field()

class bgradeItem(scrapy.Item):
    id=scrapy.Field()#游戏id
    comment_number=scrapy.Field()#评论人数，同时也是评价人数
    grade=scrapy.Field()#评分
    star_num_list=scrapy.Field()#各评分人数
    tag=scrapy.Field()

class taptapItem(scrapy.Item):
    id=scrapy.Field()#游戏id
    name=scrapy.Field()#游戏名
    type=scrapy.Field()#游戏类型
    comment_number=scrapy.Field()#评论人数，同时也是评价人数
    grade=scrapy.Field()#评分
    star_num_list=scrapy.Field()#各评分人数
    downloads=scrapy.Field()#下载量
    fans_count=scrapy.Field()#关注量
import scrapy
import json
import logging
from normal.items import biliItem
from normal.items import bgradeItem
logger = logging.getLogger(__name__)

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # allowed_domains = ['www.bilibili.com']
    # num1 = [x for x in range(0, 300)]#爬取网站的id
    # num2 = [x for x in range(100000, 110000)]
    with open('bili.txt','r') as f:
        bili_list=f.read().split(',')
    start_urls = bili_list
    crawl_gid=set(start_urls)
    finish_id=set()
    def start_requests(self):
        while 1:
            bid=self.crawl_gid.pop()#从crawl_gid中取出一个值
            self.finish_id.add(bid)#加入到finish_id中
            bid=str(bid)
            url_bgame="https://line1-h5-pc-api.biligame.com/game/detail/content?game_base_id={}".format(bid)#游戏名和游戏类型
            url_bgrade="https://line1-h5-pc-api.biligame.com/game/comment/summary?game_base_id={}".format(bid)#游戏评分
            yield scrapy.Request(url_bgame,callback=self.parse0,meta={'id':bid,'tag':0})
            yield scrapy.Request(url_bgrade,callback=self.parse1,meta={'id':bid,'tag':1})


    def parse0(self, response):
        JsToPy=json.loads(response.text)
        try:
            if JsToPy["code"]==0:#有数据
                items=biliItem()
                items['id']=response.meta['id']
                items['tag']=response.meta['tag']
                items['name']=JsToPy['data']['title']
                type_list = []
                for num in range(len(JsToPy['data']['tag_list'])):  # 游戏类型
                    type = JsToPy['data']['tag_list'][num]['name']
                    type_list.append(type)
                items['type']=type_list
                # print('parse0', items['id'])
                yield items
            else:
                pass
        except Exception as e:
            logger.warning(e)
            pass

    def parse1(self,response):
        JsToPy0=json.loads(response.text)
        try:
            if JsToPy0['code']==0 and JsToPy0['data']['comment_number'] > 50:
                dic=bgradeItem()
                dic['id']=response.meta['id']
                dic['tag'] = response.meta['tag']
                dic['comment_number']=JsToPy0['data']['comment_number']  # 评价人数
                dic['grade']=JsToPy0['data']['grade']  # 评分
                dic['star_num_list']=JsToPy0['data']['star_number_list']
                # print('parse1', dic['id'])
                yield dic
            else:
                pass
        except Exception as e:
            logger.warning(e)
            pass



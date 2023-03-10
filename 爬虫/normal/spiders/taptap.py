import scrapy
from selenium import webdriver
import json
from normal.items import taptapItem

chrome_options = webdriver.ChromeOptions()
# 提前进行一些设置，避免遇到奇怪的bug
chrome_options.add_argument("--window-size=1920,1080")  # 窗口大小
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--headless')  # 启动无头模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 关闭Chrome浏览器弹出的自动化测试横条

class TaptapSpider(scrapy.Spider):
    name = 'taptap'
    # allowed_domains = ['www.taptap.com']

    def __init__(self):
        with open('taptap.txt', 'r') as f:
            taptap_list = f.read().split(',')
        self.start_urls = taptap_list

        self.driver = webdriver.Chrome('F:\Chrome下载\chromedriver', options=chrome_options)
        with open('F:\\学习用\\毕设用\\18210120610_李兆宗_毕设\\stealth.min.js-main\\stealth.min.js') as f:
            js = f.read()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {  # 加载js文件，用于掩盖使用seleium的痕迹
            "source": js
        })
        super().__init__()

    def start_requests(self):
        for tid in self.start_urls:
            tid=str(tid)
            url_tgame='https://www.taptap.com/webapiv2/app/v2/detail-by-id/{}?' \
            'X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D68%26VN%3D0.1.0' \
            '%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26DT%3DPC%26OS%3DWindows%26OSV%3D10'.format(tid)#游戏名和游戏类型
            yield scrapy.Request(url_tgame,callback=self.parse,meta={'id':tid})
        self.driver.quit()



    def parse(self, response):
        try:
            JsToPy=json.loads(response.text)
            if JsToPy['success'] != False and JsToPy['data']['stat']['fans_count']>500:
                item=taptapItem()
                item['id']=JsToPy['data']['id']
                item['name']=JsToPy['data']['title']
                item['fans_count'] = JsToPy['data']['stat']['fans_count']  # 关注量
                item['grade'] = JsToPy['data']['stat']['rating']['score']
                type_list=[]
                for i in range(len(JsToPy['data']['tags'])):
                    type_list.append(JsToPy['data']['tags'][i]['value'])# 标签
                item['type']=type_list
                star_num_list=[]
                try:
                    for num in range(len(JsToPy['data']['stat']['vote_info'])):
                        star_num_list.append(JsToPy['data']['stat']['vote_info'][str(num+1)])
                        item['star_num_list'] =star_num_list # 各等级评分人数
                except:
                    item['star_num_list']=0
                item['downloads'] =JsToPy['data']['stat']['hits_total'] # 下载量
                item['comment_number'] =JsToPy['data']['stat']['review_count']# 评论人数
                # print('success',item['id'])
                yield item
            else:
                pass
        except Exception as e:
            print(e)
            pass

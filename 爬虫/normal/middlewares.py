# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import random
from scrapy.http import HtmlResponse
import selenium.webdriver.support.ui as ui
class RandomUserAgentMiddleware:

    def process_request(self, request, spider):
        random_ua=random.choice(spider.settings.get('USER_AGENT_LIST'))
        request.headers["User-Agent"]=random_ua


class ProxyMiddleware(object):
        # 写两个列表 原因是代理IP的类型中有 http 和 https两种类型
        # 可被选用的代理IP
    PROXY_http = [
            '153.180.102.104:80',
            '195.208.131.189:56055',
    ]
    PROXY_https = [
            '120.83.49.90:9000',
            '95.189.112.214:35508',
    ]
        # 拦截所有的异常请求

    def process_exception(self, request, exception, spider):
        # 这一步是必须要用的 因为当你访问一个网站次数过多的时候  你可以使用代理IP继续爬取该网站的数据
        ## #使用代理池进行请求代理ip的设置
        # request.url 返回的是请求对象所对应的URL
        print('process_exception')
        if request.url.split(':')[0] == 'http':
            request.meta['proxy'] = random.choice(self.PROXY_http)
        else:
            request.meta['proxy'] = random.choice(self.PROXY_https)

class SeleiumDownloaderMiddleware:

    def process_request(self, request, spider):
            spider.driver.get(url=request.url)
            button = spider.driver.find_element_by_id('nc_1_n1z')  # 找到要拖动的按钮
            action = ActionChains(spider.driver)  # 实例化一个action对象
            action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
            a = []#随机生成一些滑动列表
            c = 300
            for i in range(random.choice([3, 4])):
                b = random.uniform(50, 100)
                c = c - b
                a.append(b)
            if c > 0:
                a.append(c)
            for x in a:
                action.move_by_offset(x, 0)
            action.release().perform()

            time.sleep(0.5)  # 暂停1-2秒
            # self.driver.save_screenshot('123.jpg')
            content = str(spider.driver.page_source).replace(
                '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
                '')  # 将获取到的源码整理后能被json.load识别
            content = content.replace('</pre></body></html>', '')
            url=spider.driver.current_url
            # url_list=url.split('70253')
            # request.meta['url_list']=url_list

            return HtmlResponse(url=request.url,body=content,request=request,encoding='utf-8')

class NormalSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NormalDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

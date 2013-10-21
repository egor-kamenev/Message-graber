# -*- coding: utf-8 -*-
from diesel_spider import DieselSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
from diesel.diesel.items import MessageItem, FileItem
from scrapy.exceptions import CloseSpider
from MessageCollector.models import MessageReserve
import re
import datetime



class ParseSpider(DieselSpider):
    name = "parse"

    allowed_domains = ["diesel.elcat.kg"]


    xpath_templates = {
        'message_link':   '//a[contains(@href,"index.php?act=Msg&CODE=03&VID=in&MSID=")]/@href',
        'message_title':  '//div[@class="subtitle"]/text()',
        'message_sender': '//span[@class="normalname"]/a/text()',
        'message_date':   '//span[@class="postdetails"]/text()',
        'message_text':   '//td[@class="post1"]/descendant-or-self::text()',
        'delete_message': '//a[contains(@href,"CODE=05")]/@href',
        'attach_files':   '//a[contains(@href,"index.php?act=attach")]/@href',
        'images_files':   '//div[@class="postcolor"]/descendant-or-self::img[not(contains(@src,".gif"))]/@src',
    }


    # Собираем ссылки на сообщения
    def parse(self):


        max_diesel_massages = 100
        messages_per_page = 100


        for page in range(0,max_diesel_massages,messages_per_page):
            yield  Request(url= self.urls['messages_url'] % (page), callback=self.parsePage)



    def parsePage(self, response):

        if u'Inbox'.encode('cp1251') in response.body:

            x = HtmlXPathSelector(response)

            for messageLink in x.select(self.xpath_templates['message_link']):
                # резервируем id для сообщения, и передаем его по цепочке вызовов,
                # для того что бы иметь возможность свзязать файлы с сообщением
                item = MessageItem()
                item['source_user_pk'] = self.source_user_pk
                item['message_reserve'] = MessageReserve.objects.create()
                item['forum_id'] = int(messageLink.re(r'MSID=(\d+)')[0])

                yield  Request(url=messageLink.extract(), callback=self.processMessage, meta={'item':item})

        else:
            log.msg('Ошибка перехода в сообщения', level= log.ERROR)
            raise CloseSpider(reason='Ошибка перехода в сообщения')


    # получаем текст письма
    def processMessage(self, response):


        yield self.processMessageTextData(response, response.meta['item'])

#        images =  self.processMessageImages(response, response.meta['item']['message_reserve'])
#        for image in images:
#            yield image

        files = self.processMessageFiles(response,response.meta['item']['message_reserve'])
        for file in files:
            yield file


    def processMessageFiles(self, response, message_reserve):
        x = HtmlXPathSelector(response)
        attached_files = self.getFields(self.xpath_templates['attach_files'],x)

        for fileURL in attached_files:
            yield Request(url=fileURL.extract(), meta={'message_reserve':message_reserve}, callback=self.getFile)


    def processMessageImages(self, response, message_reserve):

        x = HtmlXPathSelector(response)

        attached_images = self.getFields(self.xpath_templates['images_files'],x)
        for fileURL in attached_images:
            yield  Request(url=fileURL.extract(), meta={'message_reserve':message_reserve}, callback=self.getImage)



    def processMessageTextData(self,response, item):


        x = HtmlXPathSelector(response)

#        item['title'] = self.getField(self.xpath_templates['message_title'], x)
        item['sender']= self.getField(self.xpath_templates['message_sender'], x)
        item['date']= datetime.datetime.now()
        item['text']= self.collectField(self.xpath_templates['message_text'], x)

        return item



    def getImage(self,response):

        item = FileItem()
        item['bin_content'] = response.body
        item['message_reserve'] = response.meta['message_reserve']
        item['type'] = 'image'

        return item


    def getFile(self, response):
        #inspect_response(response)


        item = FileItem()
#        item['name'] = 'test'
        item['name'] = (re.search('filename="(.+)"', response.headers['Content-Disposition']).group(1)).decode('cp1251')
        item['message_reserve'] = response.meta['message_reserve']
        item['bin_content'] = response.body
        item['type'] = 'file'

        return item


    def collectField(self, xpath, x):

        result = ''

        try:
            # если такого xpath нет, то возвращаем пустую строку
            for text in x.select(xpath).extract():
                result+= text + " "
        except Exception as ex:
            log.msg("Ошибка получения поля : %s" %(xpath) , level=log.ERROR)
            raise ex

        return result

    def getField(self, xpath, x):

        try:
            # если такого xpath нет, то возвращаем пустую строку
            result = x.select(xpath)[0].extract()
        except (IndexError, ValueError) as ex:
            log.msg("Ошибка получения поля : %s" %(xpath) , level=log.ERROR)
            raise ex

        return result


    def getFields(self, xpath, x):

        try:
            result = x.select(xpath)
        except Exception as ex:
            log.msg("Ошибка получения поля : %s" %(xpath) , level=log.ERROR)
            raise ex

        return result

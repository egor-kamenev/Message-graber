# -*- coding: utf-8 -*-
from scrapy.http import FormRequest, Request
from delete_spider import DieselSpider
from diesel.diesel.items import PostedItem
from scrapy import log
from scrapy.shell import inspect_response


class SendSpider(DieselSpider):
    name = "send"
    allowed_domains = ["diesel.elcat.kg"]

    def __init__(self, login, password, companion_name, msg_text, message_reserve_id, **kwargs):

        super(SendSpider,self).__init__(login,password, **kwargs)

        self.message_reserve_id = int(message_reserve_id)

        self.urls['send_page'] = 'http://diesel.elcat.kg/index.php?act=Msg&CODE=04'

        self.msg_info= {
            'companion_name': companion_name,
            'msg_text': msg_text
        }



    def parse(self):
        return [Request(url=self.urls['send_page'], callback=self.posting)]




    def posting(self,response):
        return [FormRequest.from_response(
            response,
            formname='REPLIER',
            formdata={
                'entered_name': self.msg_info['companion_name'],
                'msg_title':self.msg_info['msg_text'][:30]+'...' ,
                'Post':self.msg_info['msg_text']
            },
            meta={'dont_redirect': False},
            callback=self.posted
        )]



    def posted(self,response):
        item = PostedItem()
        item['message_reserve'] = self.message_reserve_id


        if u'успешно'.encode('cp1251') in response.body:
            log.msg(message='Сообщение успешно отправлено', logLevel=log.INFO)
            item['posted'] = True

        else:
            log.msg(message='Ошибка отправки сообщения', logLevel=log.ERROR)
            item['posted'] = False


        return item



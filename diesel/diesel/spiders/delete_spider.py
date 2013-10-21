# -*- coding: utf-8 -*-
from diesel_spider import DieselSpider
from diesel.diesel.items import DeletedItem
from scrapy import log
from scrapy.http import Request
import cx_Oracle

class DeleteSpider(DieselSpider):
    name = "delete"

    urls = {
        'login_page_url' : "https://diesel.elcat.kg/index.php?act=Login&CODE=01&CookieDate=1",
        'message_delete_url': 'http://diesel.elcat.kg/index.php?CODE=05&act=Msg&MSID=%d&VID=in'
        }

    xpath_templates = {
        'message_delete': '//a[contains(@href,"CODE=05")]/@href'
    }

    db = cx_Oracle.connect("%s/%s@%s:1521/%s" % ('egor','Fhes#4','192.168.10.252','billing'))

    def __init__(self, login, password, forum_id, **kwargs):
        super(DeleteSpider, self).__init__(login, password, **kwargs)
        self.forum_id = int(forum_id) # id сообщения на форуме которое следует удалить


    def parse(self):
        try:
            return Request(url=self.urls['message_delete_url'] % (self.forum_id), callback=self.deleted)
        except Exception as ex:
            log.msg("Ошибка удаления %d" %(self.forum_id), level=log.ERROR)
            raise ex

    def deleted(self,response):
        item = DeletedItem()
        item['forum_id'] = self.forum_id
        return item

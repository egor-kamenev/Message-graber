# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import  FormRequest
from scrapy import log
from scrapy.exceptions import CloseSpider
from scrapy.shell import inspect_response

class DieselSpider(BaseSpider):

    name = "diesel"
    allowed_domains = ["diesel.elcat.kg"]

    urls= {
        'login_page_url' : "https://diesel.elcat.kg/index.php?act=Login&CODE=01&CookieDate=1",
        'messages_url' : "http://diesel.elcat.kg/index.php?act=Msg&CODE=1&VID=in&sort=&st=%s",
        }


    def __init__(self,login=None,password=None, source_user_pk=1, **kwargs):

        super(DieselSpider, self).__init__(**kwargs)

        self.source_user_pk = int(source_user_pk)

        self.user = {
            'login':login,
            'password':password
        }

    # Логинимся
    def start_requests(self):
        return [FormRequest(self.urls['login_page_url'], formdata={'UserName': self.user['login'], 'PassWord': self.user['password']}, callback=self.logged_in)]

    # проверяем результат авторизации
    def logged_in(self, response):

        #inspect_response(response, self)

        if self.user['login'].lower() in response.body.lower():
            log.msg(u"Авторизация %s прошла успешно"  %(self.user['login'].decode('cp1251')) ,level=log.INFO)
            return self.parse()
        else:
            raise CloseSpider(reason=u"Ошибка авторизации пользователя %s" %(self.user['login'].decode('cp1251')))
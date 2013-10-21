# -*- coding: utf-8 -*-
__author__ = 'e.kamenev'


import subprocess

from abc import ABCMeta, abstractmethod, abstractproperty

import sys
reload(sys)
sys.setdefaultencoding('cp1251')


"""
    Абстрактный класс  для "Источника сообщений"
"""

class Source():

    login = ''
    password = ''
    options = {}

    def __init__(self,login,password,source_user_pk):
        if not isinstance(login, unicode) : raise ValueError("var 'login' must be unicode type")
        if not isinstance(password, unicode) : raise ValueError("var 'login' must be unicode type")
        if not isinstance(source_user_pk, int) : raise ValueError("var 'login' must be int type")

        self.login = login
        self.password = password
        self.source_user_pk = source_user_pk

    __metaclass__=ABCMeta

#    @abstractproperty
#    def login(self):
#        """Лолгин"""
#
#    @abstractproperty
#    def password(self):
#        pass
#
#    @abstractproperty
#    def options(self):
#        pass

    @abstractmethod
    def sendMsg(self, recipient, msg_text, id):
        pass

    @abstractmethod
    def reciveMsg(self):
        pass

    @abstractmethod
    def deleteMsg(self, forum_id):
        pass


#class DieselSourceScrapyd(Source):
#
#    login = ''
#    password = ''
#    options = {}
#
#    def sendMsg(self, recipient, msg_text):
#
#        subprocess.call([
#            'curl',
#              '-d project=diesel',
#              '-d spider=sendMsg',
#              '-d login=%s' % (self.login),
#              '-d password=%s' %(self.password),
#              '-d msg=%s' %(msg_text)
#        ])
#
#    def reciveMsg(self):
#        subprocess.call('curl http://localhost:6800/schedule.json -d project=diesel -d spider=parse -d login=%s -d password=%s'
#                        % (self.login, self.password), shell=True)
#
#
#    def deleteMsg(self):
#        pass

"""
    Обертка для Scrapy Spyders для Дизеля
"""
class DieselSourceCrawl(Source):

    def sendMsg(self, companion_name, msg_text, id):

        if not isinstance(companion_name, unicode) : raise ValueError("var 'companion_name' must be unicode type")
        if not isinstance(msg_text, unicode) : raise ValueError("var 'msg_text' must be unicode type")
        if not isinstance(id, int) : raise ValueError("var 'id' must be int type")

        subprocess.call('scrapy crawl send -a login="%s" -a password="%s" -a companion_name="%s" -a msg_text="%s" -a message_reserve_id=%d'
                        % (self.login, self.password, companion_name, msg_text, id), shell=True)

    def reciveMsg(self):
        subprocess.call('scrapy crawl parse -a login="%s" -a password="%s" -a source_user_pk=%d'
                        % (self.login, self.password, self.source_user_pk),shell=True)

    def deleteMsg(self,forum_id):
        subprocess.call('scrapy crawl delete -a login="%s" -a password="%s" -a forum_id=%d'
                        % (self.login, self.password, forum_id),shell=True)


"""
   Абстрактная фабрика API для обработчкиков
"""
class HandlerFactory:

    def get(self, handler_class_name, **kwargs):

        module= __import__('sourceAPI')
        handler_cls = getattr(module,handler_class_name)
        return handler_cls (**kwargs)
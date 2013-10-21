# -*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, TransactionTestCase
from MessageCollector.models import *
import datetime
from diesel.diesel.pipelines import MessageItem
from django.core.files.base import ContentFile
import sourceAPI

class DieselMessageTestCase(TestCase):
    def setUp(self):

        sh = SourceHandler.objects.create(name='DieselSourceScrapyd')
        sys_user = SystemUser.objects.create(fio='System', email='system@saimatelecom.kg', enabled = True, login = 'System', password = '123')
        source = Source.objects.create(name='Diesel Elcat', host='http:\\\\diesel.elcat.kg', logo_path='logo.png', handler=sh)
        self.su = SourceUser.objects.create(login='Nafigator',password='Kapa53', system_user = sys_user, avatar_path = 'logo.png', source=source)


    def testSaveDiesel(self):

        item = MessageItem()
        item['message_reserve'] =  MessageReserve.objects.get_or_create(pk=1)[0]
        item['companion'] = Companion.objects.get_or_create(source_user=self.su, name='Nafigator', avatar_path = 'logo.png')[0]
        item['sender'] = 'Nafigator'
        item['date'] = datetime.datetime.now()
        item['text'] = 'Работает!!!'
        item['forum_id'] = 000000000

        Message.diesel.create(item)

        self.assertEqual(
            000000000,
            DieselMessage.objects.get().forum_id
        )

        self.assertEqual(
            'Nafigator',
            Message.objects.get().sender
        )

        self.assertEqual(MessageReserve.objects.get().pk,1)

    def testAllDieselMessage(self):

        item = MessageItem()
        item['message_reserve'] =  MessageReserve.objects.create()
        item['companion'] = Companion.objects.get_or_create(source_user=self.su, name='Nafigator', avatar_path = 'logo.png')[0]
        item['sender'] = 'Nafigator'
        item['date'] = datetime.datetime.now()
        item['text'] = 'Работает!!!'
        item['forum_id'] = 000000000

        Message.diesel.create(item)

        item = MessageItem()
        item['message_reserve'] =  MessageReserve.objects.create()
        item['companion'] = Companion.objects.get_or_create(source_user=self.su, name='Nafigator', avatar_path = 'logo.png')[0]
        item['sender'] = 'Nafigator'
        item['date'] = datetime.datetime.now()
        item['text'] = 'Работает!!!'
        item['forum_id'] = 000000001

        Message.diesel.create(item)

        msgs = Message.diesel.all()

        self.assertEqual(msgs[0].companion.source_user.source.name,'Diesel Elcat')
        self.assertEqual(msgs[1].companion.source_user.source.name,'Diesel Elcat')

    def testDeletedFromSource(self):

        item = MessageItem()
        item['message_reserve'] =  MessageReserve.objects.create()
        item['companion'] = Companion.objects.get_or_create(source_user=self.su, name='Nafigator', avatar_path = 'logo.png')[0]
        item['sender'] = 'Nafigator'
        item['date'] = datetime.datetime.now()
        item['text'] = 'Работает!!!'
        item['forum_id'] = 000000001

        Message.diesel.create(item)

        Message.diesel.deletedFromSource(forum_id = item['forum_id'])
        self.assertTrue(DieselMessage.objects.get(forum_id = item['forum_id']).deleted)




class FileTestCase(TestCase):

    def setUp(self):

        sh = SourceHandler.objects.create(name='DieselSourceScrapyd')
        sys_user = SystemUser.objects.create(fio='System', email='system@saimatelecom.kg', enabled = True, login = 'System', password = '123')
        source = Source.objects.create(name='Diesel Elcat', host='http:\\\\diesel.elcat.kg', logo_path='logo.png', handler=sh)
        self.su = SourceUser.objects.create(login='Nafigator',password='Kapa53', system_user = sys_user, avatar_path = 'logo.png', source=source)
        self.message_reserve = MessageReserve.objects.create()

        item = MessageItem()
        item['message_reserve'] =  MessageReserve.objects.get_or_create(pk=1)[0]
        item['companion'] = Companion.objects.get_or_create(source_user=self.su, name='Nafigator', avatar_path = 'logo.png')[0]
        item['sender'] = 'Nafigator'
        item['date'] = datetime.datetime.now()
        item['text'] = 'Работает!!!'
        item['forum_id'] = 000000000

        self.message = Message.diesel.create(item)

    def testGenerateUploadPath(self):



        a = File(message_reserve=self.message.message_reserve,type='file')
        a.file.save('test', ContentFile('test'))

        self.assertIn('attachedFiles/System/Diesel%20Elcat/Nafigator/Nafigator/test', a.file.url)
        self.assertIn('C:\\Users\\Nafigator\\Desktop\\djcode\\SaimaTelecom\\MessageCollector\\files\\attachedFiles\\System\\Diesel Elcat\\Nafigator\\Nafigator\\test', a.file.path)


class DieselSourceCrawlTestCase(TransactionTestCase):

    def setUp(self):

        sh = SourceHandler.objects.create(name='DieselSourceScrapyd')
        sys_user = SystemUser.objects.create(fio='System', email='system@saimatelecom.kg', enabled = True, login = 'System', password = '123')
        source = Source.objects.create(name='Diesel Elcat', host='http:\\\\diesel.elcat.kg', logo_path='logo.png', handler=sh)
        self.su = SourceUser.objects.create(login='Nafigator',password='Kapa53', system_user = sys_user, avatar_path = 'logo.png', source=source)


    def testSendMessage(self):



        source =  sourceAPI.DieselSourceCrawl('Nafigator','Kapa53')
        #        message_reserve = MessageReserve.objects.create()
        #        source.sendMsg('Nafigator', "Привет как дела?", message_reserve.pk)

        source.reciveMsg()
        print Message.diesel.all()
        self.assertEqual(Message.diesel.get().text, "Привет как дела?")








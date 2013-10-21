# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from django.core.files.base import ContentFile
from diesel.diesel.items import MessageItem, FileItem, DeletedItem
from MessageCollector.models import Companion, SourceUser, Message, DieselMessage


class DieselPipeline(object):

    def process_message(self, item):
        # если такого собеседника нет, то создаем нового
        #TODO Перенести в модель
        item['companion'] = Companion.objects.get_or_create(name=item['sender'], source_user=SourceUser.objects.get(pk=item['source_user_pk']))[0]
        item['visible'] = True
        Message.diesel.create(item)

    def process_file(self, item):

        file_model = item.save()
        file_model.file.save(item['name'], ContentFile(item['bin_content']))

    def process_deleted_message(self,item):
        Message.diesel.deletedFromSource(forum_id=item['forum_id'])


    def process_item(self, item, spider):

        if isinstance(item, MessageItem):
            self.process_message(item)

        if isinstance(item, FileItem):
            self.process_file(item)

        if isinstance(item, DeletedItem):
            self.process_deleted_message(item)


        return item

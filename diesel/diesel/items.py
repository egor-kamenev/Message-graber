# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field
from scrapy.item import Item
from MessageCollector.models import Message, File

class MessageItem(DjangoItem):
    django_model = Message
    forum_id = Field()
    source_user_pk = Field()
#    messageId = Field()
#    title = Field()
#    sender = Field()
#    date = Field()
#    text = Field()



class FileItem(DjangoItem):
    django_model = File
    bin_content = Field()
    name = Field()
#    messageId = Field()
#    name = Field()
#    type = Field()

class DeletedItem(Item):
    forum_id = Field()

class PostedItem(Item):
    message_reserve = Field()
    posted = Field()





# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class User(models.Model):

    login = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)

    class Meta:
        abstract = True



class SystemUser(User):

    fio = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    enabled = models.BooleanField()




class SourceHandler(models.Model):

    name = models.CharField(max_length=128, unique=True)


class Source(models.Model):

    name = models.CharField(max_length=128, unique=True)
    host = models.URLField(unique=True)
    logo_path = models.FilePathField(path='C:/Users/Nafigator/Desktop/djcode/SaimaTelecom/MessageCollector/static/source_avatar')
    handler = models.ForeignKey(SourceHandler)


class SourceUser(User):

    system_user = models.ForeignKey(SystemUser)
    avatar_path = models.FilePathField(path='C:/Users/Nafigator/Desktop/djcode/SaimaTelecom/MessageCollector/static/source_user_avatar', unique=True)
    source = models.ForeignKey(Source)

    class Meta:
        unique_together = ('login', 'source')


class Companion(models.Model):

    source_user = models.ForeignKey(SourceUser)
    name = models.CharField(max_length=32)
    avatar_path = models.FilePathField(path="C:/Users/Nafigator/Desktop/djcode/SaimaTelecom/MessageCollector/static/companion_avatar",unique=True)
#    objects = CompanionManager()


    class Meta:
        unique_together = ('source_user','name')



# при создании нового сообщения для дизеля, размещаем доп. данные в модели DieselMessage
class DieselManager(models.Manager):

    def create(self, item):
        DieselMessage.objects.create(message_reserve=item['message_reserve'], forum_id=item['forum_id'])
        model = item.save()
        return model

    def deletedFromSource(self, forum_id=None):

        a = DieselMessage.objects.get(forum_id=forum_id)
        a.deleted = True
        a.save()

    def all(self):
        return super(DieselManager, self).get_query_set().filter(companion__source_user__source__name = 'Diesel Elcat')


class Message(models.Model):
    message_reserve = models.OneToOneField('MessageReserve',primary_key=True)
    companion = models.ForeignKey(Companion)
    sender = models.CharField(max_length=32)
    date = models.DateTimeField()
    text = models.TextField()
    visible = models.BooleanField()
    diesel = DieselManager()
    objects = models.Manager()


    class Meta:
        unique_together = ('companion', 'sender', 'date')
        ordering = ['date']

class DieselMessage(models.Model):
    message_reserve = models.OneToOneField('MessageReserve',primary_key=True)
    forum_id = models.IntegerField(unique=True)
    deleted = models.BooleanField(default=False)




class File(models.Model):

    def generateUploadPath(instance, filename):

        companion= Message.objects.get(message_reserve=instance.message_reserve).companion
        source_user = companion.source_user
        system_user = source_user.system_user
        source = source_user.source

        return u'attachedFiles/%s/%s/%s/%s/%s' % (system_user.login, source.name, source_user.login, companion.name, filename)

    file_types = (
        (u'file',u'file'),
        (u'image',u'image')
    )

    message_reserve = models.ForeignKey('MessageReserve')
    type = models.CharField(max_length=16, choices=file_types)
    file = models.FileField(upload_to=generateUploadPath, max_length=200)



#    class Meta:
#        unique_together = ('message', 'path')


class MessageStatus(models.Model):

    status_types = (
        (u'unread',u'unread'),
        (u'outbox',u'outbox'),

    )

    message = models.ForeignKey(Message, unique= True)
    status = models.CharField(max_length=16, choices=status_types, null=True)


class MessageReserve(models.Model):
    id = models.AutoField(primary_key=True)



#sh = SourceHandler.objects.create(name='DieselSourceCrawl')
#sys_user = SystemUser.objects.create(fio='System', email='system@saimatelecom.kg', enabled = True, login = 'System', password = '123')
#source = Source.objects.create(name='Diesel Elcat', host='http:\\\\diesel.elcat.kg', logo_path='logo.png', handler=sh)
#su = SourceUser.objects.create(login='Nafigator',password='Kapa53', system_user = sys_user, avatar_path = 'logo.png', source=source)


















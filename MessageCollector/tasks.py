__author__ = 'e.kamenev'
from celery import task
from MessageCollector.models import SourceUser, SourceHandler
from sourceAPI import HandlerFactory



@task()
def receiveForAllSourceUsers():
    for handler in SourceHandler.objects.all():
        handler_source_users = SourceUser.objects.filter(source__handler = handler)
        for source_user in handler_source_users:
            HandlerFactory().get(handler.name, login=source_user.login, password=source_user.password, source_user_pk=source_user.pk).reciveMsg()


@task()
def sendUserMsg(login, password, source_user_pk, companion_name, text, message_reserve_id):
    HandlerFactory().get(SourceUser.objects.get(pk=source_user_pk).source.handler.name, login=login, password=password, source_user_pk=source_user_pk).sendMsg(companion_name, text, message_reserve_id)








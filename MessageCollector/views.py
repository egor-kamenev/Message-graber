# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.utils import  simplejson
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from MessageCollector.models import *

def messenger(request):
    return render_to_response("prototype.html",{})


def sourceList(request):
    if request.method == u'GET':

        result = list(Source.objects.all().values('id','name'))
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')

    else:
        return HttpResponseNotFound()


def userList(request):
    if request.method == u'GET':
         result = list(SourceUser.objects.filter(source__id = request.GET['source_id']).values('id', 'login'))
         json = simplejson.dumps(result)
         return HttpResponse(json, mimetype='application/json')

    else:
        return HttpResponseNotFound()

def companionList(request):
    if request.method == u'GET':
        result = list(Companion.objects.filter(source_user__id = request.GET['source_user_id']).values('id', 'name'))
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')

    else:
        return HttpResponseNotFound()

def messageList(request):
    if request.method == u'GET':
        result = list(Message.objects.filter(companion__id = request.GET['companion_id']).values('message_reserve','text'))
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')
    else:
        return HttpResponseNotFound()



def test(request):
    return render_to_response("SpecRunner.html",{})
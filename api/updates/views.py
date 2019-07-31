import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.views.generic import View
from api.mixins import JsonResponseMixin
from updates.models import Updates

class MyView(View):
    def get(self, request, *args, **kwargs):
        data = {
            'count': 100,
            'content': 'Some content here...'
        }
        return JsonResponse(data)

class MyViewMix(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            'count': 100,
            'content': 'Some content here...'
        }
        return self.renderToJsonResponse(data)

class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Updates.objects.get(id=1)
        jsonData = obj.serialize()
        #jsonData = serialize('json', [obj], fields=('user', 'content'))
        return HttpResponse(jsonData, content_type='application/json')

class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        obj = Updates.objects.all()
        jsonData = obj.serialize()
        return HttpResponse(jsonData, content_type='application/json')
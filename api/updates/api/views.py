import json

from django.http import HttpResponse
from django.views.generic import View

from api.mixins import HttpResponseMixin
from updates.api.mixins import CSRFExemptMixin
from updates.forms import UpdatesModelForm
from updates.models import Updates
from updates.api.utils import isJson

# Creating, Updating, Deleting, Retrieving -- Updates Model
class UpdatesModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def getObject(self, id=None):
        try:
            obj = Updates.objects.get(id=id)
        except:
            obj = None
        return obj

    def get(self, request, id, *args, **kwargs):
        obj = self.getObject(id=id)
        if obj == None:
            jsonData = json.dumps({'message': 'Page does not exist'})
            return self.renderToResponse(jsonData, status=404)
        jsonData = obj.serialize()
        return self.renderToResponse(jsonData, status=200)
    
    def post(self, request, *args, **kwargs):
        jsonData = json.dumps({'message': 'Not allowed, try using /api/updates/ endpoint'})
        return self.renderToResponse(jsonData, status=403)
    
    def put(self, request, id, *args, **kwargs):
        if not isJson(request.body):
            jsonData = json.dumps({'message': 'Invalid data sent. Please make sure that the data is in JSON'})
            return self.renderToResponse(jsonData, status=400)

        obj = self.getObject(id=id)
        if obj == None:
            jsonData = json.dumps({'message': 'Page does not exist'})
            return self.renderToResponse(jsonData, status=404)
        
        objData = json.loads(obj.serialize())
        passedData = json.loads(request.body)
        
        for key, value in passedData.items():
            objData[key] = value

        form = UpdatesModelForm(objData, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            jsonData = json.dumps(objData)
            return self.renderToResponse(jsonData, status=201)
        
        if form.errors:
            jsonData = json.dumps(form.errors)
            return self.renderToResponse(jsonData, status=400)

        jsonData = json.dumps({'message': 'Unknown data'})
        return self.renderToResponse(jsonData, status=400)
    
    def delete(self, request, id, *args, **kwargs):
        obj = self.getObject(id=id)
        if obj == None:
            jsonData = json.dumps({'message': 'Page does not exist'})
            return self.renderToResponse(jsonData, status=404)
        deleted_, deletedObj = obj.delete()
        if deleted_ == 1:
            jsonData = json.dumps({'message': f'Update {id} was deleted'})
            return self.renderToResponse(jsonData, status=200)
        errorData = {'message': 'Could not delete item'}
        return self.renderToResponse(json.dumps(errorData), status=400)


class UpdatesModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get(self, request, *args, **kwargs):
        qs = Updates.objects.all()
        jsonData = qs.serialize()
        return self.renderToResponse(jsonData, status=200)
    
    def post(self, request, *args, **kwargs):
        if not isJson(request.body):
            jsonData = json.dumps({'message': 'Invalid data sent. Please make sure that the data is in JSON'})
            return self.renderToResponse(jsonData, status=400)

        form = UpdatesModelForm(json.loads(request.body))
        if form.is_valid():
            obj = form.save(commit=True)
            jsonData = obj.serialize()
            return self.renderToResponse(jsonData, status=201)
        
        if form.errors:
            jsonData = json.dumps(form.errors)
            return self.renderToResponse(jsonData, status=400)

        jsonData = json.dumps({'message': 'Unknown data'})
        return self.renderToResponse(jsonData, status=400)
    
    def delete(self, request, *args, **kwargs):
        jsonData = json.dumps({'message': 'Can\'t delete an entire list.'})
        return self.renderToResponse(jsonData, status=403)
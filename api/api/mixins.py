from django.http import JsonResponse, HttpResponse

class HttpResponseMixin(object):
    is_json = False

    def renderToResponse(self, data, status=200):
        content_type = 'text/html'
        if self.is_json:
            content_type = 'application/json'
        return HttpResponse(data, content_type=content_type, status=status)

class JsonResponseMixin(object):
    def renderToJsonResponse(self, context, **response_kwargs):
        return JsonResponse(self.getData(context), **response_kwargs)

    def getData(self, context):
        return context
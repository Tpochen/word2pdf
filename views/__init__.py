from django.http import JsonResponse
from django.views import View
from . import converter_views


class Index(View):
    async def get(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 200,
            'msg': 'Welcome to word2pdf',
            'data': None,
        })

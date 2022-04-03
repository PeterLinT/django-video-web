# coding:utf-8
from django.views.generic import View
from app.libs.base_render import render_to_response


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    def get(self, request):
        return render_to_response(request, self.TEMPLATE)

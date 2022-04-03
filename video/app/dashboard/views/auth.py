# coding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.core.paginator import Paginator
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth

class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        to = request.GET.get('to', '')

        data = {'error': '', 'to': to}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to', '')
        data = {}
        print(username, password)
        exists = User.objects.filter(username=username).exists()
        data['error'] = '没有该用户'

        if not exists:
            return render_to_response(request, self.TEMPLATE, data=data)
        user = authenticate(username=username, password=password)

        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = '你无权登录'
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)

        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class AdminManager(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.all()

        page = request.GET.get('page', 1)
        p = Paginator(users, 2)
        total_page = p.num_pages

        if int(page) <= 1:
            page = 1

        current_page = p.get_page(int(page)).object_list
        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}

        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):

    def get(self, request):
        status = request.GET.get('status', 'on')

        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))

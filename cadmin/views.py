from django.shortcuts import render

# Create your views here.
import logging
import re
import uuid
import sys
from datetime import datetime, timedelta

from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
# from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
# from django.contrib.auth import views as auth_views
# from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator   
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from . import models
from .decorators import cadmin_user_login_required, cadmin_user_is_logged_in

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


@method_decorator(cadmin_user_is_logged_in, name='dispatch')
class LoginView(View):

    def get(self, request):
        return render(request, 'cadmin/login.html')

    def post(self, request):
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = models.Users.objects.get(Q(username=email_or_username) | Q(email=email_or_username))
            if user and check_password(password, user.password):
                token = user.token if user.token is not None else get_random_string(length=100)
                user.token = token
                user.save()
                request.session['cadmin_user'] = token
            else:
                return render(request, 'cadmin/login.html', {'error': 'Incorrect Password'})
        except:
            return render(request, 'cadmin/login.html', {'error': 'Incorrect User'})
        
        return redirect('/cadmin')


@cadmin_user_login_required
def logout(request):
    del request.session['cadmin_user']
    return redirect('/cadmin')


@method_decorator(cadmin_user_login_required, name='dispatch')
class IndexView(View):
    
    def get(self, request):
        return render(request, 'cadmin/index.html')


@method_decorator(cadmin_user_login_required, name='dispatch')
class AddUserView(View):

    def get(self, request):
        return render(request, 'cadmin/add-user.html')

    def post(self, request):
        data=request.POST
        temp_user = models.Users(
                    fullname=data['fullname'],
                    username=data['username'],
                    email=data['email'],
                    password=make_password(data['password']),
                    role=data['role'],
                )

        error = ''
        try:
            temp_user.save()
        except Exception as err:
            if 'duplicate key value' in str(err):
                logger.info("User {} hasn't been added because of duplication.".format(temp_user.email))
                error = temp_user.email + " is already exist."
        logger.info("User {} has been added".format(temp_user.username))
        if 'send_email' in data:
            logger.info("Send user detail email to {}".format(temp_user.username))
            temp_user.send_info_email()
        return render(request, 'cadmin/add-user.html', {'error': error})


@method_decorator(cadmin_user_login_required, name='dispatch')
class UsersView(View):

    def get(self, request):
        username = request.GET.get('username', '').strip()
        user_list = models.Users.objects.filter(username__icontains=username)
        page_number = request.GET.get('page', 1)
        user_list, paginator = do_paginate(user_list, page_number)
        base_url = '/cadmin/users/?username=' + username + "&"
        return render(request, 'cadmin/users.html',
                      {'user_list': user_list, 'paginator' : paginator, 'base_url': base_url, 'search_user_name': username})


def do_paginate(data_list, page_number):
    ret_data_list = data_list
    result_per_page = 1
    paginator = Paginator(data_list, result_per_page)
    try:
        ret_data_list = paginator.page(page_number)
    except EmptyPage:
        ret_data_list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        ret_data_list = paginator.page(1)
    return ret_data_list, paginator

def get_weekdate(day):
    dt = datetime.strptime(day, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


@method_decorator(cadmin_user_is_logged_in, name='dispatch')
class RecoverView(View):

    def get(self, request):
        return render(request, 'cadmin/recover.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()

        try:
            user = models.Users.objects.get(email=email)
            if user:
                token = user.token if user.token is not None else get_random_string(length=100)
                user.token = token
                user.save()
                send_mail(
                    subject='Recovery password verification Email',
                    message='Please verify if you are owner of this email by clicking <a href="/cadmin/recovery_verify/{}">here</a>.'.format(token),
                    from_email='admin@raplev.com',
                    recipient_list=[email]
                )
            else:
                return render(request, 'cadmin/recover.html', {'error': 'Incorrect User'})
        except:
            return render(request, 'cadmin/recover.html', {'error': 'Sorry, Something wrong. Please try later.'})
        
        return render(request, 'cadmin/recover.html', {'error': 'Please check your email.'})


@method_decorator(cadmin_user_is_logged_in, name='dispatch')
class SetPWView(View):

    def get(self, request):
        token = request.POST.get('token', '').strip()
        return render(request, 'cadmin/set-pw.html', {'token': token})

    def post(self, request):
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        token = request.POST.get('token', '').strip()

        if password != password_confirm:
            return render(request, 'cadmin/set-pw.html', {'error': 'Please confirm password.'})
        try:
            user = models.Users.objects.get(token=token)
            if user:
                user.password = make_password(data['password'])
                user.token = token
                user.save()
            else:
                return render(request, 'cadmin/set-pw.html', {'error': 'Incorrect User'})
        except:
            return render(request, 'cadmin/set-pw.html', {'error': 'Sorry, Something wrong. Please try later.'})
        
        return redirect('/cadmin')


@method_decorator(cadmin_user_login_required, name='dispatch')
class RevenueView(View):

    def get(self, request):
        source = request.GET.get('source', '').strip()
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        revenue_list = models.Revenue.objects.filter(source__icontains=source, date__range=(start_date, end_date))
        page_number = request.GET.get('page', 1)
        revenue_list, paginator = do_paginate(revenue_list, page_number)
        base_url = '/cadmin/revenue/?source=' + source + "&start_date=" + start_date + "&end_date=" + end_date + "&"
        return render(request, 'cadmin/revenue.html',
                      {'revenue_list': revenue_list, 'paginator' : paginator, 'base_url': base_url, 'source': source, 
                      'start_date': start_date, 'end_date': end_date})


@method_decorator(cadmin_user_login_required, name='dispatch')
class RevenueDetailsView(View):

    def get(self, request):
        source = request.GET.get('source', '').strip()
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        revenue_list = models.Revenue.objects.filter(source__icontains=source, date__range=(start_date, end_date))
        page_number = request.GET.get('page', 1)
        revenue_list, paginator = do_paginate(revenue_list, page_number)
        base_url = '/cadmin/revenue/?source=' + source + "&start_date=" + start_date + "&end_date=" + end_date + "&"
        return render(request, 'cadmin/revenue.html',
                      {'revenue_list': revenue_list, 'paginator' : paginator, 'base_url': base_url, 'source': source, 
                      'start_date': start_date, 'end_date': end_date})


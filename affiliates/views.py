import logging
# import re
# import uuid
# import sys
# import string
from datetime import datetime, timedelta, date

from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q, Sum, Count, F
# from django.db.models.functions import Extract
# from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator   
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.defaulttags import register

from cadmin import models
# from affiliates.models import COUNTRY_CODE
# from affiliates.form import MediasForm
from .decorators import affiliates_login_required, user_not_logged_in
from django.contrib.auth import (login as auth_login, logout as auth_logout)

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)
# app_url = '/affiliates'
app_url = ''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def current_user(request):
    try:
        # user = models.Users.objects.get(token=request.session['user'])
        # return user
        return request.user
    except:
        None


@method_decorator(user_not_logged_in, name='dispatch')
class Login(View):

    def get(self, request):
        return render(request, 'affiliates/login.html')

    def post(self, request):
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = models.Users.objects.get(Q(username=email_or_username) | Q(email=email_or_username))
            if user and check_password(password, user.password) and user.is_affiliate:
                token = user.token if user.token else get_random_string(length=100)
                user.token = token
                user.save()
                models.LoginLogs(
                    user=user,
                    ip_address=get_client_ip(request)
                ).save()
                auth_login(request, user)
                # request.session['user'] = token
            else:
                try:
                    models.SecurityStatus(
                        user=user,
                        ip_address=get_client_ip(request)
                    ).save()
                except:
                    log = 'here it need to sys log for error user login.'
                return render(request, 'affiliates/login.html', {'error': 'Invalid user.'})
        except Exception as e:
            print(e)
            return render(request, 'affiliates/login.html', {'error': 'Incorrect User'})
        
        return redirect(app_url+'')


@affiliates_login_required
def logout(request):
    # del request.session['user']
    auth_logout(request)
    # request.session['global_alert'] = {'success': "You are logged out."}
    return redirect(app_url+'')


@method_decorator(affiliates_login_required, name='dispatch')
class Index(View):
    
    def get(self, request):
        return redirect(app_url+'/dashboard')


@method_decorator(user_not_logged_in, name='dispatch')
class Register(View):

    def get(self, request, more={}):
        return render(request, 'affiliates/request.html', {**more})

    def post(self, request):
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        organization = request.POST.get('organization', '').strip()
        overview = request.POST.get('overview', '').strip()
        username = first_name.lower()+last_name.lower()
        password = '123456789'

        try:
            user = models.Users.objects.filter(Q(email=email) | Q(username=username))
            if user:
                return self.get(request, {'next': next_to, 'error': {'exist': True}})
            user = models.Users(
                username=username,
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                organization=organization,
                overview=overview,
                date_joined=datetime.now(),
                is_customer=True
            )
            user.save()
            affiliate = models.Affiliates(
                user = user,
            )
            affiliate.save()
            return self.get(request, {'success': True})
        except Exception as e:
            print(e)
            return self.get(request, {'error': 'Something wrong. Please try later.'})
            

def do_paginate(data_list, page_number, per_page=10):
    ret_data_list = data_list
    result_per_page = per_page
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


@method_decorator(user_not_logged_in, name='dispatch')
class ForgotPassword(View):

    def get(self, request, more={}):
        return render(request, 'affiliates/password.html', {**more})

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
                    message='Please verify if you are owner of this email by clicking <a href="{}/reset?t={}">here</a>.'.format(app_url, token),
                    from_email='admin@raplev.com',
                    recipient_list=[email]
                )
                return self.get(request, {'success': True})
            else:
                return self.get(request, {'error': True})
        except Exception as e:
            print(e)
            return self.get(request, {'error': 'Sorry, Something wrong. Please try later.'})
        


@method_decorator(user_not_logged_in, name='dispatch')
class ResetPassword(View):

    def get(self, request, more={}):
        token = request.GET.get('t', '').strip()
        return render(request, 'affiliates/reset.html', {'token': token, **more})

    def post(self, request):
        password = request.POST.get('password', '').strip()
        token = request.POST.get('token', '').strip()

        try:
            user = models.Users.objects.get(token=token)
            user.email_verified = True
            user.password = make_password(password)
            user.save()
            return self.get(request, {'success': True})
        except:
            return self.get(request, {'error': Try})
        
        return redirect(app_url+'')


@method_decorator(affiliates_login_required, name='dispatch')
class Dashboard(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        yesterday = (date.today() - timedelta(days=1))
        yesterday = yesterday.strftime('%Y-%m-%d')
        today = models.Reports.objects.filter(campaign__owner=current_user(request).affiliate(), created_at__date=date.today()).aggregate(Sum('payout'))['payout__sum']
        yesterday = models.Reports.objects.filter(campaign__owner=current_user(request).affiliate(), created_at__date=yesterday).aggregate(Sum('payout'))['payout__sum']
        week = models.Reports.objects.filter(campaign__owner=current_user(request).affiliate(), created_at__range=(start_date, end_date)).aggregate(Sum('payout'))['payout__sum']
        total = models.Reports.objects.filter(campaign__owner=current_user(request).affiliate()).aggregate(Sum('payout'))['payout__sum']

        items = models.Campaigns.objects.filter(id__contains=search, owner=current_user(request).affiliate())
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = app_url+'/dashboard/?search=' + search + "&start_date=" + start_date + "&end_date=" + end_date + "&"
        return render(request, 'affiliates/dashboard.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search, 
                      'start_date': start_date, 'end_date': end_date, 
                      'today': today, 'yesterday': yesterday, 'week': week, 'total': total})


class Contact(View):

    def get(self, request, more={}):
        return render(request, 'affiliates/contact.html', {**more})

    def post(self, request):
        email_address = request.POST.get('email_address', '')
        cc_email_address = request.POST.get('cc_email_address', '')
        use_my_email = request.POST.get('use_my_email', '')
        subject = 'Affiliates Contact'
        content = request.POST.get('content', '').strip()
        fullname = email_address
        user = None
        if use_my_email == 'on':
            try:
                # user = models.Users.objects.get(token=request.session['user'])
                user = request.user
                fullname = user.get_fullname()
                email_address = user.email
            except:
                return self.get(request, {'error': {'email_address': 'Not valid email address.'}})
        elif email_address == '':
            return self.get(request, {'error': {'email_address': 'Email address is required.'}})

        try:
            contact = models.Contacts()
            contact.fullname = fullname
            contact.email_address = email_address
            contact.cc_email_address = cc_email_address
            contact.subject = subject
            contact.content = content
            contact.user = user
            contact.ip_address = get_client_ip(request)
            contact.created_at = datetime.now()
            contact.save()

            return self.get(request, {'alert': {'success': 'Message is sent successfuly. We will contact you soon.'}})
        except:
            return self.get(request, {'alert': {'warning': 'Sorry, Something wrong. Try later.'}})


@method_decorator(affiliates_login_required, name='dispatch')
class Profile(View):

    def get(self, request, more={}):
        return render(request, 'affiliates/profile.html', {**more})

    def post(self, request):
        avatars = request.POST.get('avatar', '')
        object_data = {
            'email': request.POST.get('email', ''),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'organization': request.POST.get('organization', ''),
            'billing_address': request.POST.get('billing_address', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'overview': request.POST.get('overview', ''),
            'phonenumber': request.POST.get('phonenumber', ''),
        }
        user = current_user(request)
        user.__dict__.update(object_data)

        password = request.POST.get('password', '')
        if password:
            user.password = make_password(password)

        try:
            user.save()
            return self.get(request, {'alert': {'success': 'Profile updated successfully!'}})
        except:
            return self.get(request, {'alert': {'warning': 'Not saved.'}})


@method_decorator(affiliates_login_required, name='dispatch')
class Reports(View):

    def get(self, request):
        campaign = request.GET.get('campaign', '').strip()
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        if campaign:
            items = models.Reports.objects.filter(campaign_id=campaign, created_at__range=(start_date, end_date))
        else:
            items = models.Reports.objects.filter(campaign__owner=current_user(request).affiliate(), created_at__range=(start_date, end_date))
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        campaigns = models.Campaigns.objects.all()
        base_url = app_url+'/reports/?campaign=' + campaign + "&start_date=" + start_date + "&end_date=" + end_date + "&"
        return render(request, 'affiliates/reports.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'campaign': campaign, 'campaigns': campaigns, 
                      'start_date': start_date, 'end_date': end_date})


@method_decorator(affiliates_login_required, name='dispatch')
class Campaigns(View):

    def get(self, request):
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        items = models.Campaigns.objects.filter(owner=current_user(request).affiliate())
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        for item in items:
            item.payouts = models.Reports.objects.filter(campaign=item, created_at__range=(start_date, end_date)).aggregate(Sum('payout'))['payout__sum']
            item.clicks = models.Reports.objects.filter(campaign=item, report_field='click', created_at__range=(start_date, end_date)).count()
            item.conversions = models.Reports.objects.filter(campaign=item, report_field='conversion', created_at__range=(start_date, end_date)).count()
        base_url = app_url+'/campaigns/?start_date=' + start_date + "&end_date=" + end_date + "&"
        return render(request, 'affiliates/campaigns.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url,
                      'start_date': start_date, 'end_date': end_date})


@method_decorator(affiliates_login_required, name='dispatch')
class CampaignDetails(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        try:
            item = models.Campaigns.objects.get(id=item_id)
            return render(request, 'affiliates/campaign-details.html', {'item': item})
        except:
            return render(request, 'affiliates/campaign-details.html', {'item': [], 'alert': {'warning': 'We couldn`t find it.'}})
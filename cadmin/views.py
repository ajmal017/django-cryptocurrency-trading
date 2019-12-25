from django.shortcuts import render

# Create your views here.
import logging
import re
import uuid
import sys
from datetime import datetime, timedelta

from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
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
                del request.session['global_alert']
            else:
                return render(request, 'cadmin/login.html', {'error': 'Incorrect Password'})
        except:
            return render(request, 'cadmin/login.html', {'error': 'Incorrect User'})
        
        return redirect('/cadmin')


@cadmin_user_login_required
def logout(request):
    del request.session['cadmin_user']
    request.session['global_alert'] = {'success': "You are logged out."}
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

        try:
            temp_user.save()
        except Exception as err:
            if 'duplicate key value' in str(err):
                logger.info("User {} hasn't been added because of duplication.".format(temp_user.email))
                return render(request, 'cadmin/add-user.html', {'error': temp_user.email + " is already exist."})
            return render(request, 'cadmin/add-user.html', {'error': "Something wrong. Please try again later."})
        logger.info("User {} has been added".format(temp_user.username))
        if 'send_email' in data:
            logger.info("Send user detail email to {}".format(temp_user.username))
            temp_user.send_info_email()
        return render(request, 'cadmin/add-user.html', {'success': "User {} has been added".format(temp_user.username)})


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
                # send_mail(
                #     subject='Recovery password verification Email',
                #     message='Please verify if you are owner of this email by clicking <a href="/cadmin/recovery_verify/{}">here</a>.'.format(token),
                #     from_email='admin@raplev.com',
                #     recipient_list=[email]
                # )
            else:
                return render(request, 'cadmin/recover.html', {'error': 'Incorrect User'})
        except:
            return render(request, 'cadmin/recover.html', {'error': 'Sorry, Something wrong. Please try later.'})
        
        return render(request, 'cadmin/recover.html', {'success': 'Please check your email.'})


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
                user.save()
            else:
                return render(request, 'cadmin/set-pw.html', {'success': 'Success reset password.'})
        except:
            return render(request, 'cadmin/set-pw.html', {'error': 'Sorry, Something wrong. Please try later.'})
        
        return redirect('/cadmin')


@method_decorator(cadmin_user_login_required, name='dispatch')
class RevenueView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        items = models.Revenue.objects.filter(source__icontains=search, date__range=(start_date, end_date))
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/revenue/?search=' + search + "&start_date=" + start_date + "&end_date=" + end_date + "&"
        return render(request, 'cadmin/revenue.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search, 
                      'start_date': start_date, 'end_date': end_date})


@method_decorator(cadmin_user_login_required, name='dispatch')
class RevenueDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Revenue.objects.get(id=item_id)
        return render(request, 'cadmin/revenue-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class RevStatsView(View):

    def get(self, request):
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        total_sum = models.Revenue.objects.filter(date__range=(start_date, end_date)).aggregate(total_earned=Sum('amount'), 
            total_refunded=Sum('refund'))
        total_earned = total_sum['total_earned'] or 0
        total_refunded = total_sum['total_refunded'] or 0
        total_count = models.Revenue.objects.filter(date__range=(start_date, end_date)).count()
        main_count = models.Revenue.objects.filter(source='Main platform', date__range=(start_date, end_date)).count()
        percentage = round(main_count/total_count*100) if total_count > 0 else 0
        return render(request, 'cadmin/rev-stats.html',
                      {'total_earned': total_earned, 'total_refunded' : total_refunded, 'percentage': percentage, 
                      'start_date': start_date, 'end_date': end_date})


@method_decorator(cadmin_user_login_required, name='dispatch')
class OffersView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Offers.objects.filter(Q(id__icontains=search) | Q(address__icontains=search))
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/offers/?search=' + search + "&"
        return render(request, 'cadmin/offers.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class OfferDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Offers.objects.get(id=item_id)
        return render(request, 'cadmin/offer-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class TradesView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        startweek, endweek = get_weekdate(datetime.now().date().strftime("%Y-%m-%d"))
        start_date = request.GET.get('start_date', startweek).strip()
        end_date = request.GET.get('end_date', endweek).strip()
        items = models.Trades.objects.filter(id__icontains=search, created_at__range=(start_date, end_date))
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/trades/?search=' + search + "&start_date=" + start_date + "&end_date=" + end_date + "&"
        return render(request, 'cadmin/trades.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search, 
                      'start_date': start_date, 'end_date': end_date})


@method_decorator(cadmin_user_login_required, name='dispatch')
class TradeDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Trades.objects.get(id=item_id)
        return render(request, 'cadmin/trade-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class CustomersView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Customers.objects.filter(Q(email__icontains=search) | Q(username__icontains=search))
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/customers/?search=' + search + "&"
        return render(request, 'cadmin/customers.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class CustomerDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Customers.objects.get(id=item_id)
        return render(request, 'cadmin/customer-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class CustomerSuspend(View):

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        item = models.Customers.objects.get(id=item_id)
        item.suspended = True
        item.save()
        return render(request, 'cadmin/customer-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class TransactionsView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Transactions.objects.filter(id__icontains=search)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/transactions/?search=' + search + "&"
        return render(request, 'cadmin/transactions.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class TransactionDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Transactions.objects.get(id=item_id)
        return render(request, 'cadmin/transaction-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class EscrowsView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Escrows.objects.filter(id__icontains=search)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/escrows/?search=' + search + "&"
        return render(request, 'cadmin/escrows.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class EscrowDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Escrows.objects.get(id=item_id)
        return render(request, 'cadmin/escrow-details.html', {'item': item, })



@method_decorator(cadmin_user_login_required, name='dispatch')
class EscrowRelease(View):

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        item = models.Escrows.objects.get(id=item_id)
        item.status = True
        item.save()
        return render(request, 'cadmin/escrow-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class EscrowCancel(View):

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        item = models.Escrows.objects.get(id=item_id)
        item.status = False
        item.save()
        return render(request, 'cadmin/escrow-details.html', {'item': item, })
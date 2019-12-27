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
from .context_processors import cadmin_user

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
                token = user.token if user.token else get_random_string(length=100)
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


@method_decorator(cadmin_user_login_required, name='dispatch')
class SupportCenterView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Tickets.objects.filter(id__icontains=search)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/support-center/?search=' + search + "&"
        return render(request, 'cadmin/support-center.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class TicketDetailsDisputeView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Tickets.objects.get(id=item_id)
        messages = models.Messages.objects.filter(ticket=item_id).order_by('-created_at')
        return render(request, 'cadmin/ticket-details-dispute.html', {'item': item, 'messages': messages})

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        content = request.POST.get('content', '').strip()
        # attach_file = request.POST.attach_file
        item = models.Tickets.objects.get(id=item_id)
        mes = models.Messages()
        mes.ticket = item
        mes.writer = cadmin_user(request)['cadmin_user'].username
        mes.content = content
        # mes.attach_file = attach_file
        mes.created_at = datetime.now()
        mes.save()
        messages = models.Messages.objects.filter(ticket=item_id).order_by('-created_at')
        return render(request, 'cadmin/ticket-details-dispute.html', {'item': item, 'messages': messages})


@method_decorator(cadmin_user_login_required, name='dispatch')
class TicketDetailsNoDisputeView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Tickets.objects.get(id=item_id)
        messages = models.Messages.objects.filter(ticket=item_id).order_by('-created_at')
        return render(request, 'cadmin/ticket-details-no-dispute.html', {'item': item, 'messages': messages})

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        content = request.POST.get('content', '').strip()
        # attach_file = request.POST.attach_file
        item = models.Tickets.objects.get(id=item_id)
        mes = models.Messages()
        mes.ticket = item
        mes.writer = cadmin_user(request)['cadmin_user'].username
        mes.content = content
        # mes.attach_file = attach_file
        mes.created_at = datetime.now()
        mes.save()
        messages = models.Messages.objects.filter(ticket=item_id).order_by('-created_at')
        return render(request, 'cadmin/ticket-details-no-dispute.html', {'item': item, 'messages': messages})


@method_decorator(cadmin_user_login_required, name='dispatch')
class IdVerifyAppView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Idcards.objects.filter(id__icontains=search)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/id-verify-app/?search=' + search + "&"
        return render(request, 'cadmin/id-verify-app.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class IdVerifyAppDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Idcards.objects.get(id=item_id)
        return render(request, 'cadmin/id-verify-app-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class IdVerifyAppReject(View):

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        item = models.Idcards.objects.get(id=item_id)
        item.status = False
        item.save()
        return render(request, 'cadmin/id-verify-app-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class IdVerifyAppAccept(View):

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        item = models.Idcards.objects.get(id=item_id)
        item.status = True
        item.save()
        return render(request, 'cadmin/id-verify-app-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class ContactFormView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        items = models.Contacts.objects.filter(email_address__icontains=search)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/contact-form/?search=' + search + "&"
        return render(request, 'cadmin/contact-form.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search,})


@method_decorator(cadmin_user_login_required, name='dispatch')
class ContactFormDetailsView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Contacts.objects.get(id=item_id)
        item.readed = True
        item.save()
        return render(request, 'cadmin/contact-form-details.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class AdditionalPagesView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        search_status = request.GET.get('search_status', '').strip()
        items = models.Pages.objects.filter(title__icontains=search, status__icontains=search_status)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/additional-pages/?search=' + search + "&search_status=" + search_status + "&"
        return render(request, 'cadmin/additional-pages.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search, 'search_status': search_status})


@method_decorator(cadmin_user_login_required, name='dispatch')
class AdditionalPagePreviewView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Pages.objects.get(id=item_id)
        return render(request, 'cadmin/custom-page.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class AddNewPageView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Pages()
        try:
            item = models.Pages.objects.get(id=item_id)
            title = 'Edit page'
        except:
            title = 'Add new page'
        return render(request, 'cadmin/add-new-page.html', {'item': item, 'title': title})

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        action = request.POST.get('action', '').strip()
        title = request.POST.get('title', '').strip()
        context = request.POST.get('context', '').strip()
        try:
            item = models.Pages.objects.get(id=item_id)
        except:
            item = models.Pages()
            item.created_at = datetime.now()
        
        item.posted_by = cadmin_user(request)['cadmin_user'].username
        item.status = action
        item.title = title
        item.context = context
        item.updated_on = datetime.now()
        item.save()
        title = 'Edit page'
        return render(request, 'cadmin/add-new-page.html', {'item': item, 'title': title})


@method_decorator(cadmin_user_login_required, name='dispatch')
class BlogView(View):

    def get(self, request):
        search = request.GET.get('search', '').strip()
        search_status = request.GET.get('search_status', '').strip()
        items = models.Posts.objects.filter(title__icontains=search, status__icontains=search_status)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = '/cadmin/blog/?search=' + search + "&search_status=" + search_status + "&"
        return render(request, 'cadmin/blog.html',
                      {'items': items, 'paginator' : paginator, 'base_url': base_url, 'search': search, 'search_status': search_status})


@method_decorator(cadmin_user_login_required, name='dispatch')
class PostPreviewView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Posts.objects.get(id=item_id)
        return render(request, 'cadmin/custom-post.html', {'item': item, })


@method_decorator(cadmin_user_login_required, name='dispatch')
class AddNewPostView(View):

    def get(self, request):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Posts()
        try:
            item = models.Posts.objects.get(id=item_id)
            title = 'Edit post'
        except:
            title = 'Add new post'
        return render(request, 'cadmin/add-new-post.html', {'item': item, 'title': title})

    def post(self, request):
        item_id = request.POST.get('item_id', '').strip()
        action = request.POST.get('action', '').strip()
        title = request.POST.get('title', '').strip()
        context = request.POST.get('context', '').strip()
        disallow_comments = request.POST.get('disallow_comments', False)
        featured_images = request.POST.get('featured_images', '').strip()
        tags = request.POST.get('tags', '').strip()
        try:
            item = models.Posts.objects.get(id=item_id)
        except:
            item = models.Posts()
            item.created_at = datetime.now()
        
        item.posted_by = cadmin_user(request)['cadmin_user'].username
        item.status = action
        item.title = title
        item.context = context
        item.disallow_comments = disallow_comments
        item.featured_images = featured_images
        item.tags = tags
        item.updated_on = datetime.now()
        item.save()
        title = 'Edit post'
        return render(request, 'cadmin/add-new-post.html', {'item': item, 'title': title})


# ----------------- From here for dw920  ----------------
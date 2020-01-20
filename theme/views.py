import logging
# import re
# import uuid
from datetime import datetime, timedelta

from django.utils.decorators import method_decorator   
# from month.models import Month

from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.db.models import Q, Sum, Count, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
# from django.contrib.auth import views as auth_views
# from django.core.exceptions import ObjectDoesNotExist
from django.views import View
# from django.core.paginator import Paginator
# from django.http import Http404
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from cadmin import models
from .decorators import customer_user_login_required, user_not_logged_in
from .context_processors import theme_decorators
# from .cache import CurrencyExchangeData, GoogleMapsGeocoding
from django.template.defaulttags import register

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)
app_url = ''


@register.filter
def multiple3(num):    
    ret = True if num % 3 == 0 else False
    return ret


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def current_user(request):
    try:
        user = models.Users.objects.get(token=request.session['user'])
        return user
    except:
        None


class Index(View):
    
    def get(self, request, more={}):
        # request.LANGUAGE_CODE == 'zh-hans'
        BTC_items = models.Offers.objects.filter(what_crypto='BTC', admin_confirmed=True).order_by('-created_at')[:5]
        ETH_items = models.Offers.objects.filter(what_crypto='ETH', admin_confirmed=True).order_by('-created_at')[:5]
        XRP_items = models.Offers.objects.filter(what_crypto='XRP', admin_confirmed=True).order_by('-created_at')[:5]
        return render(request, 'theme/index.html', {'BTC_items': BTC_items, 'ETH_items': ETH_items, 'XRP_items': XRP_items, **more})


@method_decorator(user_not_logged_in, name='dispatch')
class Login(View):

    def get(self, request, more={}):
        next_to = more['next'] if 'next' in more else request.GET.get('next', '').strip()
        return render(request, 'theme/login.html', {'next': next_to, **more})

    def post(self, request):
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        next_to = request.POST.get('next', '').strip()

        try:
            user = models.Users.objects.get(email=email_or_username) # Q(username=email_or_username) |
            if user and check_password(password, user.password):
                token = user.token if user.token else get_random_string(length=100)
                user.token = token
                user.save()
                request.session['user'] = token
            else:
                if next_to:
                    return self.get(request, {'next': next_to, 'error': {'password': 'Incorrect Password'}})
                else:
                    return JsonResponse({'error': {'password': 'Incorrect Password'}})
        except:
            if next_to:
                return self.get(request, {'next': next_to, 'error': {'email': 'Incorrect User'}})
            else:
                return JsonResponse({'error': {'email': 'Incorrect User'}})
        
        if next_to:
            return redirect(next_to)
        else:
            return JsonResponse({'success': True})


@customer_user_login_required
def logout(request):
    del request.session['user']
    # request.session['global_alert'] = {'success': "You are logged out."}
    return redirect('/'+app_url+'')


@method_decorator(user_not_logged_in, name='dispatch')
class Register(View):

    def get(self, request, more={}):
        next_to = more['next'] if 'next' in more else request.GET.get('next', '').strip()
        return render(request, 'theme/register.html', {'next': next_to, **more})

    def post(self, request):
        customer_type = request.POST.get('customer_type', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        next_to = request.POST.get('next', '').strip()

        if password != password_confirm:
            if next_to:
                return self.get(request, {'next': next_to, 'error': {'password': 'Password is not confirmed.'}})
            else:
                return JsonResponse({'error': {'password': 'Password is not confirmed.'}})
        try:
            user = models.Users.objects.filter(Q(email=email) | Q(username=username))
            if user:
                if next_to:
                    return self.get(request, {'next': next_to, 'error': {'email': 'This account is already exist.'}})
                else:
                    return JsonResponse({'error': {'email': 'This account is already exist.'}})
            user = models.Users(
                username=username,
                email=email,
                password=make_password(password),
                date_joined=datetime.now(),
                is_customer=True
            )
            user.save()
            customer = models.Customers(
                user = user,
                customer_type = customer_type,
                seller_level = 1 if customer_type == 'sell' else None
            )
            customer.save()
            token = user.token if user.token else get_random_string(length=100)
            user.token = token
            user.save()
            request.session['user'] = token

        except Exception as e:
            if next_to:
                return self.get(request, {'next': next_to, 'error': {'email': 'Something wrong. Please try later.'}})
            else:
                return JsonResponse({'error': {'email': 'Something wrong. Please try later.'}})
        
        if next_to:
            return redirect(next_to)
        else:
            return JsonResponse({'success': True})


@method_decorator(user_not_logged_in, name='dispatch')
class ForgotPassword(View):

    def post(self, request):
        email = request.POST.get('email', '').strip()
        phonenumber = request.POST.get('phonenumber', '').strip()
        next_to = request.POST.get('next', '').strip()

        try:
            users = models.Users.objects.filter(Q(email=email) | Q(phonenumber=phonenumber))
            if users.count() > 0:
                user = user[0]
            else:
                if email:
                    if next_to:
                        return ForgotPasswordEmail.get(ForgotPasswordEmail, request, {'error': {'email': 'Please Insert correct Email.'}, 'next': next_to})
                    else:
                        return JsonResponse({'error': {'email': 'Please Insert correct Email.'}})
                elif phonenumber:
                    if next_to:
                        return ForgotPasswordPhone.get(ForgotPasswordPhone, request, {'error': {'phonenumber': 'Please Insert correct Phone number.'}, 'next': next_to})
                    else:
                        return JsonResponse({'error': {'phonenumber': 'Please Insert correct Phonenumber.'}})

            if email:
                next_tos = '&next='+next_to if next_to else ''
                user.send_forgot_pw_email(next_tos)
                if next_to:
                    return ForgotPasswordEmail.get(ForgotPasswordEmail, request, {'alert': {'success': 'Verification Email sent to your email, Please check your emails.'}, 'next': next_to})
                else:
                    return JsonResponse({'success': 'Verification Email sent to your email, Please check your emails.'})
            elif phonenumber:
                user.send_phone_code(phonenumber)
                if next_to:
                    return redirect(app_url+'/confirm-forgot-password-phone-code?phonenumber='+phonenumber+'&next='+next_to)
                else:
                    return JsonResponse({'phone_code_confirm': True, 'phonenumber': phonenumber})
            else:
                return {'error': 'Insert Email or Phonenumber'}
        except Exception as e:
            return JsonResponse({'error': True})
        
        if next_to:
            return redirect(next_to)
        else:
            return JsonResponse({'success': True})


@method_decorator(user_not_logged_in, name='dispatch')
class ForgotPasswordEmail(View):

    def get(self, request, more={}):
        next_to = more['next'] if 'next' in more else request.GET.get('next', '').strip()
        return render(request, 'theme/forgot-password-email.html', {'next': next_to, **more})


@method_decorator(user_not_logged_in, name='dispatch')
class ForgotPasswordPhone(View):

    def get(self, request, more={}):
        next_to = more['next'] if 'next' in more else request.GET.get('next', '').strip()
        return render(request, 'theme/forgot-password-phone.html', {'next': next_to, **more})


@method_decorator(user_not_logged_in, name='dispatch')
class ResendConfirmEmail(View):
    
    def post(self, request):
        user = current_user(request)
        user.send_confirm_email()
        return JsonResponse({'success': 'Email sent.'})


@method_decorator(user_not_logged_in, name='dispatch')
class ResendConfirmPhone(View):
    
    def post(self, request):
        phonenumber = request.POST.get('phonenumber', '')
        try:
            user = models.Users.objects.get(phonenumber=phonenumber)
            # user.send_phone_code(phonenumber)
            return JsonResponse({'success': 'Phone code resent.'})
        except:
            return JsonResponse({'error': 'Try again.'})


@method_decorator(user_not_logged_in, name='dispatch')
class ConfirmForgotPWPhoneCode(View):

    def get(self, request, more={}):
        next_to = more['next'] if 'next' in more else request.GET.get('next', '').strip()
        phonenumber = request.GET.get('phonenumber', '').strip()
        return render(request, 'theme/confirm-forgot-password-phone-code.html', {'next': next_to, 'phonenumber': phonenumber, **more})

    def post(self, request):
        phonenumber = request.POST.get('phonenumber', '')
        code = request.POST.get('code', '')
        next_to = request.POST.get('next', '').strip()
        try:
            user = models.Users.objects.get(phonenumber=phonenumber)
            if True:#user.validate_phone_code(phonenumber, code):
                user.phone_verified = True
                user.phonenumber = phonenumber
                user.save()
                request.session['user'] = user.token
                if next_to:
                    return redirect(app_url+'/reset-password?next='+next_to)
                else:
                    return JsonResponse({'success': True})
            else:
                if next_to:
                    return self.get(request, {'next': next_to, 'phonenumber': phonenumber, 'error': {'code': 'Invaild phone code. Try again'}})
                else:
                    return JsonResponse({'error': 'That`s invalid phone code.'})
        except:
            if next_to:
                return self.get(request, {'next': next_to, 'phonenumber': phonenumber, 'error': {'code': 'ERROR!. Try again'}})
            else:
                return JsonResponse({'error': 'Try again.'})

class ConfirmForgotPWEmail(View):

    def get(self, request, more={}):
        token = request.GET.get('t', '').strip()
        next_to = request.GET.get('next', '').strip()
        try:
            user = models.Users.objects.get(token=token)
            user.email_verified = True
            user.save()
            request.session['user'] = user.token
        
            if next_to:
                return redirect(app_url+'/reset-password?next='+next_to)
            else:
                return Index.get(Index, request, {'alert': {'success': 'Email Confirmed'}})
        except:
            return Index.get(Index, request, {'alert': {'success':  'Email is Not Verified'}})


class ConfirmForgotPWPhone(View):

    def post(self, request):
        return False

@method_decorator(customer_user_login_required, name='dispatch')
class ResetPassword(View):

    def get(self, request, more={}):
        next_to = more['next'] if 'next' in more else request.GET.get('next', '').strip()
        return render(request, 'theme/reset-password.html', {'next': next_to, **more})

    def post(self, request):
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        next_to = request.POST.get('next', '/')
        if password != password_confirm:
            return self.get(request, {'next': next_to, 'error': {'password': 'Password is not confirmed.'}})
        try:
            user = current_user(request)
            user.password = make_password(password)
            user.save()
            return redirect(next_to)
        except:
            return self.get(request, {'next': next_to, 'alert': {'warning': 'Error! Try later.'}})


@method_decorator(customer_user_login_required, name='dispatch')
class ResendVerifyEmail(View):

    def post(self, request):
        user = current_user(request)
        user.send_confirm_email()
        return JsonResponse({'success': 'Email sent.'})


@method_decorator(customer_user_login_required, name='dispatch')
class ResendVerifyPhone(View):

    def post(self, request):
        user = current_user(request)
        user.send_phone_code()
        return JsonResponse({'success': 'Phone code sent.'})


@method_decorator(customer_user_login_required, name='dispatch')
class VerifyPhoneCode(View):

    def get(self, request, more={}):
        return render(request, 'theme/index.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class VerifyEmail(View):

    def get(self, request, more={}):
        token = request.GET.get('t', '').strip()
        next_to = request.GET.get('next', '').strip()
        try:
            user = current_user(request)

            if token == user.token:
                user.email_verified = True
                user.save()
                if next_to:
                    return redirect(next_to)
                else:
                    return Index.get(Index, request, {'alert': {'success': 'Email Verified'}})
            else:
                return Index.get(request, {'alert': 'Email is Not Verified'})

        except:
            return Index.get(request, {'alert': 'Email is Not Verified'})


@method_decorator(customer_user_login_required, name='dispatch')
class VerifyPhone(View):

    def get(self, request, more={}):
        return render(request, 'theme/index.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class NewOffer(View):
    
    def get(self, request, more={}):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Offers.objects.get(id=item_id) if item_id else ''
        return render(request, 'theme/new-offer.html', {'item': item, **more})

    def post(self, request):
        item_id = request.POST.get('item_id', '')
        trade_price = float(request.POST.get('trade_price', 0))
        if request.POST.get('useMarketPrice', '').strip() == 'on':
            trade_price = models.Pricing.get_rate(request.POST.get('what_crypto'), request.POST.get('flat'), 'market_price')
        if request.POST.get('trailMarketPrice', '').strip() == 'on':
            trade_price = models.Pricing.get_rate(request.POST.get('what_crypto'), request.POST.get('flat'), 'trail_market_price')

        object_data = {
            'trade_type': request.POST.get('trade_type'),
            'what_crypto': request.POST.get('what_crypto'),
            'flat': request.POST.get('flat'),
            'postal_code': request.POST.get('postal_code') if request.POST.get('postal_code') else None,
            'show_postcode': True if request.POST.get('show_postcode') == 'on' else False,
            'country': request.POST.get('country'),
            'city': request.POST.get('city'),
            'trade_price': trade_price,
            'use_market_price': True if request.POST.get('useMarketPrice') == 'on' else False,
            'trail_market_price': True if request.POST.get('trailMarketPrice') == 'on' else False,
            'profit_start': float(request.POST.get('profit_start')) if request.POST.get('profit_start', None) != '' else None,
            'profit_end': float(request.POST.get('profit_end')) if request.POST.get('profit_end', None) != '' else None,
            'profit_time': request.POST.get('profit_time'),
            'minimum_transaction_limit': request.POST.get('minimum_transaction_limit'),
            'maximum_transaction_limit': request.POST.get('maximum_transaction_limit'),
            'operating_hours_start': request.POST.get('operating_hours_start'),
            'operating_hours_end': request.POST.get('operating_hours_end'),
            'restrict_hours_start': request.POST.get('restrict_hours_start'),
            'restrict_hours_end': request.POST.get('restrict_hours_end'),
            'proof_times': request.POST.get('proof_times'),
            'supported_location': request.POST.getlist('supported_location[]'),
            'trade_overview': request.POST.get('trade_overview', '').strip(),
            'message_for_proof': request.POST.get('message_for_proof', '').strip(),
            'identified_user_required': True if request.POST.get('identified_user_required') == 'on' else False,
            'sms_verification_required': True if request.POST.get('sms_verification_required') == 'on' else False,
            'minimum_successful_trades': request.POST.get('minimum_successful_trades'),
            'minimum_complete_trade_rate': request.POST.get('minimum_complete_trade_rate'),
            'admin_confirmed': False,
            'created_by': current_user(request),
            'created_at': datetime.now(),
        }

        offer = models.Offers()
        try:
            offer.__dict__.update(object_data)
            offer.save()
            return OfferActivity.get(OfferActivity, request, {'item_id': offer.pk, 'offer_success': 'Offer Posted'})
        except Exception as e:
            print(e)
            return self.get(request, {'alert': {'warning': 'Sorry, Your offer is not saved.'}})


class SupportCenter(View):

    def get(self, request, more={}):
        # items = models.Tickets.objects.filter('email' == current_user(request).email)[:100]
        items = models.Tickets.objects.all().order_by('created_at')[:100]
        return render(request, 'theme/support-center.html', {'items': items, **more})


class SubmitTicket(View):

    def get(self, request, more={}):
        return render(request, 'theme/submit-ticket.html', {**more})

    def post(self, request):
        object_data = {
            'email': request.POST.get('email', ''),
            'topic': request.POST.get('topic', ''),
            'content': request.POST.get('content', ''),
            'attached_files': request.POST.get('attached_files', ''),
            'created_at': datetime.now(),
            'transaction': None,
            'is_dispute': False,
            'ticket_manager': current_user(request) if current_user(request) else None,
            'ticket_priority': 'Low'
        }
        ticket = models.Tickets()
        ticket.__dict__.update(object_data)
        ticket.save()
        return self.get(request, {'alert': {'success': 'Submit ticket success!!'}})

class TicketDetails(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Tickets.objects.get(id=item_id)
        return render(request, 'theme/ticket-details.html', {'item': item, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class ProfileOverview(View):

    def get(self, request, more={}):
        return render(request, 'theme/profile-overview.html', {**more})

    def post(self, request):
        password_old = request.POST.get('password_old', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        avatars = request.POST.get('avatar', '')
        object_data = {
            'email': request.POST.get('email', ''),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'billing_address': request.POST.get('billing_address', ''),
            'overview': request.POST.get('overview', ''),
            'phonenumber': request.POST.get('phonenumber', ''),
            'use_2factor_authentication': True if request.POST.get('use_2factor_authentication') == 'on' else False,
        }
        user = current_user(request)
        user.__dict__.update(object_data)

        if password and check_password(password_old, user.password) and password == password_confirm:
            user.password = make_password(password)
        elif password:
            return self.get(request, {'error': {'password_old': 'Incorrect Password!'}})

        lists = avatars.split(',') if avatars else []
        if len(lists) > 0:
            print(lists)
            avatar = models.Medias.objects.get(id=lists[-1])
            user.avatar = avatar

        user.save()
        return self.get(request, {'alert': {'success': 'Profile updated successfully!'}})

@method_decorator(customer_user_login_required, name='dispatch')
class ReceivedOffers(View):

    def get(self, request, more={}):
        items = models.CounterOffers.objects.filter(Q(offer__created_by=current_user(request).customer(), status='pending') | Q(created_by=current_user(request).customer(), status='accepted')).order_by('-created_at')[:3]
        return render(request, 'theme/received-offers.html', {'items': items, **more})

    def post(self, request):
        item_id = request.POST.get('item_id', '')
        mode = request.POST.get('mode', '')
        try:
            item = models.CounterOffers.objects.get(id=item_id)
            item.status = mode
            item.save()
            return JsonResponse({'success': 'Declined!'})
        except:
            return JsonResponse({'error': 'Error! Try again.'})

@method_decorator(customer_user_login_required, name='dispatch')
class BuySellCoins(View):

    def get(self, request, more={}):
        return render(request, 'theme/index.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class Funding(View):

    def get(self, request, more={}):
        return render(request, 'theme/fund.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class UserPublicProfile(View):

    def get(self, request, more={}):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Customers.objects.get(id=item_id)
        items = models.Offers.objects.filter(created_by=item, is_expired=False)
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = app_url+'/user-public-profile/?'
        return render(request, 'theme/user-public-profile.html', {'customer': item, 'items': items, 'paginator' : paginator, 'base_url': base_url,  **more})


@method_decorator(customer_user_login_required, name='dispatch')
class OfferActivity(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Offers.objects.get(id=item_id)
        return render(request, 'theme/offer-activity.html', {'item': item, **more})

    def post(self, request):
        item_id = request.POST.get('item_id', '')
        item = models.Offers.objects.get(id=item_id)
        item.is_paused = True
        item.paused_by = current_user(request)
        item.save()
        return self.get(request, {'item_id': item_id, 'offer_error': 'Your Offer is paused by moderator.'})


@method_decorator(customer_user_login_required, name='dispatch')
class EditOffer(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Offers.objects.get(id=item_id)
        return render(request, 'theme/edit-offer.html', {'item': item, **more})

    def post(self, request):
        item_id = request.POST.get('item_id', '')
        trade_price = float(request.POST.get('trade_price', 0))
        if request.POST.get('useMarketPrice', '').strip() == 'on':
            trade_price = 123#[[[?]]]
        if request.POST.get('trailMarketPrice', '').strip() == 'on':
            trade_price = 123#[[[?]]]
        try:
            offer = models.Offers.objects.get(id=item_id)
            object_data = {
                'what_crypto': request.POST.get('what_crypto'),
                'flat': request.POST.get('flat'),
                'postal_code': request.POST.get('postal_code'),
                'show_postcode': True if request.POST.get('show_postcode') == 'on' else False,
                'country': request.POST.get('country'),
                'city': request.POST.get('city'),
                'trade_price': trade_price,
                'profit_start': float(request.POST.get('profit_start')) if request.POST.get('profit_start', None) != '' else None,
                'profit_end': float(request.POST.get('profit_end')) if request.POST.get('profit_end', None) != '' else None,
                'profit_time': request.POST.get('profit_time'),
                'minimum_transaction_limit': request.POST.get('minimum_transaction_limit'),
                'maximum_transaction_limit': request.POST.get('maximum_transaction_limit'),
                'operating_hours_start': request.POST.get('operating_hours_start'),
                'operating_hours_end': request.POST.get('operating_hours_end'),
                'restrict_hours_start': request.POST.get('restrict_hours_start'),
                'restrict_hours_end': request.POST.get('restrict_hours_end'),
                'proof_times': request.POST.get('proof_times'),
                'supported_location': request.POST.getlist('supported_location[]'),
                'trade_overview': request.POST.get('trade_overview', '').strip(),
                'message_for_proof': request.POST.get('message_for_proof', '').strip(),
                'identified_user_required': True if request.POST.get('identified_user_required') == 'on' else False,
                'sms_verification_required': True if request.POST.get('sms_verification_required') == 'on' else False,
                'minimum_successful_trades': request.POST.get('minimum_successful_trades'),
                'minimum_complete_trade_rate': request.POST.get('minimum_complete_trade_rate'),
                'admin_confirmed': False,
                'created_by': current_user(request),
                'created_at': datetime.now(),
            }

            offer.__dict__.update(object_data)
            offer.save()
            return OfferActivity.get(OfferActivity, request, {'item_id': offer.pk, 'offer_success': 'Offer Posted'})
        except:
            return OfferActivity.get(OfferActivity, request, {'item_id': offer.pk, 'offer_error': 'Your Offer is not running. Ref: RD23. <a href="'+app_url+'/issue?name=RD23">Find out</a> what it means'})


@method_decorator(customer_user_login_required, name='dispatch')
class AllOffers(View):

    def get(self, request, more={}):
        items = models.Offers.objects.order_by('-created_at').filter(created_by=current_user(request))
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = app_url+'/all-offers/?'
        return render(request, 'theme/all-offers.html', {'items': items, 'paginator' : paginator, 'base_url': base_url, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class OfferDetail(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Offers.objects.get(id=item_id)
        return render(request, 'theme/offer-details.html', {'item': item, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class OfferListing(View):

    def get(self, request, more={}):
        trade_type = request.GET.get('trade_type', '')
        what_crypto = request.GET.get('what_crypto', '')
        trade_price = request.GET.get('trade_price') if request.GET.get('trade_price') else 0
        flat = request.GET.get('flat', '')
        payment_method = request.GET.get('payment_method', '')
        
        crypto_filter = request.GET.get('crypto_filter', '')
        type_all = []
        type_BTC = []
        type_ETH = []
        type_XRP = []
        type_all.append('buy' if  request.GET.get('crypto_all_buy', 'no') == 'on' else 'no')
        type_BTC.append('buy' if  request.GET.get('crypto_BTC_buy', 'no') == 'on' else 'no')
        type_ETH.append('buy' if  request.GET.get('crypto_ETH_buy', 'no') == 'on' else 'no')
        type_XRP.append('buy' if  request.GET.get('crypto_XRP_buy', 'no') == 'on' else 'no')
        type_all.append('sell' if request.GET.get('crypto_all_sell', 'no') == 'on' else 'no')
        type_BTC.append('sell' if request.GET.get('crypto_BTC_sell', 'no') == 'on' else 'no')
        type_ETH.append('sell' if request.GET.get('crypto_ETH_sell', 'no') == 'on' else 'no')
        type_XRP.append('sell' if request.GET.get('crypto_XRP_sell', 'no') == 'on' else 'no')
        if crypto_filter == 'true':
            items = models.Offers.objects.filter(
                Q(what_crypto='BTC', trade_type__in=type_BTC) | 
                Q(what_crypto='ETH', trade_type__in=type_ETH) | 
                Q(what_crypto='XRP', trade_type__in=type_XRP) | 
                Q(trade_type__in=type_all)
                ).order_by('-created_at')
        else:
            if int(trade_price) > 0:
                items = models.Offers.objects.filter(trade_type__contains=trade_type, what_crypto__contains=what_crypto, flat__contains=flat, 
                minimum_transaction_limit__lte=trade_price, maximum_transaction_limit__gte=trade_price).order_by('-created_at')
            else:
                items = models.Offers.objects.filter(trade_type__contains=trade_type, what_crypto__contains=what_crypto, flat__contains=flat).order_by('-created_at')

        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = app_url+'/offer-listing/?'
        return render(request, 'theme/offer-listing.html', {'items': items, 'paginator' : paginator, 'base_url': base_url,
            'trade_type': trade_type, 'what_crypto': what_crypto, 'trade_price': trade_price, 'flat': flat, 'payment_method': payment_method, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class BuyListing(View):

    def get(self, request, more={}):
        return render(request, 'theme/index.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class SellListing(View):

    def get(self, request, more={}):
        return render(request, 'theme/index.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class SingleOfferDetail(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Offers.objects.get(id=item_id)
        return render(request, 'theme/single-offer-details.html', {'item': item, **more})
    
    def post(self, request):
        item_id = request.POST.get('item_id', '')
        offer = models.Offers.objects.get(id=item_id)
        try:
            list = models.Lists.objects.get(offer=offer, created_by=current_user(request).customer())
            return self.get(request, {'item_id': item_id, 'alert': {'warning': 'Already listed.'}})
        except:
            list = models.Lists(
                offer=offer,
                created_by=current_user(request).customer()
            )
            list.save()
            return self.get(request, {'item_id': item_id, 'alert': {'success': 'Added to your list.'}})


@method_decorator(customer_user_login_required, name='dispatch')
class InitiateTrade(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        return render(request, 'theme/initiate-trade.html', {'offer_id': item_id, **more})

    def post(self, request):
        offer_id = request.POST.get('offer_id', '')
        offer = models.Offers.objects.get(id=offer_id)
        if offer.is_started():
            return self.get(request, {'item_id': offer_id, 'alert': {'warning': 'Warning! Already started. ' + ('<a href="'+app_url+'/trade-processed?item_id='+str(offer.is_started().id)+'">go to trade.</a>' if offer.is_started() else '')}})
        payment_method = request.POST.get('payment_method', '')
        amount = request.POST.get('amount', '')
        try:
            trade = models.Trades()
            trade.offer = offer
            trade.payment_method = payment_method
            trade.amount = amount
            trade.status = True
            trade.vendor = current_user(request).customer()
            trade.created_at = datetime.now()
            trade.save()
            escrow = models.Escrows()
            escrow.trade = trade
            escrow.held_for = trade.buyer()
            escrow.held_from = trade.seller()
            escrow.status = False
            escrow.amount = amount
            escrow.created_at = datetime.now()
            escrow.save()
            calculate_escrow(escrow.pk)
            return TradeProcessed.get(TradeProcessed, request, {'item_id': trade.pk, 'alert': {'success': 'Success intiate trade.'}})
        except Exception as e:
            print(e)
            return self.get(request, {'item_id': offer_id, 'alert': {'warning': 'Sorry, Try again.'}})


def caculateTrade(request):
    offer_id = request.POST.get('offer_id', '')
    offer = models.Offers.objects.get(id=item_id)
    payment_method = request.POST.get('payment_method', '')
    amount = request.POST.get('amount', '')
    return JsonResponse({
        'you_pay_amount': 400, 'you_pay_flat': 'USD',
        'you_get_amount': 1981, 'you_get_flat': 'XRP',
        'offerer_pay_amount': 18, 'offerer_pay_flat': 'XRP',
        'you_cover_amount': 9.5, 'you_cover_flat': 'XRP'
    })


@method_decorator(customer_user_login_required, name='dispatch')
class TradeProcessed(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Trades.objects.get(id=item_id)
        return render(request, 'theme/trade-processed.html', {'item': item, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class ProofOfTransaction(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Trades.objects.get(id=item_id)
        return render(request, 'theme/proof-of-transaction.html', {'item': item, **more})

    def post(self, request):
        trade_id = request.POST.get('trade_id', '')
        trade = models.Trades.objects.get(id=trade_id)
        gift_card_code = request.POST.get('gift_card_code', '')
        reference_number = request.POST.get('reference_number', '')
        proof_documents = request.POST.get('proof_documents', '')
        proof_not_opened = request.POST.get('proof_not_opened', '')
        try:
            trade.gift_card_code = gift_card_code
            trade.reference_number = reference_number
            trade.proof_documents = proof_documents
            trade.proof_not_opened = proof_not_opened
            trade.trade_date = datetime.now()
            trade.trade_complete = False
            trade.trade_status = False
            trade.save()
            return redirect(app_url+'/trade-complete?item_id='+trade_id)
        except Exception as e:
            print(e)
            return self.get(request, {'item_id': trade_id, 'alert': {'warning': 'Sorry, Try again.'}})


@method_decorator(customer_user_login_required, name='dispatch')
class TradeComplete(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Trades.objects.get(id=item_id)
        return render(request, 'theme/trade-complete.html', {'item': item, **more})

    def post(self, request):
        trade_id = request.POST.get('trade_id', '')
        trade = models.Trades.objects.get(id=trade_id)
        review_rate = request.POST.get('rate', '')
        try:
            review = models.Reviews()
            review.trade = trade
            review.to_customer = trade.buyer() if trade.seller == current_user(request) else trade.seller()
            review.as_role = 'buyer' if trade.seller() == current_user(request) else 'seller'
            review.review_rate = review_rate
            review.created_by = current_user(request).customer()
            review.created_at = datetime.now()
            review.save()
            return self.get(request, {'item_id': trade_id, 'alert': {'success': 'Rate submited.'}})
        except Exception as e:
            print(e)
            return self.get(request, {'item_id': trade_id, 'alert': {'warning': 'Sorry, Try again.'}})


@method_decorator(customer_user_login_required, name='dispatch')
class SendCounterOffer(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        return render(request, 'theme/send-offer.html', {'offer_id': item_id, **more})

    def post(self, request):
        offer_id = request.POST.get('offer_id', '')
        offer = models.Offers.objects.get(id=offer_id)
        try:
            counter = models.CounterOffers()
            counter.offer = offer
            counter.created_by = current_user(request).customer()
            counter.price = request.POST.get('price', '')
            counter.flat = request.POST.get('flat', '')
            counter.message = request.POST.get('message', '').strip()
            counter.created_at = datetime.now()
            counter.status = 'pending'
            counter.save()
            return self.get(request, {'item_id': offer_id, 'alert': {'success': 'Sent your offer.'}})
        except Exception as e:
            print(e)
            return self.get(request, {'item_id': offer_id, 'alert': {'warning': 'Sorry, Try again.'}})



@method_decorator(customer_user_login_required, name='dispatch')
class WatchList(View):

    def get(self, request, more={}):
        user = current_user(request)
        items = models.Lists.objects.filter(created_by=current_user(request).customer()).order_by('-created_at')
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number)
        base_url = app_url+'/watch-list/?'
        return render(request, 'theme/watch-list.html', {'items': items, 'paginator' : paginator, 'base_url': base_url, **more})
    
    def post(self, request):
        item_id = request.POST.get('item_id', '')
        item = models.Lists.objects.get(id=item_id)
        try:
            item.delete()
            return JsonResponse({'success': 'Successfuly removed.'})
        except:
            return JsonResponse({'error': 'ERROR! Try later.'})


@method_decorator(customer_user_login_required, name='dispatch')
class FlagFeedback(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Reviews.objects.get(id=item_id)
        return render(request, 'theme/flag-feedback.html', {'item': item, **more})
    
    def post(self, request):
        review_id = request.POST.get('review_id', '')
        review = models.Reviews.objects.get(id=review_id)
        reason = request.POST.get('reason', '')
        content = request.POST.get('content', '')
        try:
            flag_feedback = models.FlaggedFeedback()
            flag_feedback.review = review
            flag_feedback.reason = reason
            flag_feedback.content = content
            flag_feedback.created_by = current_user(request)
            flag_feedback.created_at = datetime.now()
            flag_feedback.save()
            return self.get(request, {'item_id': review_id, 'alert' : {'success': 'Successfuly saved.'}})
        except Exception as e:
            print(e)
            return self.get(request, {'item_id': review_id, 'alert' : {'warning': 'Not saved. Try later.'}})


@method_decorator(customer_user_login_required, name='dispatch')
class LeaveReview(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Reviews.objects.get(id=item_id)
        return render(request, 'theme/leave-review.html', {'item': item, **more})
    
    def post(self, request):
        item_id = request.POST.get('item_id', '')
        item = models.Reviews.objects.get(id=item_id)
        feedback = request.POST.get('feedback', '')
        try:
            item.feedback = feedback
            item.save()
            return self.get(request, {'item_id': item_id, 'alert' : {'success': 'Successfuly saved.'}})
        except:
            return self.get(request, {'item_id': item_id, 'alert' : {'warning': 'Not saved. Try later.'}})

@method_decorator(customer_user_login_required, name='dispatch')
class IndependentEscrow(View):

    def get(self, request, more={}):
        confirmed = request.GET.get('confirmed') if request.GET.get('confirmed') else 'opened'
        status = request.GET.get('status') if request.GET.get('status') else 'all'
        trade_id = request.GET.get('trade_id')
        trade = models.Trades.objects.get(id=trade_id)
        if status == 'all':
            items = models.Escrows.objects.filter(trade=trade, confirmed=confirmed)
        elif status == 'not_funded':
            items = models.Escrows.objects.filter(trade=trade, confirmed=confirmed, status=False)
        elif status == 'funded':
            items = models.Escrows.objects.filter(trade=trade, confirmed=confirmed, status=True)
        return render(request, 'theme/independent-escrow.html', {'items': items, 'trade_id': trade_id, 'status': status, 'confirmed': confirmed, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class VendorProofOfTransaction(View):

    def get(self, request, more={}):
        item_id = more['item_id'] if 'item_id' in more else request.GET.get('item_id', '')
        item = models.Trades.objects.get(id=item_id)
        return render(request, 'theme/vendor-proof-of-transaction.html', {'item': item, **more})

    def post(self, request):
        item_id = request.POST.get('item_id', '')
        try:
            item = models.Trades.objects.get(id=item_id)
            item.is_completed = True
            item.save()
            return self.get(request, {'item_id': item_id, 'alert' : {'success': 'Trade Approved.'}})
        except:
            return self.get(request, {'item_id': item_id, 'alert' : {'warning': 'Error!. Try later.'}})



@method_decorator(customer_user_login_required, name='dispatch')
class VPOFGiftCardSteps(View):

    def get(self, request, more={}):
        return render(request, 'theme/vpof-giftcard-steps.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class VPOFGiftCardOpenCode(View):

    def get(self, request, more={}):
        return render(request, 'theme/vpof-giftcard-open-code.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class Send(View):

    def get(self, request, more={}):
        return render(request, 'theme/send.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
def receive(request):

    return render(request, 'theme/receive.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class TransactionHistory(View):

    def get(self, request, more={}):
        return render(request, 'theme/transaction-history.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class SavedWallets(View):

    def get(self, request, more={}):
        return render(request, 'theme/saved-wallets.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class MyBalance(View):

    def get(self, request, more={}):
        return render(request, 'theme/my-balance.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class WithdrawFunds(View):

    def get(self, request, more={}):
        return render(request, 'theme/withdraw-funds.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class Deposits(View):

    def get(self, request, more={}):
        return render(request, 'theme/deposits.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class Withdrawals(View):

    def get(self, request, more={}):
        return render(request, 'theme/withdrawals.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class Messages(View):
    
    def get(self, request):
        return render(request, 'theme/messages.html', {})


@method_decorator(customer_user_login_required, name='dispatch')
class InvitationInMessage(View):

    def get(self, request, more={}):
        return render(request, 'theme/invitation-in-message.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class IdVerification(View):

    def get(self, request, more={}):
        return render(request, 'theme/id-verification.html', {**more})


@method_decorator(customer_user_login_required, name='dispatch')
class Notifications(View):

    def get(self, request, more={}):
        return render(request, 'theme/notifications.html', {**more})


class BlogListing(View):

    def get(self, request, more={}):
        items = models.Posts.objects.filter(status='Publish')
        page_number = request.GET.get('page', 1)
        items, paginator = do_paginate(items, page_number, 9)
        base_url = app_url+'/blog-listing/?'

        return render(request, 'theme/blog-listing.html', {'items': items, 'paginator' : paginator, 'base_url': base_url, **more})


class BlogDetail(View):

    def get(self, request, more={}):
        item_id = request.GET.get('item_id', '').strip()
        item = models.Posts.objects.get(id=item_id)
        return render(request, 'theme/blog-detail.html', {'item': item, **more})


@method_decorator(customer_user_login_required, name='dispatch')
class Vendors(View):

    def get(self, request, more={}):
        return render(request, 'theme/seller-directory.html', {**more})


class Contact(View):

    def get(self, request, more={}):
        return render(request, 'theme/contact.html', {**more})

    def post(self, request):
        fullname = request.POST.get('fullname', '')
        email_address = request.POST.get('email_address', '')
        use_my_email = request.POST.get('use_my_email', '')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()
        customer = None
        if use_my_email == 'on':
            try:
                customer = models.Customers.objects.get(token=request.session['theme_user'])
                email_address = customer.email
            except:
                return self.get(request, {'error': {'email_address': 'Not valid email address.'}})
        elif email_address == '':
            return self.get(request, {'error': {'email_address': 'Email address is required.'}})

        contact = models.Contacts()
        contact.fullname = fullname
        contact.email_address = email_address
        contact.subject = subject
        contact.content = content
        contact.customer = customer
        contact.ip_address = get_client_ip(request)
        contact.save()

        return self.get(request, {'alert': {'success': 'Message is sent successfuly. We will contact you soon.'}})


@method_decorator(customer_user_login_required, name='dispatch')
class Referrals(View):

    def get(self, request, more={}):
        return render(request, 'theme/referrals.html', {**more})


class Buy(View):
    
    def get(self, request):
        template_name = 'theme/buy-listing.html'
        if request.LANGUAGE_CODE == 'zh-hans':
            template_name = 'theme/landing-china-all-coins.html'
        items = models.Trades.objects.filter(status=True).order_by('-created_at')[:5]
        return render(request, template_name, {'items': items})


@method_decorator(customer_user_login_required, name='dispatch')
class AddMessage(View):
    
    def post(self, request):
        message_type = request.POST.get('message_type', '')
        if message_type == 'ticket':
            ticket_id = request.POST.get('ticket_id', '')
            ticket = models.Tickets.objects.get(id=ticket_id)
            content = request.POST.get('content', '')
            writer = current_user(request)

            try:
                message = models.Messages()
                message.message_type = message_type
                message.ticket = ticket
                message.content = content
                message.writer = writer
                message.created_at = datetime.now()
                message.save()
                return TicketDetails.get(TicketDetails, request, {'item_id': ticket_id, 'alert': {'success': 'Added.'}})
            except Exception as e:
                print(e)
                return TicketDetails.get(TicketDetails, request, {'item_id': ticket_id, 'alert': {'warning': 'ERROR! Try again.'}})
        


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


from cadmin.form import MediasForm

@method_decorator(customer_user_login_required, name='dispatch')
class UploadView(View):

    def post(self, request):
        form = MediasForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            media = form.save()
            media.created_by = current_user(request)
            media.save()
            data = {'is_valid': True, 'name': media.file.name, 'url': media.file.url, 'id': media.pk}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def calculate_escrow(escrow_id):
    return True
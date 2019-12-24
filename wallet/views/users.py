import logging
import re
import uuid

from wallet import forms
from wallet import models
from month.models import Month

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import views as auth_views
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


class AffiliatesView(View):
    """
    View class for the affiliates page
    """

    def get(self, request):
        return render(request, 'affiliates.html')


class BalanceView(View):
    """
    View class for the balance page
    """

    def get(self, request):
        return render(request, 'balance.html')


class DisputeDetailsView(View):
    """
    View class for the dispute-details page
    """

    def get(self, request):
        return render(request, 'dispute-details.html')


class EscrowsView(LoginRequiredMixin, View):
    """
    View class for the escrows page
    """

    def get(self, request):
        return render(request, "independent-escrow.html")


class FundingView(LoginRequiredMixin, View):
    """
    View class for the funding page
    """

    def get(self, request):
        trades_count = request.user.get_trades_count()
        trade_partners = request.user.get_trade_partners()
        blocked_by = request.user.blocked_by.count()
        trusted_by = request.user.trusted_by.count()

        return render(request, 'fund.html', {
            'trades_count': trades_count,
            'trade_partners': trade_partners,
            'blocked_by': blocked_by,
            'trusted_by': trusted_by,
            'profile_photo': request.user.profile_photo,
        })

    def post(self, request):
        def _strip_cc_numbers(cc_number):
            re.sub(r'[^0-9]+', '', cc_number)
            return cc_number

        # def _find_cc_type(cc_number):
        #     cc_regexes = {
        #         'V': r'^4[0-9]{12}(?:[0-9]{3})?$',
        #         'M': r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',
        #         'A': r'^3[47][0-9]{13}$'
        #     }
        #     for cc_type, cc_regex in cc_regexes.items():
        #         if re.search(cc_regex, cc_number):
        #             return cc_type
        #     return None

        trades_count = request.user.get_trades_count()
        trade_partners = request.user.get_trade_partners()
        blocked_by = request.user.blocked_by.count()
        trusted_by = request.user.trusted_by.count()

        form = forms.CCCreationForm(request.POST)
        if form.is_valid():
            temp_card = models.CreditCard(
                reason=form.cleaned_data['reason'],
                cc_currency=form.cleaned_data['cc_currency'],
                last_digits=_strip_cc_numbers(form.cleaned_data['cc_number'][:-4]),
                expiration_date=Month(
                    form.cleaned_data['expiration_date'].year,
                    form.cleaned_data['expiration_date'].month,
                ),
                name_on_card=form.cleaned_data['name_on_card'],
                user=request.user,
            )
            temp_card.save()
            return redirect('/funding')
        else:
            return render(request, 'fund.html', {
                'trades_count': trades_count,
                'trade_partners': trade_partners,
                'blocked_by': blocked_by,
                'trusted_by': trusted_by,
                'profile_photo': request.user.profile_photo,
                'form': form,
            })


class HistoryView(LoginRequiredMixin, View):
    """
    View class for the history page
    """

    def get(self, request):
        return render(request, 'trade-history.html')


class OverviewView(LoginRequiredMixin, View):
    """
    View class for the overview page
    """

    def get(self, request):
        trades_count = request.user.get_trades_count()
        trade_partners = request.user.get_trade_partners()
        blocked_by = request.user.blocked_by.count()
        trusted_by = request.user.trusted_by.count()
        profile_photo = request.user.profile_photo

        return render(request, 'overview.html', {
            'trades_count': trades_count,
            'trade_partners': trade_partners,
            'blocked_by': blocked_by,
            'trusted_by': trusted_by,
            'profile_photo': profile_photo,
        })

    def post(self, request):
        def generate_name(filename):
            ext = filename.split('.')[-1]
            filename = "%s.%s" % (uuid.uuid4(), ext)
            return filename

        trades_count = request.user.get_trades_count()
        trade_partners = request.user.get_trade_partners()
        blocked_by = request.user.blocked_by.count()
        trusted_by = request.user.trusted_by.count()

        form = forms.UserOverviewForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile_picture = request.FILES['profile_photo']
            request.user.profile_photo.save(generate_name(user_profile_picture.name), user_profile_picture)
            for key, element in form.cleaned_data.items():
                if element and key != 'profile_photo':
                    setattr(request.user, key, element)
            request.user.full_name = request.user.first_name + ' ' + request.user.last_name
            request.user.save()

        return render(request, 'overview.html', {
            'trades_count': trades_count,
            'trade_partners': trade_partners,
            'blocked_by': blocked_by,
            'trusted_by': trusted_by,
            'form': form,
            'profile_photo': request.user.profile_photo,
        })


class ReferView(LoginRequiredMixin, View):
    """
    View class for the refer page
    """

    def get(self, request):
        return render(request, 'refer.html')


class VerificationView(View):
    """
    Class used for verification page
    """

    def get(self, request):
        return render(request, 'id-verification-a.html')


class VerificationBView(View):
    """
    Verification-B
    """

    def get(self, request):
        return render(request, 'id-verification-b.html')


class WalletsView(LoginRequiredMixin, View):
    """
    View class for the wallets page
    """

    def get(self, request):
        return render(request, 'saved-wallets.html')


class RegistrationView(View):
    """
    View class
    """

    def get(self, request):
        return redirect('/index', permanent=True)

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            try:
                temp_user = models.User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                )
                temp_user.username = form.cleaned_data['email']
                temp_user.full_name = form.cleaned_data['full_name']
                temp_user.registration_reason = form.cleaned_data['registration_reason']
                temp_user.save()
                temp_user.send_email_validation_code()
                logger.info("User {} has been registered".format(temp_user.username))
            except:
                response = render(request, 'index.html', context={'registration_form': form})
                return response
            if request.META.get('HTTP_REFERER', ):
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect('/index')
        else:
            response = render(request, 'index.html', context={'registration_form': form})
            return response


class UserExistsView(View):
    """
    Class that is used as a helper to find if a user exists or not
    """

    def post(self, request):
        logger.info("Validation for {} is attempted".format(request.POST))
        try:
            models.User.objects.get(email=request.POST.get('email'))
            return JsonResponse('An user with this email already exists.', safe=False)
        except ObjectDoesNotExist:
            return JsonResponse('true', safe=False)


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Class that is used as a helper to find if a user exists or not
    """

    def get(self, request):
        return render(request, 'change-pw.html')

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password1'])
            return redirect(request.META.get('HTTP_REFERER', '/index'))
        else:
            return HttpResponseBadRequest(content='Invalid POST request')


class LogInView(auth_views.LoginView):
    """
    View used for logging in the users
    """

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.GET.get('next'), '/index')
        return render(request, 'index.html', context={'login_errors': True})

    def post(self, request):
        logout(request)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user.is_active:
                login(request, user)
                return redirect(request.META.get('HTTP_REFERER', '/index'))
        return render(request, 'index.html', {'login_errors': True, 'form': form})


class LogOutView(LoginRequiredMixin, auth_views.LogoutView):
    """
    Class that is used for logging out the user
    """

    def get(self, request, **kwargs):
        response = HttpResponseRedirect('/index')
        logout(request)
        return response


class ProofTransactionSlipView(LoginRequiredMixin, View):
    """
    View for the Transact Slip validation
    """

    def get(self, request):
        form = forms.ProofTransactionSlipForm()
        return render(request, 'send-transaction-slip.html', context={'form': form})

    def post(self, request):
        form = forms.ProofTransactionSlipForm(request.POST)
        if form.is_valid():
            new_transaction_slip = models.ProofTransactionSlip(
                user=request.user,
                name=form.cleaned_data['name'],
                date_of_transaction=form.cleaned_data['date_of_transaction'],
                reference_num=form.cleaned_data['reference_num'],
                total_amount_paid=form.cleaned_data['total_amount_paid']
            )
            new_transaction_slip.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'errors': form.errors})


class EditCreditCardView(LoginRequiredMixin, View):
    """
    View class used for editing credit card details
    """

    def get(self):
        pass

    def post(self):
        pass


class EmailConfirmationView(LoginRequiredMixin, View):
    """
    Class used for confirming user's email
    """

    def get(self, request):
        form = forms.EmailConfirmationKeyValidationForm(request.GET)
        if form.is_valid():
            confirmation_key = form.cleaned_data['key']
            request.user.confirm_email(confirmation_key)
            return redirect(request.META.get('HTTP_REFERER', '/index'))
        return HttpResponseBadRequest("Expected field confirmation_key absent or invalid")


class SendNewEmailView(LoginRequiredMixin, View):
    """
    Class that is called when the user clicks on -Resend Link- when their emails aren't activated
    """

    def get(self, request):
        request.user.send_email_validation_code()
        return redirect(request.META.get('HTTP_REFERER', '/index'))


class SendView(LoginRequiredMixin, View):
    """
    View class for the send page
    """

    def get(self, request):
        return render(request, 'send.html')


class DepositsAndWithdrawalsView(View):
    """
    View used for the deposits and withdrawals page
    """

    def get(self, request):
        return render(request, 'deposits-and-withdraws.html')


class PhoneActivationView(LoginRequiredMixin, View):
    """
    Class used for user's phone activation
    """
    def post(self, request):
        form = forms.UserPhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            request.user.send_phone_code(str(phone_number))
            request.user.phone_number = phone_number
            request.user.save()
            return JsonResponse({'status': 'success'})
        return HttpResponseBadRequest


class PhoneValidationView(LoginRequiredMixin, View):
    """
    Class used for validating the code sent by the user
    """
    def post(self, request):
        phone_number = str(request.user.phone_number)
        form = forms.UserPhoneNumberValidationForm(request.POST)
        if form.is_valid():
            validation_code = form.cleaned_data['code']
            verification_check = request.user.validate_phone_code(str(phone_number), validation_code)
            if verification_check.status == 'approved':
                request.user.phone_activated = True
                request.user.save()
            return JsonResponse({'status': 'success'})
        return HttpResponseBadRequest('Invalid validation code')


class ResendPhoneValidationView(LoginRequiredMixin, View):
    """
    Class used to resent user's validation code
    """
    def get(self, request):
        if request.user.phone_number and request.user.phone_confirmation_code_sent:
            request.user.send_phone_code(request.user.phone_number)
            return JsonResponse({'status': 'success'})
        return HttpResponseBadRequest('Invalid request')

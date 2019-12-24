from django.contrib.auth.forms import UserCreationForm
from django import forms
from wallet.models import User, ProofTransactionSlip, CreditCard, Trade, TRADE_TYPES
from wallet.models import CRYPTO_CHOICES, FIAT_CHOICES
import luhn
from phonenumber_field.formfields import PhoneNumberField

PAYMENT_METHODS = (
    ('cd', 'Cash Deposit'),
    ('bt', 'Bank Transfer'),
    ('p1', 'PayPal'),
    ('p2', 'Pingit'),
    ('cp', 'Cash (In Person)'),
    ('ag', 'Amazon Gift Card'),
    ('ig', 'iTunes Gift Card'),
    ('sg', 'Steam Gift Card'),
    ('o', 'Other')
)


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2', 'registration_reason')


class ProofTransactionSlipForm(forms.ModelForm):
    """
    Class used for defining the Proof Transaction Slip Form
    """
    class Meta:
        model = ProofTransactionSlip
        fields = ('name', 'date_of_transaction', 'reference_num', 'total_amount_paid')


class CCCreationForm(forms.ModelForm):
    """
    Class used for defining the credit card creation form
    """
    cc_number = forms.CharField(max_length=25, min_length=16)
    expiration_date = forms.DateField()
    security_code = forms.CharField(max_length=4)

    def clean_cc_number(self):
        data = self.cleaned_data['cc_number']
        if not luhn.verify(data):
            raise forms.ValidationError('Error: Credit card number fails Luhn validation')
        return data

    class Meta:
        model = CreditCard
        fields = ('name_on_card', 'reason', 'cc_currency')


class UserOverviewForm(forms.Form):
    """Class used for the User Overview page"""
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    language = forms.CheckboxSelectMultiple()
    first_name = forms.CharField(max_length=200, required=False)
    last_name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(required=False)
    billing_address = forms.CharField(max_length=200, required=False)
    profile_photo = forms.ImageField(required=False)


class FormAboveTheWave(forms.Form):
    """
    Class used for defining the form from above the wave
    """
    amount = forms.FloatField(label='How Much?')
    crypto_currency = forms.ChoiceField(choices=CRYPTO_CHOICES, label='What to Buy?')
    fiat_currency = forms.ChoiceField(choices=FIAT_CHOICES, label='What to Pay For?')
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS, label='Payment Method')


class NewTradeForm(forms.ModelForm):
    """
    Form used for creating a new trade
    """
    trade_type = forms.CharField(label='', widget=forms.RadioSelect(choices=TRADE_TYPES))

    class Meta:
        # TODO implement custom validation - if restrict hours is checked, validate opening and closing hours
        model = Trade
        opening_time = forms.TimeField(input_formats=['%H:%M:%S', '%H:%M', '%r'])
        closing_time = forms.TimeField(input_formats=['%H:%M:%S', '%H:%M', '%r'])
        fields = ['trade_type', 'crypto_currency', 'fiat_currency', 'trade_amount', 'city', 'country',
                  'postcode', 'hide_postcode', 'price', 'minimum_transaction_limit',
                  'maximum_transaction_limit', 'trail_market_price', 'restrict_hours',
                  'opening_time', 'closing_time', 'trade_terms', 'track_liquidity',
                  'identified_people_only', 'sms_verification_required', 'check_successful_trades',
                  'minimum_successful_trades', 'preferred_payment_method']
        labels = {
            'crypto_currency': "What Crypto?",
            'fiat_currency': "What Fiat?",
            'city': 'Enter City',
            'country': "Select Country",
            'postcode': 'Enter Postcode',
        }


class UserPhoneNumberValidationForm(forms.Form):
    """
    Form used for submitting the user's code for authenticating his phone number
    """
    code = forms.CharField(max_length=6)


class UserPhoneNumberForm(forms.Form):
    """
    Form used for submitting user's phone number on phone validation
    """
    phone_number = PhoneNumberField()


class EmailConfirmationKeyValidationForm(forms.Form):
    """
    Form used for validating the confirmation key
    """
    confirmation_key = forms.CharField(max_length=40)

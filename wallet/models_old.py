from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from month.models import MonthField
from phonenumber_field.modelfields import PhoneNumberField
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from django_countries.fields import CountryField
import os


FIAT_CHOICES = (
    ('USD', 'US Dollars'),
    ('EUR', 'Euro'),
    ('GBP', 'Great British Pound'),
    ('JPY', 'Japanese Yen'),
)

CRYPTO_CHOICES = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('XRP', 'Ripple'),
)

CURRENCY_CHOICES = FIAT_CHOICES[1:] + CRYPTO_CHOICES[1:]

REGISTRATION_CHOICES = (
    ('BUY', 'I want to buy'),
    ('SELL', 'I want to sell'),
)

CC_TYPES = (
    ('V', 'Visa'),
    ('M', 'Master Card'),
    ('A', 'American Express')
)

LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    ('Chinese', 'Chinese'),
    ('Japanese', 'Japanese'),
    ('Arabic', 'Arabic'),
    ('Portuguese', 'Portuguese'),
    ('Russian', 'Russian'),
    ('German', 'German'),
    ('Hindi', 'Hindi'),
    ('Urdu', 'Urdu')
)

TICKET_STATUS_CHOICES = (
    ('p', 'Pending'),
    ('s', 'Solved')
)

TRADE_TYPES = (
    ('sell', 'Sell'),
    ('buy', 'Buy'),
)

PAYMENT_METHODS = (
    ('cash_deposit', 'Cash Deposit'),
    ('bank_transfer', 'Bank Transfer'),
    ('paypal', 'PayPal'),
    ('pingit', 'Pingit'),
    ('cash_in_person', 'Cash (In Person)'),
    ('amazon_gc', 'Amazon Gift Card'),
    ('itunes_gc', 'iTunes Gift Card'),
    ('steam_gc', 'Steam Wallet Gift Card'),
    ('other', 'Other')
)


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    """
    User class for Raplev, created based on the Django user
    """

    full_name = models.TextField(max_length=200)
    registration_reason = models.CharField(
        max_length=4,
        choices=REGISTRATION_CHOICES,
    )
    phone_number = PhoneNumberField()
    phone_activated = models.BooleanField(default=False)
    phone_confirmation_code_sent = models.BooleanField(default=False)
    confirmation_email_sent = models.BooleanField(default=False)
    feedback_score = models.FloatField(default=0.0)
    billing_address = models.CharField(max_length=100)
    blocked_users = models.ManyToManyField(
        'self',
        related_name='blocked_by',
        symmetrical=False
    )
    trusted_users = models.ManyToManyField(
        'self',
        related_name='trusted_by',
        symmetrical=False
    )
    registration_date = models.DateField(auto_now=True)
    profile_photo = models.ImageField(
        upload_to='user_profiles',
        null=True
    )

    def get_trades_count(self):
        return Trade.objects.filter(owner=self).count()

    def get_trade_partners(self):
        buyer_transactions = Transaction.objects.filter(buyer=self)
        seller_transactions = Transaction.objects.filter(seller=self)
        partner_set = set()
        for transaction in buyer_transactions:
            partner_set.add(transaction.seller)
        for transaction in seller_transactions:
            partner_set.add(transaction.buyer)
        return len(partner_set)

    def save_profile_picture(self, image_file, image_path):
        with open(os.path.join(settings.MEDIA_ROOT, 'user_profiles/', image_path), 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        self.profile_photo = image_path
        self.save()

    def can_start_transaction(self, trade):
        """
        Returns True if the user can start a transaction based on trade, false otherwise
        :param trade: The trade that needs validation
        :return: Boolean
        """
        return True

    def send_phone_code(self, phone_number):
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        verification = client.verify \
            .services(settings.TWILIO_VERIFICATION_SID) \
            .verifications \
            .create(to=phone_number, channel='sms')
        self.phone_confirmation_code_sent = True
        return verification.status

    def validate_phone_code(self, phone_number, validation_code):
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        verification_check = client.verify \
            .services(settings.TWILIO_VERIFICATION_SID) \
            .verification_checks \
            .create(to=phone_number, code=validation_code)
        return verification_check

    def send_email_validation_code(self):
        send_mail(
            subject='Welcome to Raplev',
            message='Use http://raplev.com/confirm_email?{} to confirm your email'.format(
                self.confirmation_key),
            from_email='admin@raplev.com',
            recipient_list=[self.email]
        )


class UserLanguages(models.Model):
    """
    Class used for defining the languages for the user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

    class Meta:
        unique_together = (('user', 'language'),)


class Balance(models.Model):
    """
    Class used for describing the current user's balance
    """

    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD',
    )
    amount = models.IntegerField()


class Account(models.Model):
    """
    Class used for describing the current user's bank and crypto accounts
    """

    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='BTC',
    )
    description = models.TextField()
    address = models.CharField(max_length=60)
    name = models.CharField(max_length=200)


class Trade(models.Model):
    """
    Class used for defining the Trade model
    """
    owner = models.ForeignKey(
        'User',
        on_delete=models.PROTECT
    )
    trade_type = models.CharField(max_length=20, choices=TRADE_TYPES)
    creation_date = models.DateTimeField(default=timezone.now())
    crypto_currency = models.CharField(max_length=3, choices=CRYPTO_CHOICES, default='BTC')
    fiat_currency = models.CharField(max_length=3, choices=FIAT_CHOICES, default='BTC')
    trade_amount = models.FloatField()
    city = models.CharField(max_length=200)
    country = CountryField()
    postcode = models.CharField(max_length=30)
    hide_postcode = models.BooleanField(default=False)

    price = models.FloatField()
    minimum_transaction_limit = models.IntegerField()
    maximum_transaction_limit = models.IntegerField()
    trail_market_price = models.BooleanField(default=False)
    preferred_payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='bank_transfer')

    restrict_hours = models.BooleanField(default=False)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    trade_terms = models.TextField()
    track_liquidity = models.BooleanField(default=False)
    identified_people_only = models.BooleanField(default=False)
    sms_verification_required = models.BooleanField(default=False)
    check_successful_trades = models.BooleanField(default=False)
    minimum_successful_trades = models.IntegerField(null=True, blank=True)

    @staticmethod
    def get_n_newest_trades(n, crypto_currency):
        """
        Returns the newest trades, based on their crypto currency. Used on the first page
        :param n:
        :param crypto_currency:
        :return:
        """
        trades = Trade.objects.filter(crypto_currency=crypto_currency).filter(trade_type='sell').order_by('-pk')
        if len(trades) >= n:
            return trades[:n]
        else:
            return trades

    @staticmethod
    def search(amount, crypto, fiat, payment_method):
        trades = Trade.objects.filter(crypto_currency=crypto.upper()).filter(fiat_currency=fiat.upper()).\
            filter(minimum_transaction_limit__lte=amount).filter(maximum_transaction_limit__gte=amount).\
            filter(preferred_payment_method=payment_method).values()
        return trades

    @staticmethod
    def search_alternatives(amount, crypto, fiat, payment_method):
        trades = Trade.objects.filter(crypto_currency=crypto.upper()).filter(fiat_currency=fiat.upper()). \
            filter(minimum_transaction_limit__lte=amount).filter(maximum_transaction_limit__gte=amount)
        optional_methods = ('cash_deposit', 'bank_transfer', 'cash_in_person', 'paypal')
        result = []
        for method in optional_methods:
            if method == payment_method:
                continue
            result.extend(trades.filter(preferred_payment_method=method).values())
        return result


class PaymentProcessor(models.Model):
    pass


class BankingProcessor(models.Model):
    pass


class BitcoinProcessor(models.Model):
    pass


class EthereumProcessor(models.Model):
    pass


class RippleProcessor(models.Model):
    pass


class Transaction(models.Model):
    """
    Class used for defining the Transaction model
    """
    seller = models.ForeignKey(
        'User',
        related_name='seller',
        on_delete=models.PROTECT
    )
    buyer = models.ForeignKey(
        'User',
        related_name='buyer',
        on_delete=models.PROTECT
    )
    seller_account = models.ForeignKey(
        'Account',
        related_name='seller_account',
        on_delete=models.PROTECT,
        null=True
    )
    buyer_account = models.ForeignKey(
        'Account',
        related_name='buyer_account',
        on_delete=models.PROTECT,
        null=True
    )
    seller_pp = models.ForeignKey(
        'PaymentProcessor',
        related_name='seller_pp',
        on_delete=models.PROTECT,
        null=True
    )
    buyer_pp = models.ForeignKey(
        'PaymentProcessor',
        related_name='buyer_pp',
        on_delete=models.PROTECT,
        null=True
    )
    trade = models.ForeignKey(
        'Trade',
        on_delete=models.PROTECT,
        null=True
    )
    description = models.TextField()


class CreditCard(models.Model):
    """
    Class used for defining credit cards details belonging to users
    """
    reason = models.CharField(max_length=3, choices=CRYPTO_CHOICES)
    cc_currency = models.CharField(max_length=3, choices=FIAT_CHOICES)
    last_digits = models.CharField(
        max_length=4,
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(4),
            validators.RegexValidator(r"\d\d\d\d")
        ]
    )
    expiration_date = MonthField()
    name_on_card = models.CharField(max_length=60)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProofTransactionSlip(models.Model):
    """
    Class used for the definition of Proof Transaction Slip
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_of_transaction = models.DateField()
    reference_num = models.CharField(max_length=40)
    total_amount_paid = models.FloatField()


class Ticket(models.Model):
    """
    Class used for defining the Tickets for disputes
    """
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    first_request = models.TextField()
    status = models.CharField(max_length=1, choices=TICKET_STATUS_CHOICES)

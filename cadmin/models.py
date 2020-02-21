from theme.constants import CAMPAIGN_STATUS_TYPES, BLOCK_TYPES, DRAWALS_CHOIES, ESCROWS_STATUS_TYPES, VOTE_TYPES, TRADE_STATUS_TYPES, FLAT_CHOICES, CRYPTO_CHOICES, CURRENCY_CHOICES,REGISTRATION_CHOICES,CC_TYPES,LANGUAGE_CHOICES,TICKET_STATUS_CHOICES,TRADE_TYPES,CUSTOMER_TYPES,PAYMENT_METHODS,ROLE_TYPES,BOOLEAN_TYPES,STATUS_TYPES,VERIFIED_TYPES,PENDING_TYPES,ACCEPTIVE_TYPES,PAGESTATUS_TYPES,COUNTRY_CODE

from django.db import models
from django.core.mail import send_mail
import random
import string
import timeago
from datetime import datetime, timezone
from raplev import settings
from django.db.models import Q, Sum, Count, F
from django.contrib.auth.models import AbstractUser
from bs4 import BeautifulSoup as bs
from crypto.models import BTC, ETH, XRP


class MyModelBase( models.base.ModelBase ):
    def __new__( cls, name, bases, attrs, **kwargs ):
        if name != "MyModel":
            class MetaB:
                db_table = "p127_" + name.lower()

            attrs["Meta"] = MetaB

        r = super().__new__( cls, name, bases, attrs, **kwargs )
        return r

class MyModel( models.Model, metaclass = MyModelBase ):
    class Meta:
        abstract = True


class Users(MyModel, AbstractUser):
    fullname = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, unique=True)
    email_verified = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255, null=True)
    phonenumber = models.CharField(max_length=255, null=True)
    phone_verified = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    id_verified = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    is_superuser = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    is_admin = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    is_customer = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    is_affiliate = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    is_staff = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    is_active = models.BooleanField(choices=BOOLEAN_TYPES, default=True)
    last_login = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ForeignKey('Medias', on_delete=models.CASCADE, null=True)
    overview = models.TextField(null=True)
    billing_address = models.CharField(max_length=255, null=True)
    use_2factor_authentication = models.BooleanField(default=False)
    organization = models.CharField(max_length=255, null=True)
    postcode = models.IntegerField(null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

    def customer(self):
        try:
            return Customers.objects.get(user=self)
        except:
            return None

    def admin(self):
        try:
            return Admin.objects.get(user=self)
        except:
            return None

    def affiliate(self):
        try:
            return Affiliates.objects.get(user=self)
        except:
            return None

    def get_fullname(self):
        try:
            return self.fullname if self.fullname else (self.first_name + ' ' +self.last_name)
        except:
            return self.username

    def id_cards_list(self):
        return UserIDs.objects.filter(user=self)

    def supported_language(self):
        return 'English, Germany'

    def send_info_email(self):
        send_mail(
            subject='Welcome to Raplev',
            message='Your Info: \n - Fullname: {}\n - Username: {}\n - Email: {}\n - Role: {}'.format(
                self.fullname, self.username, self.email, self.get_role_display()),
            from_email='admin@raplev.com',
            recipient_list=[self.email]
        )

    def send_forgot_pw_email(self, next=''):
        send_mail(
            subject='Please verify your Email.',
            message='Click <a href="'+settings.HOSTNAME+'/confirm-forgot-password-email?t='+self.token+next+'">here</a> to verify your email, or follow to this link.',
            from_email='admin@raplev.com',
            recipient_list=[self.email]
        )
        return settings.HOSTNAME+'/confirm-forgot-password-email?t='+self.token+next

    def send_confirm_email(self, next=''):
        send_mail(
            subject='Please verify your Email.',
            message='Click <a href="'+settings.HOSTNAME+'/verify-email?t='+self.token+next+'">here</a> to verify your email, or follow to this link.',
            from_email='admin@raplev.com',
            recipient_list=[self.email]
        )
        return settings.HOSTNAME+'/verify-email?t='+self.token+next

    def send_invite_email(self, invite_email, message, fullname):
        try:
            send_mail(
                subject='Invite from Raplev by '+self.get_fullname(),
                message='<h4>Hi, '+fullname+'</h4><p>'+message + '</p><p>Click <a href="'+settings.HOSTNAME+'/verify-email?t='+self.token+next+'">here</a> to try Raplev, or follow to this link.</p>',
                from_email='admin@raplev.com',
                recipient_list=[invite_email]
            )
            return True
        except:
            return False

    def send_email_code(self, email):
        send_mail(
            subject='Your CODE: '+self.token[3:8].upper(),
            message='Here is your verification CODE: '+self.token[3:8].upper(),
            from_email='admin@raplev.com',
            recipient_list=[email]
        )
        return self.token[3:8].upper()

    def send_phone_code(self, phonenumber):
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        verification = client.verify \
            .services(settings.TWILIO_VERIFICATION_SID) \
            .verifications \
            .create(to=phonenumber, channel='sms')
        return verification.status

    def validate_phone_code(self, phonenumber, validation_code):
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        verification_check = client.verify \
            .services(settings.TWILIO_VERIFICATION_SID) \
            .verification_checks \
            .create(to=phonenumber, code=validation_code)
        if verification_check:
            self.phonenumber = phonenumber
        return verification_check


class Admins(MyModel):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_TYPES, null=True)


class Customers(MyModel):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, null=True)
    seller_level = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username

    def get_public_url(self):
        return '<a href="/user-public-profile/?item_id='+str(self.pk)+'">'+self.user.username+'</a>'

    def review_list(self):
        return Reviews.objects.filter(to_customer=self)

    def other_open_offers_list(self):
        return Offers.objects.filter(created_by=self, is_expired=False)

    def balance_list(self):
        return Balance.objects.filter(customer=self)

    def balance(self):
        try:
            return str(self.balance_list()[0].amount) + ' ' + self.balance_list()[0].currency
        except:
            return ''

    def avail_sendup(self):
        try:
            return str(self.balance_list()[0].amount*0.8) + ' ' + self.balance_list()[0].currency
        except:
            return ''

    def average_trade_complete_time(self):
        return 3

    def trade_partners(self):
        return 3

    def trade_initiate_complete_rate(self):
        return 80

    def customer_rate(self):
        return 4.9

    def review_count(self):
        return 58

    def trade_count(self):
        return 3

    def successful_trade_count(self):
        return 2

    def successful_trade_rate(self):
        return round(self.successful_trade_count()/self.trade_count()*100)

    def unsuccessful_trade_count(self):
        return 1

    def trade_volumn(self):
        return 3

    def trusted_by_count(self):
        return 3

    def blocked_by_count(self):
        return 3

    def set_suspend(self):
        user = self.user
        user.is_customer = False
        user.save()
        return True

    def withdrawals(self):
        return DrawLists.objects.filter(created_by=self, draw_type='withdraw')[:20]

    def deposits(self):
        return DrawLists.objects.filter(created_by=self, draw_type='fund')[:20]
        
    def btc_wallet(self):
        try:
            return BTC.objects.get(customer=self)
        except:
            return None
        
    def eth_wallet(self):
        try:
            return ETH.objects.get(customer=self)
        except:
            return None
        
    def xrp_wallet(self):
        try:
            return XRP.objects.get(customer=self)
        except:
            return None


class Balance(MyModel):
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    amount = models.FloatField(default=0)


class UserIDs(MyModel):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    security_code = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()
    images = models.TextField(null=True)
    status = models.BooleanField(choices=ACCEPTIVE_TYPES, default=False)

    def images_list(self):
        lists = self.images.split(',') if self.images else []
        return Medias.objects.filter(id__in=lists)


class Medias(MyModel):
    file = models.FileField(upload_to='', null=True)
    created_by = models.ForeignKey('Users', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.url

    @property
    def created_by_name(self):
        return self.created_by.username

    @property
    def file_url(self):
        return self.file.url

    @property
    def file_name(self):
        return self.file.name


class Reviews(MyModel):
    to_customer = models.ForeignKey('Customers', on_delete=models.CASCADE, related_name='review_for')
    trade = models.ForeignKey('Trades', on_delete=models.CASCADE, null=True)
    as_role = models.CharField(max_length=255)
    review_rate = models.FloatField()
    feedback = models.TextField(null=True)
    created_by = models.ForeignKey('Customers', on_delete=models.CASCADE, related_name='review_by')
    created_at = models.DateTimeField()

    def is_flagged(self):
        try:
            return FlaggedFeedback.objects.get(review=self)
        except:
            return None


class FlaggedFeedback(MyModel):
    review = models.ForeignKey('Reviews', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    content = models.TextField(null=True)
    created_by = models.ForeignKey('Customers', on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Offers(MyModel):
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPES)
    what_crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    flat = models.CharField(max_length=10, choices=FLAT_CHOICES)
    postal_code = models.IntegerField(null=True)
    show_postcode = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    country = models.CharField(max_length=10, choices=COUNTRY_CODE)
    city = models.CharField(max_length=100, null=True)
    trade_price = models.FloatField(default=0)
    use_market_price = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    trail_market_price = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    profit_start = models.FloatField(null=True)
    profit_end = models.FloatField(null=True)
    profit_time = models.IntegerField()
    minimum_transaction_limit = models.IntegerField()
    maximum_transaction_limit = models.IntegerField()
    operating_hours_start = models.TimeField()
    operating_hours_end = models.TimeField()
    restrict_hours_start = models.TimeField()
    restrict_hours_end = models.TimeField()
    proof_times = models.IntegerField()
    supported_location = models.TextField(null=True)
    trade_overview = models.TextField()
    message_for_proof = models.TextField()
    identified_user_required = models.BooleanField(choices=BOOLEAN_TYPES)
    sms_verification_required = models.BooleanField(choices=BOOLEAN_TYPES)
    minimum_successful_trades = models.IntegerField()
    minimum_complete_trade_rate = models.IntegerField()
    admin_confirmed = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    created_by = models.ForeignKey('Customers', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    paused_by = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def supported_location_list(self):
        lists = self.supported_location if self.supported_location else []
        return lists

    def counter(self):
        try:
            return Trades.objects.get(offer=self, status='waiting')
        except:
            return None

    def relate_trades(self):
        return Trades.objects.filter(offer=self)

    def completed_trade(self):
        try:
            return Trades.objects.get(offer=self, status='completed')
        except:
            return None

    def get_trade_price(self):
        # if self.use_market_price:
        #     return Pricing.get_price(self.what_crypto, self.flat, 'market_price')
        # if self.trail_market_price:
        #     return Pricing.get_price(self.what_crypto, self.flat, 'trail_market_price')
        return "{:.3f}".format(self.trade_price)

    def payment_method(self):
        return 'All'

    def payment_risk(self):
        if self.trade_price > 10000:
            return 'High Risk'
        else:
            return 'Low Risk'

    def address(self):
        return self.city + ', ' + self.get_country_display() + (', ' + str(self.postal_code) if not self.show_postcode else '')

    def is_started(self):
        try:
            return Trades.objects.get(Q(offer=self), ~Q(status='waiting'))
        except:
            return None

    def bought_amount(self):
        if self.trade_type == 'buy':
            try:
                return self.completed_trade.amount
            except:
                return 0
        else:
            try:
                return self.completed_trade.flat_amount_completed()
            except:
                return 0

    def sold_amount(self):
        if self.trade_type == 'sell':
            try:
                return self.completed_trade.amount
            except:
                return 0
        else:
            try:
                return self.completed_trade.flat_amount_completed()
            except:
                return 0

    def bought_currency(self):
        if self.trade_type == 'buy':
            return self.what_crypto
        else:
            try:
                return self.completed_trade.trade_flat
            except:
                return '-'

    def sold_currency(self):
        if self.trade_type == 'sell':
            return self.what_crypto
        else:
            try:
                return self.completed_trade.trade_flat
            except:
                return '-'

    def status(self):
        if self.is_expired:
            return 'Expired'
        elif self.is_paused:
            return 'Paused'
        else:
            return 'Pending'

    def is_completed(self):
        return True if self.completed_trade() else False


class Trades(MyModel):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    offer = models.ForeignKey('Offers', on_delete=models.CASCADE)
    trade_initiator = models.ForeignKey('Customers', on_delete=models.CASCADE, null=True, related_name='trade_initiator_customer')
    vendor = models.ForeignKey('Customers', on_delete=models.CASCADE, related_name='vendor_customer')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    price = models.FloatField(null=True)
    flat = models.CharField(max_length=100, choices=FLAT_CHOICES, null=True)
    counter_status = models.CharField(max_length=10, null=True)
    message = models.TextField(null=True)
    amount = models.FloatField(null=True)
    status = models.CharField(max_length=10, choices=TRADE_STATUS_TYPES)
    proof_documents = models.TextField(null=True)
    reference_number = models.CharField(max_length=255, null=True)
    proof_gift_code = models.CharField(max_length=255, null=True)
    proof_opened = models.BooleanField(default=False)
    trade_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField()

    def is_gift_card(self):
        return True if '_gc' in self.payment_method else False

    def is_proofed(self):
        return True if self.proof_gift_code or self.reference_number else False

    def is_completed(self):
        return True if self.status == 'completed' else False

    def is_opened(self):
        return True if self.proof_opened else False

    def seller(self):
        return self.offer.created_by if self.offer.trade_type == 'sell' else self.vendor

    @property
    def seller_name(self):
        return self.seller().__str__
    
    def buyer(self):
        return self.offer.created_by if self.offer.trade_type == 'buy' else self.vendor

    @property
    def buyer_name(self):
        return self.buyer().__str__

    def offerer_review(self):
        try:
            return Reviews.objects.get(trade=self, to_customer=self.offer.created_by)
        except:
            return None

    def vender_review(self):
        try:
            return Reviews.objects.get(trade=self, to_customer=self.vendor)
        except:
            return None

    def escrow_amount(self):
        try:
            escrow = Escrows.objects.get(trade=self, status=True)
            return str(escrow.amount) + ' ' + escrow.trade.offer.what_crypto
        except:
            return 0

    def escrow_status(self):
        try:
            Escrows.objects.get(trade=self, status=True)
            return True
        except:
            return False

    @property
    def trade_price(self):
        return self.price if self.price else self.offer.trade_price

    @property
    def trade_flat(self):
        return self.flat if self.flat else self.offer.flat

    @property
    def trade_payment(self):
        return self.payment_method

    def proof_documents_list(self):
        try:
            string = self.proof_documents
            lists = string.split(',')
            return Medias.objects.filter(id__in=lists)
        except:
            return []

    def flat_amount_completed(self):
        return self.trade_price()*self.amount if self.status == 'completed' else 0

    def flat_amount(self):
        return float(self.trade_price) * float(self.amount)


class Pricing(MyModel):
    price_type = models.CharField(max_length=100) #market_price, trail_market_price
    crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    flat = models.CharField(max_length=10, choices=FLAT_CHOICES)
    price = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    created_by = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True)

    def get_price(self, crypto, flat, price_type='market_price'):
        item = Pricing.objects.filter(crypto=crypto, flat=flat, price_type=price_type).order_by('-created_by')
        try:
            return float("{:.3f}".format(item[0].price))
        except:
            return 0

    def get_rate(self, crypto, flat, price_type='market_price'):
        item = Pricing.objects.filter(crypto=crypto, flat=flat, price_type=price_type).order_by('-created_by')
        try:
            return float("{:.3f}".format(item[0].rate))
        except:
            return 0

class Escrows(MyModel):
    trade = models.ForeignKey('Trades', on_delete=models.CASCADE)
    held_for = models.ForeignKey('Customers', on_delete=models.CASCADE, related_name='escrows_held_for')
    held_from = models.ForeignKey('Customers', on_delete=models.CASCADE, related_name='escrows_held_from')
    status = models.BooleanField(choices=PENDING_TYPES)
    confirmed = models.CharField(max_length=10, default='opened', choices=ESCROWS_STATUS_TYPES)
    amount = models.FloatField()
    currency = models.CharField(max_length=100, null=True)
    transaction = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField()

    def trade_price(self):
        return self.trade.trade_price()


class Lists(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    created_by = models.ForeignKey('Customers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def is_updated(self):
        offers = Offers.objects.filter(updated_at__gt=self.created_at)
        return True if offers.count() > 0 else False


class Tickets(MyModel):
    email = models.CharField(max_length=255)
    trade = models.ForeignKey('Trades', on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=255)
    content = models.TextField(null=True)
    is_dispute = models.BooleanField(choices=PENDING_TYPES)
    ticket_manager = models.ForeignKey('Users', null=True, on_delete=models.CASCADE, related_name='manager_ticket')
    ticket_priority = models.CharField(max_length=10)
    attached_files = models.TextField(null=True)
    created_by = models.ForeignKey('Users', null=True, on_delete=models.CASCADE, related_name='created_by_tickete')
    created_at = models.DateTimeField()

    def attached_files_list(self):
        lists = self.attached_files.split(',') if self.attached_files else []
        return Medias.objects.filter(id__in=lists)

    def messages_list(self):
        return Messages.objects.filter(message_type='ticket', ticket=self).order_by('-created_at')


class Messages(MyModel):
    ticket = models.ForeignKey('Tickets', on_delete=models.CASCADE, null=True)
    message = models.ForeignKey('Messages', on_delete=models.CASCADE, null=True)
    partner = models.ForeignKey('Users', null=True, on_delete=models.CASCADE, related_name='messages_partner')
    writer = models.ForeignKey('Users', null=True, on_delete=models.CASCADE, related_name='messages_writer')
    content = models.TextField()
    message_type = models.CharField(max_length=100,null=True)
    readed = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    created_at = models.DateTimeField()

    def sub_messages(self):
        return Messages.objects.filter(message_type='sub_message', message=self)


class UserRelations(MyModel): #for message
    user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='relation_user')
    partner = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='relation_partner')
    status = models.BooleanField(default=True, choices=BLOCK_TYPES)
    viewed_at = models.DateTimeField(null=True)
    blocked_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()

    def unreaded_messages(self):
        return Messages.objects.filter(partner=self.user, writer=self.partner, readed=False)

    def unreaded_first_message(self):
        try:
            return Messages.objects.filter(partner=self.user, writer=self.partner, readed=False).order_by('created_at')[0]
        except:
            return None


class Contacts(MyModel):
    email_address = models.CharField(max_length=255)
    cc_email_address = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=255, null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    subject = models.TextField()
    content = models.TextField()
    ip_address = models.CharField(max_length=100)
    readed = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    created_at = models.DateTimeField()


class Revenue(MyModel):
    source = models.CharField(max_length=255)
    revenue_type = models.CharField(max_length=255)
    amount = models.FloatField()
    refund = models.FloatField()
    date = models.DateTimeField()


class Pages(MyModel):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey('Users', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAGESTATUS_TYPES)
    context = models.TextField()
    updated_on = models.DateTimeField()
    created_at = models.DateTimeField()


class Posts(MyModel):
    slug = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey('Users', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAGESTATUS_TYPES, default='Publish')
    context = models.TextField()
    tags = models.TextField(null=True)
    featured_images = models.TextField(null=True)
    disallow_comments = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField()

    def featured_images_list(self):
        lists = self.featured_images.split(',') if self.featured_images else []
        return Medias.objects.filter(id__in=lists)

    def first_featured_image(self):
        return self.featured_images_list()[:1]
    
    @property
    def posted_by_name(self):
        return self.posted_by.username
    
    @property
    def beauty_context(self):
        return text_from_html(self.context)[:300]

    @property
    def hidden_context(self):
        return text_from_html(self.context)[300:]

    def tags_list(self):
        return self.tags.split(',')

    def related_post_list(self):
        try:
            return Posts.objects.filter(~Q(id=self.id)).order_by('-created_at')[:3]
        except:
            return []

    @property
    def upvotes_count(self):
        return Votes.objects.filter(post=self, vote_type='up').count()

    @property
    def comments_count(self):
        return Comments.objects.filter(post=self).count()

    @property
    def comments_list(self):
        return Comments.objects.filter(post=self)

    @property
    def get_update_time(self):
        return 'Posted ' + timeago.format(self.updated_on, datetime.now(timezone.utc))


def text_from_html(html):
    soup = bs(html, 'html.parser')
    text = soup.text

    # output = ''
    # blacklist = [
    #     '[document]',
    #     'noscript',
    #     'header',
    #     'html',
    #     'meta',
    #     'head', 
    #     'input',
    #     'script',
    #     'img',
    #     # there may be more elements you don't want, such as "style", etc.
    # ]

    # for t in text:
    #     if t.parent.name not in blacklist:
    #         output += '{} '.format(t)
    return text


class Tags(MyModel):
    name = models.CharField(max_length=255)
    ongoing = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class LoginLogs(MyModel):
    user = models.ForeignKey('Users', null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    destination = models.CharField(default='raplev', max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class FlaggedPosts(MyModel):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    flagged_by = models.ForeignKey('Users', on_delete=models.CASCADE)
    flag_reason = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField()


class LandingPages(MyModel):
    template_page = models.ForeignKey('Pages', on_delete=models.CASCADE)
    personalized_link = models.CharField(max_length=255)
    redirection_type = models.CharField(max_length=255)


class PersLinks(MyModel):
    landing_page = models.ForeignKey('LandingPages', on_delete=models.CASCADE)
    personalized_link = models.CharField(max_length=255)
    assigned_to_user = models.CharField(max_length=255)
    leads = models.IntegerField()


class RedirectionLinks(MyModel):
    old_link = models.CharField(max_length=255)
    new_link = models.CharField(max_length=255)
    redirection_type = models.CharField(max_length=255)


class Issues(MyModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    attached_files = models.TextField()
    created_at = models.DateTimeField()


class Options(MyModel):
    option_type = models.CharField(max_length=255)
    option_param1 = models.CharField(default=None, max_length=255, null=True)
    option_param2 = models.CharField(default=None, max_length=255, null=True)
    option_param3 = models.CharField(default=None, max_length=255, null=True)
    option_field = models.CharField(max_length=255)
    option_value = models.TextField()


class SecurityStatus(MyModel):
    ip_address = models.CharField(max_length=255)
    user = models.ForeignKey('Users', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)


class Campaigns(MyModel):
    campaign_name = models.CharField(max_length=255)
    campaign_url = models.CharField(max_length=255)
    overview = models.TextField(null=True)
    status = models.BooleanField(default=False, choices=CAMPAIGN_STATUS_TYPES)
    target_location = models.TextField(null=True)
    creative_materials = models.TextField(null=True)
    owner = models.ForeignKey('Affiliates', null=True, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField()

    def creative_materials_list(self):
        lists = self.creative_materials.split(',') if self.creative_materials else []
        return Medias.objects.filter(id__in=lists)

    @property
    def owner_name(self):
        return self.owner.user.username

    @property
    def get_name(self):
        return self.campaign_name + (' ['+self.target_location+']' if self.target_location else '')

    @property
    def total_payouts(self):
        return Reports.objects.filter(campaign=self).aggregate(Sum('payout'))['payout__sum'] or 0

    @property
    def total_clicks(self):
        return Reports.objects.filter(campaign=self, report_field='click').count()

    @property
    def total_conversions(self):
        return Reports.objects.filter(campaign=self, report_field='conversion').count()


class Affiliates(MyModel):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)


class Reports(MyModel):
    lead_status = models.BooleanField(default=False)
    payout = models.IntegerField(default=0)
    campaign = models.ForeignKey('Campaigns', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    report_field = models.CharField(max_length=100)


class Comments(MyModel):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_by = models.ForeignKey('Users', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)

    def sub_comment_list(self):
        return Comments.objects.filter(comment=self)

    @property
    def posted_by_name(self):
        return self.created_by.username
    
    @property
    def beauty_context(self):
        return text_from_html(self.message)[:300]

    @property
    def hidden_context(self):
        return text_from_html(self.message)[300:]

    @property
    def upvotes_count(self):
        return Votes.objects.filter(comment=self, vote_type='up').count()

    @property
    def comments_count(self):
        return Comments.objects.filter(comment=self).count()

    @property
    def comments_list(self):
        return Comments.objects.filter(comment=self)

    @property
    def get_update_time(self):
        return 'Posted ' + timeago.format(self.created_at, datetime.now(timezone.utc))


class Votes(MyModel):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE, null=True)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_by = models.ForeignKey('Users', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)


class DrawLists(MyModel):
    draw_type = models.CharField(max_length=10, choices=DRAWALS_CHOIES)
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=10, null=True, choices=CURRENCY_CHOICES)
    details = models.TextField(null=True)
    card = models.ForeignKey('UserIDs', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey('Customers', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)


class SavedWallets(MyModel):
    crypto = models.CharField(max_length=10, null=True, choices=CRYPTO_CHOICES)
    description = models.TextField(null=True)
    created_by = models.ForeignKey('Customers', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    

class SendCryptos(MyModel):
    cryto_amount = models.FloatField(default=0)
    flat_amount = models.FloatField(default=0)
    receiver_email = models.CharField(max_length=255)
    currency = models.CharField(max_length=10, null=True, choices=CURRENCY_CHOICES)
    description = models.TextField(null=True)
    created_by = models.ForeignKey('Customers', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)

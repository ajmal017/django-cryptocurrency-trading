from django.db import models
from django.core.mail import send_mail


FLAT_CHOICES = (
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

CURRENCY_CHOICES = FLAT_CHOICES[1:] + CRYPTO_CHOICES[1:]

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
    ('sell', 'Selling'),
    ('buy', 'Buying'),
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

ROLE_TYPES = (
    ('AD', 'Admin'),
    ('MO', 'Moderator'),
    ('IV', 'ID Verifier'),
    ('BM', 'Blog Manager'),
    ('SM', 'SEO Manager'),
    ('SA', 'Support Agent'),
    ('CM', 'Community Moderator'),
    ('AM', 'Affiliate Manager')
)

BOOLEAN_TYPES = (
    (True, 'Yes'),
    (False, 'No'),
)

STATUS_TYPES = (
    (True, 'Active'),
    (False, 'Suspend'),
)

VERIFIED_TYPES = (
    (True, 'Verified'),
    (False, 'Unverified'),
)

PENDING_TYPES = (
    (True, 'Released'),
    (False, 'Pending'),
)

ACCEPTIVE_TYPES = (
    (True, 'Accepted'),
    (False, 'Rejected'),
)

PAGESTATUS_TYPES = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
    ('Trash', 'Trash'),
)


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

class Users(MyModel):
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_TYPES)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)

    def send_info_email(self):
        send_mail(
            subject='Welcome to Raplev',
            message='Your Info: \n - Fullname: {}\n - Username: {}\n - Email: {}\n - Role: {}'.format(
                self.fullname, self.username, self.email, self.get_role_display()),
            from_email='admin@raplev.com',
            recipient_list=[self.email]
        )


class Revenue(MyModel):
    source = models.CharField(max_length=255)
    revenue_type = models.CharField(max_length=255)
    amount = models.FloatField()
    refund = models.FloatField()
    date = models.DateTimeField()


class Offers(MyModel):
    address = models.CharField(max_length=255)
    flat = models.CharField(max_length=10, choices=FLAT_CHOICES)
    created_by = models.CharField(max_length=255)
    show_postcode = models.BooleanField(choices=BOOLEAN_TYPES)
    minimum_transaction_limit = models.IntegerField()
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPES)
    what_crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    maximum_transaction_limit = models.IntegerField()
    operating_hours_start = models.TimeField()
    operating_hours_end = models.TimeField()
    restrict_hours_start = models.TimeField()
    restrict_hours_end = models.TimeField()
    trade_overview = models.TextField()
    message_for_proof = models.TextField()
    identified_user_required = models.BooleanField(choices=BOOLEAN_TYPES)
    sms_verification_required = models.BooleanField(choices=BOOLEAN_TYPES)
    minimum_successful_trades = models.IntegerField()
    created_at = models.DateTimeField()


class Trades(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.PROTECT)
    trade_initiator = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.FloatField()
    status = models.CharField(max_length=255)
    proof_documents = models.TextField()
    proof_not_opened = models.CharField(max_length=255)
    proof_opened = models.CharField(max_length=255)
    created_at = models.DateTimeField()


class Customers(MyModel):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_verified = models.BooleanField(choices=BOOLEAN_TYPES)
    phone_verified = models.BooleanField(choices=BOOLEAN_TYPES)
    id_verified = models.BooleanField(choices=BOOLEAN_TYPES)
    seller_level = models.IntegerField()
    created_at = models.DateTimeField()
    suspended = models.BooleanField(default=False, choices=BOOLEAN_TYPES)


class Transactions(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.PROTECT)
    trade_initiator = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    txn = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.BooleanField(choices=STATUS_TYPES)


class Escrows(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.PROTECT)
    held_for = models.CharField(max_length=255)
    held_from = models.CharField(max_length=255)
    status = models.BooleanField(choices=PENDING_TYPES)
    amount = models.FloatField()


class Tickets(MyModel):
    transaction = models.ForeignKey(Transactions, on_delete=models.PROTECT)
    topic = models.CharField(max_length=255)
    is_dispute = models.BooleanField(choices=BOOLEAN_TYPES)
    ticket_manager = models.CharField(max_length=255)
    ticket_priority = models.CharField(max_length=10)


class Messages(MyModel):
    ticket = models.ForeignKey(Tickets, on_delete=models.PROTECT)
    writer = models.CharField(max_length=255)
    content = models.TextField()
    # attach_file = models.CharField(max_length=255)
    created_at = models.DateTimeField()


class Idcards(MyModel):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    document_type = models.CharField(max_length=100)
    document_file = models.CharField(max_length=255)
    status = models.BooleanField(choices=ACCEPTIVE_TYPES)


class Contacts(MyModel):
    email_address = models.CharField(max_length=255)
    subject = models.TextField()
    content = models.TextField()
    ip_address = models.CharField(max_length=100)
    readed = models.BooleanField(default=False, choices=BOOLEAN_TYPES)


class Pages(MyModel):
    title = models.CharField(max_length=255)
    posted_by = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=PAGESTATUS_TYPES)
    context = models.TextField()
    updated_on = models.DateTimeField()
    created_at = models.DateTimeField()


class Posts(MyModel):
    title = models.CharField(max_length=255)
    posted_by = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=PAGESTATUS_TYPES)
    context = models.TextField()
    tags = models.TextField()
    featured_images = models.TextField()
    disallow_comments = models.BooleanField(choices=BOOLEAN_TYPES)
    updated_on = models.DateTimeField()
    created_at = models.DateTimeField()


class Tags(MyModel):
    name = models.CharField(max_length=255)
    ongoing = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class Medias(MyModel):
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    file_size = models.FloatField()
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()


class LoginLogs(MyModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    destination = models.CharField(default='raplev', max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class FlaggedPosts(MyModel):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    flagged_by = models.CharField(max_length=255)
    flag_reason = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField()


class LandingPages(MyModel):
    template_page = models.ForeignKey(Pages, on_delete=models.PROTECT)
    personalized_link = models.CharField(max_length=255)
    redirection_type = models.CharField(max_length=255)


class PersLinks(MyModel):
    landing_page = models.ForeignKey(LandingPages, on_delete=models.PROTECT)
    personalized_link = models.CharField(max_length=255)
    assigned_to_user = models.CharField(max_length=255)
    leads = models.IntegerField()


class RedirectionLinks(MyModel):
    old_link = models.CharField(max_length=255)
    new_link = models.CharField(max_length=255)
    redirection_type = models.CharField(max_length=255)


class Options(MyModel):
    option_type = models.CharField(max_length=255)
    option_param1 = models.CharField(default=None, max_length=255, null=True)
    option_param2 = models.CharField(default=None, max_length=255, null=True)
    option_param3 = models.CharField(default=None, max_length=255, null=True)
    option_field = models.CharField(max_length=255)
    option_value = models.TextField()


class SecurityStatus(MyModel):
    ip_address = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)


class Campaigns(MyModel):
    campaign_name = models.CharField(max_length=255)
    campaign_url = models.CharField(max_length=255)
    overview = models.TextField()
    payout = models.IntegerField()
    campaign_type = models.CharField(max_length=100)
    target_location = models.TextField()
    creative_materials = models.TextField()
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    updated_on = models.DateTimeField()
    created_at = models.DateTimeField()


class Affiliates(MyModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postcode = models.IntegerField()
    country = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.BooleanField(default=False, choices=STATUS_TYPES)
    created_at = models.DateTimeField()

    def send_info_email(self):
        send_mail(
            subject='Welcome to Raplev',
            message='Your Info: \n - First Name: {}\n - Last Name: {}\n - Email: {}\n - Organization: {}\n - Address: {}\n - Postcode: {}\n - Country: {}\n - Created_at: {}\n'.format(
                self.first_name, self.last_name, self.email, self.organization, self.address, self.postcode, self.country, self.created_at),
            from_email='admin@raplev.com',
            recipient_list=[self.email]
        )
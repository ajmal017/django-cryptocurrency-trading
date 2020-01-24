from django.db import models
from django.core.mail import send_mail
import random
import string
from raplev import settings


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

CUSTOMER_TYPES = (
    ('buy', 'Seller'),
    ('sell', 'Buyer'),
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


COUNTRY_CODE = (
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia, Plurinational State of'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo, the Democratic Republic of the'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'CÃ´te d\'Ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CW', 'CuraÃ§ao'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French Southern Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GG', 'Guernsey'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HM', 'Heard Island and McDonald Islands'),
    ('VA', 'Holy See (Vatican City State)'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran, Islamic Republic of'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IM', 'Isle of Man'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JE', 'Jersey'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea, Democratic People\'s Republic of'),
    ('KR', 'Korea, Republic of'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Lao People\'s Democratic Republic'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macao'),
    ('MK', 'Macedonia, the former Yugoslav Republic of'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia, Federated States of'),
    ('MD', 'Moldova, Republic of'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PS', 'Palestinian Territory, Occupied'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RE', 'RÃ©union'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('SH', 'Saint Helena, Ascension and Tristan da Cunha'),
    ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'),
    ('MF', 'Saint Martin (French part)'),
    ('PM', 'Saint Pierre and Miquelon'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome and Principe'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('RS', 'Serbia'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SX', 'Sint Maarten (Dutch part)'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('GS', 'South Georgia and the South Sandwich Islands'),
    ('SS', 'South Sudan'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan, Province of China'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania, United Republic of'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TC', 'Turks and Caicos Islands'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('GB', 'United Kingdom'),
    ('US', 'United States'),
    ('UM', 'United States Minor Outlying Islands'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela, Bolivarian Republic of'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands, British'),
    ('VI', 'Virgin Islands, U.S.'),
    ('WF', 'Wallis and Futuna'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe')
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

    def __str__(self):
        return self.username


class Medias(MyModel):
    file = models.FileField(upload_to='', null=True)
    created_by = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)# for customer?
    created_at = models.DateTimeField(auto_now=True)


class Customers(MyModel):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255, null=True)
    email_verified = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    phone_verified = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    id_verified = models.BooleanField(choices=BOOLEAN_TYPES, default=False)
    seller_level = models.IntegerField(null=True)
    created_at = models.DateTimeField()
    suspended = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    password = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, null=True)
    avatar = models.TextField(null=True)
    overview = models.TextField(null=True)
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    billing_address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

    def stat(self):
        try:
            return CustomerStat.objects.get(customer=self)
        except:
            return None

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

    def id_cards_list(self):
        return CustomerCC.objects.filter(customer=self)

    def get_avatar(self):
        lists = self.avatar.split(',') if self.avatar else []
        return Medias.objects.filter(id__in=lists)[:1]

    def review_list(self):
        return Reviews.objects.filter(customer=self)

    def other_open_offers_list(self):
        return Offers.objects.filter(created_by=self, is_expired=False)


class CustomerStat(MyModel):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    balance = models.FloatField(null=True)
    successful_trades = models.FloatField(null=True)
    complete_trade_rate = models.FloatField(null=True)
    review_rate = models.FloatField(null=True)
    review_count = models.IntegerField(null=True)
    last_postal_code = models.IntegerField(null=True)
    last_country = models.CharField(max_length=10, choices=COUNTRY_CODE, null=True)
    last_city = models.CharField(max_length=255, null=True)
    confirm_date = models.DateTimeField(auto_now=True)
    auto_confirm_date = models.DateTimeField(null=True)
    average_trade_complete_time = models.FloatField(null=True)
    trade_initiate_complete_rate = models.FloatField(null=True)
    customer_rate_amount = models.FloatField(null=True)
    trusted_by_count = models.IntegerField(null=True)
    blocked_by_count = models.IntegerField(null=True)


class CustomerCC(MyModel):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    security_code = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()
    images = models.TextField(null=True)

    def images_list(self):
        lists = self.images.split(',') if self.images else []
        return Medias.objects.filter(id__in=lists)


class Revenue(MyModel):
    source = models.CharField(max_length=255)
    revenue_type = models.CharField(max_length=255)
    amount = models.FloatField()
    refund = models.FloatField()
    date = models.DateTimeField()


class Offers(MyModel):
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPES)
    what_crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    flat = models.CharField(max_length=10, choices=FLAT_CHOICES)
    postal_code = models.IntegerField(null=True)
    show_postcode = models.BooleanField(choices=BOOLEAN_TYPES)
    country = models.CharField(max_length=10, choices=COUNTRY_CODE)
    city = models.CharField(max_length=100, null=True)
    trade_price = models.FloatField()
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
    created_by = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()
    is_expired = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def supported_location_list(self):
        lists = self.supported_location.split(',') if self.supported_location else []
        return lists

    def counter(self):
        try:
            return CounterOffer.objects.get(offer=self)
        except:
            return None


class Trades(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    trade_initiator = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='trade_trade_initiator')
    vendor = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='trade_vendor', null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.FloatField()
    status = models.BooleanField(choices=STATUS_TYPES)
    proof_documents = models.TextField(null=True)
    proof_not_opened = models.CharField(max_length=255, null=True)
    proof_opened = models.CharField(max_length=255, null=True)
    trade_date = models.DateTimeField(null=True)
    trade_complete = models.BooleanField(default=False)
    trade_status = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    def is_gift_card(self):
        return True if '_gc' in self.payment_method else False

    def is_proofed(self):
        if self.is_gift_cards:
            return True if self.proof_not_opened else False
        else:
            return True if self.proof_documents else False

    def is_opened(self):
        return True if self.proof_opened else False

    def seller(self):
        return self.offer.created_by if self.offer.trade_type == 'sell' else self.trade_initiator

    def buyer(self):
        return self.trade_initiator if self.offer.trade_type == 'buy' else self.offer.created_by

    def offerer_review(self):
        try:
            return Reviews.objects.get(transaction=self)
        except:
            return None


class Transactions(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    trade_initiator = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='transactions_trade_initiator')
    vendor = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='transactions_vendor')
    txn = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.BooleanField(choices=STATUS_TYPES)


class Escrows(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    held_for = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='escrows_held_for')
    held_from = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='escrows_held_from')
    status = models.BooleanField(choices=PENDING_TYPES)
    amount = models.FloatField()


class Tickets(MyModel):
    email = models.CharField(max_length=255)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=255)
    content = models.TextField(null=True)
    is_dispute = models.BooleanField(choices=PENDING_TYPES)
    ticket_manager = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    ticket_priority = models.CharField(max_length=10)
    attached_files = models.TextField(null=True)
    created_at = models.DateTimeField()

    def attached_files_list(self):
        lists = self.attached_files.split(',') if self.attached_files else []
        return Medias.objects.filter(id__in=lists)

    def messages_list(self):
        return Messages.objects.filter(message_type='ticket', ticket=self)


class Messages(MyModel):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey('Messages', on_delete=models.CASCADE, null=True)
    partner = models.ForeignKey(Customers, null=True, on_delete=models.CASCADE, related_name='messages_partner')
    writer = models.ForeignKey(Customers, null=True, on_delete=models.CASCADE, related_name='messages_writer')
    writer_admin = models.ForeignKey(Users, null=True, on_delete=models.CASCADE, related_name='messages_admin')
    content = models.TextField()
    message_type = models.CharField(max_length=100,null=True)
    # attach_file = models.CharField(max_length=255)
    created_at = models.DateTimeField()



class Contacts(MyModel):
    email_address = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)
    subject = models.TextField()
    content = models.TextField()
    ip_address = models.CharField(max_length=100)
    readed = models.BooleanField(default=False, choices=BOOLEAN_TYPES)


class Pages(MyModel):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAGESTATUS_TYPES)
    context = models.TextField()
    updated_on = models.DateTimeField()
    created_at = models.DateTimeField()


class Posts(MyModel):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAGESTATUS_TYPES)
    context = models.TextField()
    tags = models.TextField()
    featured_images = models.TextField()
    disallow_comments = models.BooleanField(choices=BOOLEAN_TYPES)
    updated_on = models.DateTimeField()
    created_at = models.DateTimeField()

    def featured_images_list(self):
        lists = self.featured_images.split(',') if self.featured_images else []
        return Medias.objects.filter(id__in=lists)

    def first_featured_image(self):
        return self.featured_images_list()[:1]
    
    def beauty_context(self):
        # beautify code for context
        return self.context[:1000]

    def tags_list(self):
        return self.tags.split(',')

    def related_post_list(self):
        # rposts = Posts.objects.filter(tags__in=(self.tags_list))
        # ret = rposts[:3] if rposts.count() > 0 else []
        return []


class Tags(MyModel):
    name = models.CharField(max_length=255)
    ongoing = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class Idcards(MyModel):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    document_file = models.ForeignKey(Medias, on_delete=models.CASCADE)
    status = models.BooleanField(choices=ACCEPTIVE_TYPES)


class LoginLogs(MyModel):
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
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
    template_page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    personalized_link = models.CharField(max_length=255)
    redirection_type = models.CharField(max_length=255)


class PersLinks(MyModel):
    landing_page = models.ForeignKey(LandingPages, on_delete=models.CASCADE)
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
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
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

    def creative_materials_as_file_list(self):
        lists = self.creative_materials.split(',') if self.creative_materials else []
        return Medias.objects.filter(id__in=lists)


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

class Reports(MyModel):
    user_joined = models.CharField(max_length=255)
    affiliate = models.ForeignKey(Affiliates, on_delete=models.CASCADE)
    lead_status = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    report_field = models.CharField(max_length=100)


class Reviews(MyModel):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='review_for')
    transaction = models.ForeignKey(Trades, on_delete=models.CASCADE)
    as_role = models.CharField(max_length=100)
    review_rate = models.FloatField()
    feedback = models.TextField(null=True)
    created_by = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='review_by')
    created_at = models.DateTimeField()

    def is_flagged(self):
        try:
            return FlaggedFeedback.objects.get(review=self)
        except:
            return None


class FlaggedFeedback(MyModel):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    content = models.TextField(null=True)
    created_by = models.ForeignKey(Customers, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class Lists(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Customers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def is_updated(self):
        offers = Offers.objects.filter(updated_at__gt=self.created_at)
        return True if offers.count() > 0 else False


class CounterOffer(MyModel):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    price = models.FloatField()
    flat = models.CharField(max_length=100, choices=FLAT_CHOICES)
    message = models.TextField()
    created_by = models.ForeignKey(Customers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
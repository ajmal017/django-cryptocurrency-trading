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


class Customers(MyModel):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_verified = models.BooleanField(choices=BOOLEAN_TYPES)
    phone_verified = models.BooleanField(choices=BOOLEAN_TYPES)
    id_verified = models.BooleanField(choices=BOOLEAN_TYPES)
    seller_level = models.IntegerField()
    created_at = models.DateTimeField()
    suspended = models.BooleanField(default=False, choices=BOOLEAN_TYPES)

    def __str__(self):
        return self.username

class Revenue(MyModel):
    source = models.CharField(max_length=255)
    revenue_type = models.CharField(max_length=255)
    amount = models.FloatField()
    refund = models.FloatField()
    date = models.DateTimeField()


class Offers(MyModel):
    address = models.CharField(max_length=255)
    flat = models.CharField(max_length=10, choices=FLAT_CHOICES)
    created_by = models.ForeignKey(Customers, on_delete=models.CASCADE)
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
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    trade_initiator = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='trade_trade_initiator')
    vendor = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='trade_vendor')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.FloatField()
    status = models.CharField(max_length=255)
    proof_documents = models.TextField()
    proof_not_opened = models.CharField(max_length=255)
    proof_opened = models.CharField(max_length=255)
    created_at = models.DateTimeField()


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
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    is_dispute = models.BooleanField(choices=BOOLEAN_TYPES)
    ticket_manager = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    ticket_priority = models.CharField(max_length=10)


class Messages(MyModel):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    writer = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    # attach_file = models.CharField(max_length=255)
    created_at = models.DateTimeField()


class Contacts(MyModel):
    email_address = models.CharField(max_length=255)
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

    def featured_images_as_file_list(self):
        lists = self.featured_images.split(',') if self.featured_images else []
        return Medias.objects.filter(id__in=lists)


class Tags(MyModel):
    name = models.CharField(max_length=255)
    ongoing = models.BooleanField(default=False, choices=BOOLEAN_TYPES)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class Medias(MyModel):
    file = models.FileField(upload_to='', null=True)
    created_by = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
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
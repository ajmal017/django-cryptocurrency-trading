from django.db import models
from django.core.mail import send_mail


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
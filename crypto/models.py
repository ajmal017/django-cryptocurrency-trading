from django.db import models
# from django.core.mail import send_mail
# import random
# import string
# import timeago
# from datetime import datetime, timezone
# from raplev import settings
# from django.db.models import Q, Sum, Count, F
# from bs4 import BeautifulSoup as bs


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


class BTC(MyModel):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    customer = models.ForeignKey('cadmin.Customers', on_delete=models.CASCADE)
    addr = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    addrs = models.TextField(null=True)


class ETH(MyModel):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    customer = models.ForeignKey('cadmin.Customers', on_delete=models.CASCADE)
    addr = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255, null=True)
    prv_key = models.CharField(max_length=255, null=True)
    addrs = models.TextField(null=True)
    password = models.CharField(max_length=255, null=True)


class XRP(MyModel):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    customer = models.ForeignKey('cadmin.Customers', on_delete=models.CASCADE)
    addr = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255, null=True)
    addrs = models.TextField(null=True)
    secret = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)

import json
# import random
# from datetime import datetime, timedelta, date

# from django.shortcuts import render

# # Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from blockchain.wallet import Wallet
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
# from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
# from django.utils.crypto import get_random_string
# from rest_framework.serializers import ValidationError

# from cadmin import models, serializers
# from django.http import JsonResponse, HttpResponse
# from loremipsum import get_sentence
# from slugify import slugify
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.contrib.auth.hashers import make_password, check_password
# from django.db.models import Q, Sum, Count, F
# from rest_framework.authtoken.views import ObtainAuthToken
# from .models import Token
# from rest_framework.response import Response

# from raplev import settings
# from django.core.files.storage import FileSystemStorage

from .btc import BTCProcessor
from .eth import ETHProcessor
from .xrp import XRPProcessor
from cadmin import models

# btc_processor = BTCProcessor(1)
# eth_processor = ETHProcessor(1)
# xrp_processor = XRPProcessor(1)

class IndexView(APIView):
    
    def get(self, request):
        customer = models.Customers.objects.get(id=1)
        btc_processor = BTCProcessor(customer)
        eth_processor = ETHProcessor(customer)
        xrp_processor = XRPProcessor(customer)
        return Response({'result': eth_processor.get_balance()}, status=status.HTTP_200_OK)
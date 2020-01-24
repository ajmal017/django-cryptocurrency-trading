from theme.constants import ESCROWS_STATUS_TYPES, VOTE_TYPES, TRADE_STATUS_TYPES, FLAT_CHOICES, CRYPTO_CHOICES, CURRENCY_CHOICES,REGISTRATION_CHOICES,CC_TYPES,LANGUAGE_CHOICES,TICKET_STATUS_CHOICES,TRADE_TYPES,CUSTOMER_TYPES,PAYMENT_METHODS,ROLE_TYPES,BOOLEAN_TYPES,STATUS_TYPES,VERIFIED_TYPES,PENDING_TYPES,ACCEPTIVE_TYPES,PAGESTATUS_TYPES,COUNTRY_CODE
from cadmin.models import Users, Pricing
from . import cache


def theme_decorators(request):

    price = Pricing()
    pricing = {
        # 'BTC_USD': cache.CurrencyExchangeData.get_or_set_rate('BTC', 'USD'),
        # 'ETH_USD': cache.CurrencyExchangeData.get_or_set_rate('ETH', 'USD'),
        # 'XRP_USD': cache.CurrencyExchangeData.get_or_set_rate('XRP', 'USD'),
    } 

        
    if request.user.is_superuser:
        user = request.user
        user.fullname = 'SuperUser'
    else:
        if 'user' in request.session:
            user_token = request.session['user']
        else:
            user_token = ''
        try:
            user = Users.objects.get(token=user_token)
        except:
            user = None

    return { 'user': user, 'pricing': pricing, 'theme_url': '', **global_setting() }


def global_setting():
    return {"FLAT_CHOICES": FLAT_CHOICES, 
        "ESCROWS_STATUS_TYPES": ESCROWS_STATUS_TYPES, 
        "VOTE_TYPES": VOTE_TYPES, 
        "TRADE_STATUS_TYPES": TRADE_STATUS_TYPES, 
        "CRYPTO_CHOICES": CRYPTO_CHOICES, 
        "CURRENCY_CHOICES": CURRENCY_CHOICES, 
        "REGISTRATION_CHOICES": REGISTRATION_CHOICES, 
        "CC_TYPES": CC_TYPES, 
        "LANGUAGE_CHOICES": LANGUAGE_CHOICES, 
        "TICKET_STATUS_CHOICES": TICKET_STATUS_CHOICES, 
        "TRADE_TYPES": TRADE_TYPES, 
        "CUSTOMER_TYPES": CUSTOMER_TYPES, 
        "PAYMENT_METHODS": PAYMENT_METHODS, 
        "ROLE_TYPES": ROLE_TYPES, 
        "BOOLEAN_TYPES": BOOLEAN_TYPES, 
        "STATUS_TYPES": STATUS_TYPES, 
        "VERIFIED_TYPES": VERIFIED_TYPES, 
        "PENDING_TYPES": PENDING_TYPES, 
        "ACCEPTIVE_TYPES": ACCEPTIVE_TYPES, 
        "PAGESTATUS_TYPES": PAGESTATUS_TYPES, 
        "COUNTRY_CODE": COUNTRY_CODE}
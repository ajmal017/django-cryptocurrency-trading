import redis
import json
import requests
from geopy import GoogleV3
from geopy.exc import GeocoderQueryError
import logging

from django.conf import settings


r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT
)

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


class CurrencyExchangeData:
    """
    Class used for storing currency exchange rates for 10 minutes
    """
    @staticmethod
    def get_or_set_rate(currency_one, currency_two):
        current_rate = r.get('{}-{}'.format(currency_one, currency_two))
        if current_rate:
            current_rate = json.loads(current_rate.decode())
            print(current_rate)
            return current_rate
        else:
            new_rate = requests.get('https://api.cryptonator.com/api/ticker/{}-{}'.format(currency_one, currency_two))
            print(new_rate.text)
            r.set('{}-{}'.format(currency_one, currency_two), new_rate.text)
            r.expire('{}-{}'.format(currency_one, currency_two), 600)
            return json.loads(new_rate.text)


class GoogleMapsGeocoding:
    """
    Class used for caching the values got from Google's geocoding service
    """

    def __init__(self):
        self.geo_locator = GoogleV3(api_key=settings.GOOGLE_API_KEY)

    def get_or_set_location(self, country, city, postcode):
        current_location = r.get('l-{country}-{city}-{postcode}'.format(country=country, city=city, postcode=postcode))
        if current_location:
            location = json.loads(current_location.decode())
            return location
        else:
            try:
                geo_location = self.geo_locator.geocode(components={
                    'country': country,
                    'locality': city,
                    'postal_code': postcode
                })
            except GeocoderQueryError as e:
                logger.error('Google Geocoding error: {}'.format(e))
                return None
            if geo_location:
                rgl = geo_location.raw
                r.set('l-{country}-{city}-{postcode}'.format(country=country, city=city, postcode=postcode),
                      json.dumps(rgl))
                r.expire('l-{country}-{city}-{postcode}'.format(country=country, city=city, postcode=postcode),
                         settings.GOOGLE_GEOCODING_CACHE_TIME)
                return rgl
            else:
                return None


class PhoneCodeCache:
    """
    Class used for temporarily storing the phone code used for authorizing the user
    """

    @staticmethod
    def set_phone_code(user_id):
        import random
        random.seed()
        phone_code = random.randint(10**(settings.SMS_CODE_LENGTH-1), 10**settings.SMS_CODE_LENGTH)
        r.set('phonecode-{}'.format(user_id), phone_code)
        r.expire('phonecode-{}'.format(user_id), 10)
        logger.info('Generated access code for user {user_id} - {phone_code}'.format(
            user_id=user_id, phone_code=phone_code))
        return phone_code

    @staticmethod
    def get_phone_code(user_id):
        if r.get('phonecode-{}'.format(user_id)):
            return r.get('phonecode-{}'.format(user_id)).decode()
        else:
            return None

import json
import binascii
import logging
import hashlib

from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

import hmac

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


class SingleSignOnView(LoginRequiredMixin, View):
    """
    View that is used for Commento.io to implement SSO
    """
    def get(self, request):
        token = request.GET.get('token', '')
        received_hmac = request.GET.get('hmac', '')
        logger.info('Token: {}'.format(token))
        logger.info('HMAC: {}'.format(received_hmac))
        secret_key = binascii.unhexlify(settings.COMMENTO_HMAC_KEY)
        expected_mac = hmac.new(secret_key, binascii.unhexlify(token), hashlib.sha256).hexdigest()
        logger.info('Expected HMAC: {}'.format(expected_mac))
        if received_hmac != expected_mac:
            return redirect('/index')
        logger.info('Name: {}, Email: {}, Photo: {}'.format(
            request.user.full_name,
            request.user.email,
            request.user.profile_photo
        ))
        data = {
            'token': token,
            'email': request.user.email,
            'name': request.user.full_name,
            'photo': 'http://raplev.com/media/' + str(request.user.profile_photo),
            'link': ''
        }
        encoded_data = json.dumps(data).encode('utf-8').hex()
        sent_hmac = hmac.new(secret_key, json.dumps(data).encode('utf-8'), hashlib.sha256).hexdigest()
        logger.info('Encoded data: {}'.format(encoded_data))
        logger.info('Encoded hmac: {}'.format(sent_hmac))
        return redirect('http://{}/api/oauth/sso/callback?payload={}&hmac={}'.format(settings.COMMENTO_HOST, encoded_data, sent_hmac))


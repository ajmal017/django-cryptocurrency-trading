from django.conf import settings


def commento_host(request):
    return {'COMMENTO_HOST': settings.COMMENTO_HOST}

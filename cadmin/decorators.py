from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest


def cadmin_user_is_logged_in(f):
    def wrap(request, *args, **kwargs):
        if 'cadmin_user' in request.session.keys() or request.user.is_superuser:
            return HttpResponseRedirect("/cadmin")
        return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    # wrap.__name__=f.__name__
    return wrap


def cadmin_user_login_required(f):
    def wrap(request, *args, **kwargs):
        if 'cadmin_user' in request.session.keys() or request.user.is_superuser:
            return f(request, *args, **kwargs)
        return HttpResponseRedirect("/cadmin/login")

    wrap.__doc__=f.__doc__
    # wrap.__name__=f.__name__
    return wrap
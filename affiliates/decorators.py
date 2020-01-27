from django.http import HttpResponseRedirect
from cadmin.models import Users


def user_not_logged_in(f):
    def wrap(request, *args, **kwargs):
        # if 'user' in request.session.keys():
        if request.user.is_authenticated and request.user.is_affiliate:
            return HttpResponseRedirect("/affiliates")
        return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    # wrap.__name__=f.__name__
    return wrap


def affiliates_login_required(f):
    def wrap(request, *args, **kwargs):
        # if 'user' in request.session.keys():
        if request.user.is_authenticated:
            # user = Users.objects.get(token=request.session['user'])
            if request.user.is_affiliate:
                return f(request, *args, **kwargs)
        return HttpResponseRedirect("/affiliates/login?next="+request.get_full_path())

    wrap.__doc__=f.__doc__
    # wrap.__name__=f.__name__
    return wrap

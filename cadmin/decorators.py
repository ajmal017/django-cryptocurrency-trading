from django.http import HttpResponseRedirect
from cadmin.models import Users


def user_not_logged_in(f):
    def wrap(request, *args, **kwargs):
        if 'user' in request.session.keys():
            return HttpResponseRedirect("/")
        return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    # wrap.__name__=f.__name__
    return wrap


def admin_login_required(f):
    def wrap(request, *args, **kwargs):
        if 'user' in request.session.keys():
            user = Users.objects.get(token=request.session['user'])
            if user.is_admin:
                return f(request, *args, **kwargs)
        return HttpResponseRedirect("/cadmin/login?next="+request.get_full_path())

    wrap.__doc__=f.__doc__
    # wrap.__name__=f.__name__
    return wrap

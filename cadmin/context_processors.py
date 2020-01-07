from .models import Users

def cadmin_user(request):
    
    global_alert = []
    if 'global_alert' in request.session:
        global_alert = request.session['global_alert']
        
    if request.user.is_superuser:
        cadmin_user = request.user
        cadmin_user.fullname = 'SuperUser'
        return { 'cadmin_user': cadmin_user, 'global_alert': global_alert, 'app_url': 'cadmin' }

    if 'cadmin_user' in request.session:
        user_token = request.session['cadmin_user']
    else:
        user_token = ''
    try:
        cadmin_user = Users.objects.get(token=user_token)
        cadmin_user.is_superuser = False
    except:
        cadmin_user = None

    return { 'cadmin_user': cadmin_user, 'global_alert': global_alert, 'app_url': 'cadmin' }
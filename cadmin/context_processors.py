from .models import Users

def cadmin_user(request):
    
    global_alert = []
    if 'global_alert' in request.session:
        print(request.session['global_alert'])
        if 'viewed' in request.session['global_alert']:
            del request.session['global_alert']
        else:
            global_alert = request.session['global_alert']
            request.session['global_alert'] = {'viewed': True} 
        
    if request.user.is_superuser:
        cadmin_user = request.user
        cadmin_user.fullname = 'SuperUser'
    else:
        if 'cadmin_user' in request.session:
            user_token = request.session['cadmin_user']
        else:
            user_token = ''
        try:
            cadmin_user = Users.objects.get(token=user_token)
            cadmin_user.is_superuser = False
        except:
            cadmin_user = None

    return { 'cadmin_user': cadmin_user, 'global_alert': global_alert, 'cadmin_url': '/cadmin' }
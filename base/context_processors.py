def is_admin_user(request):
    if request.user.is_authenticated:
        is_admin = 'admin' in request.user.username.lower()
    else:
        is_admin = False

    return {
        'is_admin': is_admin
    }
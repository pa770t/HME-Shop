from .views import get_cartitem_count


def cartitem_count(request):
    user = request.user
    if user.is_authenticated:
        return {'cartitem_count': get_cartitem_count(user)}
    else:
        return {'cartitem_count': 0}

from the_list.models import Products


def get_user_index_products(request):
    if not request.session.session_key:
        request.session.create()
    return Products.waitobj.filter(session_key=request.session.session_key)


def get_history_products(request):
    return Products.objects.filter(
        session_key=request.session.session_key,
        status=Products.Status.PURCHASED,
    )

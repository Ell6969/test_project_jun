from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline
from django.db.models import Q

from the_list.forms import ProductFilterForm
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


def q_search(query, products):
    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = products.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>'
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>'
        )
    )
    return result


def filter_products(request, products):
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        min_price = form.cleaned_data.get('min_price', None)
        max_price = form.cleaned_data.get('max_price', None)
        start_date = form.cleaned_data.get('start_date', None)
        end_date = form.cleaned_data.get('end_date', None)

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if start_date:
            products = products.filter(created__gte=start_date)
        if end_date:
            products = products.filter(created__lte=end_date)

    return products

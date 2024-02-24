from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from the_list.forms import ProductsForm
from the_list.models import Products
from the_list.utils import get_user_index_products, get_history_products, q_search, filter_products


def index(request):
    query = request.GET.get('q', None)
    history = request.GET.get('history', None)
    filter = request.GET.get('filter', None)

    if history:
        products = get_history_products(request).order_by('-buy_date')
    else:
        products = get_user_index_products(request)

    last_products = products[:3]

    if query:
        products = q_search(query, products)

    if filter:
        products = filter_products(request, products)

    order_by_list = request.GET.getlist('order_by')
    valid_fields = [field.name for field in Products._meta.get_fields()]
    valid_order_by_list = [field for field in order_by_list if field in valid_fields]
    if valid_order_by_list:
        products = products.order_by(*valid_order_by_list)


    paginator = Paginator(products, 8)
    page_number = request.GET.get('page', 1)
    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    total_price_waiting = Products.waitobj.all().aggregate(Sum('price'))['price__sum']
    total_price_purch = Products.objects.filter(status=Products.Status.PURCHASED).aggregate(Sum('price'))['price__sum']
    context = {
        'products': current_page,
        'last_products': last_products,
        'all_wait_product': get_user_index_products(request).count(),
        'count_history_products': get_history_products(request).count(),
        'total_price_waiting': total_price_waiting if total_price_waiting else 0,
        'total_price_purch': total_price_purch if total_price_purch else 0,
        'history': history,
    }
    if history:
        return render(request, 'the_list/list_history.html', context)
    return render(request, 'the_list/index.html', context)


def product_add(request):
    if request.method == 'POST':
        form = ProductsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if not request.session.session_key:
                request.session.create()
            form.instance.session_key = request.session.session_key
            form.save()

            messages.success(
                request, "Вы успешно добавили покупку"
            )
            return redirect("product:list_products")
    else:
        form = ProductsForm()

    return render(request, 'the_list/index.html', {'form': form})


def product_change(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    if request.method == "POST":
        form = ProductsForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Вы успешно изменили покупку"
            )
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    else:
        form = ProductsForm(instance=product)

    context = {
        'form': form,
    }
    return render(request, 'the_list/index.html', context)


def product_remove(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    product.delete()

    messages.success(
        request, f"Вы успешно удалили покупку"
    )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def clean_user_products_full(request):
    products = get_history_products(request)
    products.delete()

    messages.success(
        request, f"Вы успешно удалили всю историю"
    )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def product_change_status(request, product_slug):
    status = Products.Status.PURCHASED
    product = Products.waitobj.get(slug=product_slug)
    product.status = status
    product.save()

    messages.success(
        request, f"Покупка была успешно перенесена в историю покупок"
    )

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

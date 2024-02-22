from django.contrib import admin

from the_list.models import Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created', 'updated', 'buy_date', 'status')
    list_display = ('name', 'price', )
    search_fields = ('name', 'price',)
    list_filter = ('status',)

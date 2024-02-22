import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class WaitObjManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Products.Status.WAIT)


class Products(models.Model):

    class Status(models.TextChoices):

        PURCHASED = 'PU', 'purchased'
        WAIT = 'WA', 'wait'

    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='purchases_images', blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    buy_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.WAIT)

    objects = models.Manager()
    waitobj = WaitObjManager()

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['-created']),
        ]

    def get_absolute_url(self):
        return reverse("product:product_remove", kwargs={"product_slug": self.slug})

    def __str__(self):
        return f'Продукт {self.name} | '

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug

        super().save(*args, **kwargs)

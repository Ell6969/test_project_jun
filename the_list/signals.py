from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from the_list.models import Products


@receiver(pre_save, sender=Products)
def update_buy_date(sender, instance, **kwargs):
    if instance.pk is not None:
        old_status = Products.objects.get(pk=instance.pk).status
        if instance.status != old_status:
            instance.buy_date = timezone.now()

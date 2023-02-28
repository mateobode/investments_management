from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models.loan import Loan
from backend.models.cashflow import Cashflow


@receiver(post_save, sender=Loan)
@receiver(post_save, sender=Cashflow)
def invalidate_statistics(sender, **kwargs):
    cache.delete('statistics')

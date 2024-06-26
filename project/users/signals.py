from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from .models import Seller
from .models import User


@receiver(post_save, sender=User)
@receiver(post_save, sender=Seller)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from hr.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_permissions_new_user(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        user.permission_handler()
        user.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        Profile.objects.create(user=user, co_email=f"{user}@sotoon.ir")

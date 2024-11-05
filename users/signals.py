
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AppUser
from .updateStats import update_statistics  # Adjust the import as necessary

@receiver(post_save, sender=AppUser)
def user_saved(sender, instance, created, **kwargs):
    # Call update_statistics after a user is created or updated
    if created:
        update_statistics()

@receiver(post_delete, sender=AppUser)
def user_deleted(sender, instance, **kwargs):
    # Call update_statistics after a user is deleted
    update_statistics()
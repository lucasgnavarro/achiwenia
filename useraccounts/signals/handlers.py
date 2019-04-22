from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from useraccounts.models import UserProfile


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except User.profile.RelatedObjectDoesNotExist:
            UserProfile.objects.create(user=instance)

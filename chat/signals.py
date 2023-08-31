from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Thread

@receiver(post_save, sender=User)
def create_thread_for_new_user(sender, instance, created, **kwargs):
    if created:
        existing_users = User.objects.exclude(pk=instance.pk)
        for user in existing_users:
            Thread.objects.create(first_person=instance, second_person=user)
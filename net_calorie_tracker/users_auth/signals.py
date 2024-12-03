# users_auth/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender='users_auth.CustomUser')  # Replace with your custom user model
def log_initial_weight(sender, instance, created, **kwargs):
    """
    Logs the initial weight when a user signs up.
    """
    if created:  # Only for newly created users
        WeightHistory = apps.get_model('tracker', 'WeightHistory')
        WeightHistory.objects.create(user=instance, weight=instance.weight)

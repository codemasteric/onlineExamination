from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sat_exams = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Participant.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance,created, **kwargs):
    try:
        participant = Participant.objects.get(user=instance.pk)
        participant.email = instance.email
        participant.save()
    except(Participant.DoesNotExist):
        pass

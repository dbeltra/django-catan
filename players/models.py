from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

# Create your models here.

class Player(models.Model):
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Player, self).save(*args, **kwargs)

@receiver(post_delete, sender=Player)
def _player_post_delete(sender, instance, **kwargs):
    instance.user.delete()
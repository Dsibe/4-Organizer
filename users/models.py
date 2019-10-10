from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
        # super(Profile, self).save(*args, **kwargs)

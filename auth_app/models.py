from django.db import models

from django.contrib.auth.models import User
from register_app.models import School


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return f'{self.user.username} Profile'

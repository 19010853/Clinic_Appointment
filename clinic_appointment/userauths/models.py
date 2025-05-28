from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

USER_TYPE = (
    ("Doctor", "Doctor"),
    ("Patient", "Patient"),
)

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """How to create users. Django calls this from create_user / createsuperuser."""

    def create_user(self, phone, password=None, **extra):
        user = self.model(phone=phone, **extra)
        if password:
            user.set_password(password)     # only the admin uses a password
        else:
            user.set_unusable_password()    # normal users log in by OTP only
        user.save()
        return user

    def create_superuser(self, phone, password, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):   # Django's login machinery, without username
    phone = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)    # False = blocked account
    is_staff = models.BooleanField(default=False)    # True = can open /admin
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"      # "log in with phone instead of username"
    REQUIRED_FIELDS = []

# Create your models here.

## Creating the models means just the data shape that get stored in the db. 

# we will have 2 data table: user with id and the phone

# otp with fields: id, hash_code (dont store the orgi code), created_at, expires_at, used_at, attempts, phone_number



class OTPCode(models.Model):
    hashed_code = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=10, db_index=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)


    class Meta:
        ordering = ["-created_at"] #newest first, so first() = latest code

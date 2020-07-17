from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('A user has to have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('The password field is required')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True,
        max_length=100
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'logins'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    is_vip = models.BooleanField(default=False)
    referrals = models.IntegerField(default=0)

    class Meta:
        db_table = 'members'

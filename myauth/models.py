from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token






class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

#  customize default user model as CustomUser
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
# extend the profile of User model
class Profile(models.Model):
    LEARNER = 1
    FACILITATOR = 2
    ADMIN = 3
    VISITER=4
    ROLE_CHOICES = (
         (VISITER, 'Visiter'),
        (LEARNER, 'Learner'),
        (FACILITATOR, 'Facilitator'),
        (ADMIN, 'Admin'),

    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    #Address = models.CharField(max_length=30, blank=True)
    #DOB = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    phone=models.CharField(max_length=13,null=True, blank=True)
    portfolio = models.FileField(upload_to ='uploads/',null=True, blank=True)
    intrest=models.CharField(max_length=250)
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        #Token.objects.create(user=instance)
    instance.profile.save()
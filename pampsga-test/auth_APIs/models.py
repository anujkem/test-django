from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, fullName, password, **other_fields):
        # other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, fullName, password, **other_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    usType = ((1, 'User'), )
    deviceType = ((1, "Android"), (2, "IOS"),(3,"web"))
    genderType = ((1, "Male"), (2, "Female"), (3, "Not to Refer"))
    socialType = ((1, 'Google'), (2, 'Facebook'), (3, 'Apple'))

    profileImage = models.CharField(max_length=255,null=True,default=None)
    fullName = models.CharField(max_length=255,null=True,default=None)
    phoneNumberCountryCode = models.CharField(max_length=255, null=True, default=+91)
    mobileNo = models.CharField(max_length=15,null=True,default=None)
    email = models.EmailField(max_length=255,null=True,default=None)
    gender = models.IntegerField(choices=genderType, null=True)
    password = models.CharField(max_length=255, null=True)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    deviceToken = models.CharField(max_length=255, null=True, default=None)
    userType = models.IntegerField(choices=usType,default=1)
    deviceType = models.IntegerField(choices=deviceType, null=True)
    tnc = models.BooleanField(default=False, null=True)
    admin_forget_password_token = models.CharField(max_length=255, null=True, blank=True, default=False)
    authServiceProviderId = models.CharField(max_length=255, null=True, blank=True)
    authServiceProviderType = models.IntegerField(choices=socialType, null=True, blank=True, default=None)
    referralCode = models.CharField(max_length=255, null=True, blank=True)
    invitedCode = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['fullName']
    objects = CustomAccountManager()

    class Meta:
        db_table = 'Users'

        indexes = [
            models.Index(fields=['fullName'], name='fullName_idx'),
            models.Index(fields=['mobileNo'], name='mobileNo_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['email', 'mobileNo'], name='email_mobileNo_idx'),
        ]

    def __str__(self):
        return self.fullName

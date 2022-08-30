from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _




class CustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, username, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone number must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(phone_number=phone_number, email=email, username=username, **extra_fields)
        # user.password = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email,username, password, **extra_fields)

    def create_superuser(self, phone_number, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, username, password, **extra_fields)


class Customuser(AbstractUser):
    

    username = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10,unique=True)
    email = models.EmailField(_("Email"), unique=True, max_length=100)
    

    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email','username']
    

    objects = CustomManager()


    def __str__(self):
        return self.username
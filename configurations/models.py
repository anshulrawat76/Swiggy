from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    mobile_number = models.IntegerField(max_length=10, null= True)
    otp = models.IntegerField(max_length=6, null= True)
    otp_verify = models.BooleanField(default=False)
    otp_expire = models.DateTimeField(null=True , blank=True)
    first_name = models.CharField(max_length=18 , null=True , blank=True)
    last_name  = models.CharField(max_length=15 , null=True , blank=True)
    date_of_birth = models.DateField(null=True ,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin= models.BooleanField(default=False)


    USER_TYPES = (
        (1,'Customer'),
        (2,'Driver'),
        (3,'Restaurant'),
    )
    user_types = models.IntegerField(
        choices =  USER_TYPES,
        default = 1
    
    )



    objects = MyUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
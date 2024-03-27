from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# create custome user manager model
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password is not provided')
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )  

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


# create user model
class User(AbstractBaseUser, PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default
    email = models.EmailField(db_index = True, unique=True, max_length=254)
    first_name = models.CharField(max_length=154)
    last_name = models.CharField(max_length=254)
    mobile =  models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('user', 'User')], default='user')

    # Roles user
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta: 
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return(f'nama: {self.first_name} {self.last_name}, email: {self.email}')

# create buku model
class Buku(models.Model):
    keterangan_kas = models.CharField(max_length=255)
    saldo = models.IntegerField(default=0, null=True)
    debet = models.IntegerField(default=0, null=True)
    tanggal = models.DateField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
    def __str__(self):
        return(f'{self.keterangan_kas}') 
    


    




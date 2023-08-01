from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models



class Usermanager(BaseUserManager):


    def create_user(self,fullname,username,phone,email,password=None):
        if not email:
            raise ValueError('user must need email')
        
        if not username:
            raise ValueError('user must need username')
        
        user = self.model(
            fullname = fullname,
            email = self.normalize_email(email),
            username = username,
            phone=phone
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, fullname, username, email, password):
        user = self.create_user(
        email=email,
        username=username,
        password=password,
        fullname=fullname,
        phone='1234567890',
        )

        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.is_hoteluser = True
        user.save(using=self._db)
        return user




class UserDetails(AbstractBaseUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=100,unique=True)


    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_hoteluser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username','fullname']

    objects = Usermanager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

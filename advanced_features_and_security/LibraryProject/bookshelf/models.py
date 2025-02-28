from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUserManager(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField()

    def create_user(self):
        if not self.username:
            raise ValueError("User must have username")
        if not self.password:
            raise ValueError("User must have a password")
        
        user = self.model(username=self.username, email=self.email)
        user.set_password(self.password)
        user.active = False
        user.staff = False
        user.save(using=self._db)
        return user
    

    def create_superuser(self):
        if not self.username:
            raise ValueError("User must have username")
        if not self.password:
            raise ValueError("User must have a password")
        
        user = self.model(username=self.username, email=self.email)
        user.set_password(self.password)
        user.active = True
        user.staff = True
        user.save(using=self._db)
        return user
    


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.author} - {self.publication_year}"

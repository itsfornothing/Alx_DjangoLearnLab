from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField()
    

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password, is_staff=False, is_admin=False):
        if not self.username:
            raise ValueError("User must have username")
        if not self.password:
            raise ValueError("User must have a password")
        
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user
    

    def create_superuser(self, username, email, password, is_staff=False, is_admin=False):
        if not self.username:
            raise ValueError("User must have username")
        if not self.password:
            raise ValueError("User must have a password")
        
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.author} - {self.publication_year}"


class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name
    
    class Meta:
    
        permissions = (
        ('can_view', 'Can View'),
        ('can_create', 'Can Create'),
        ('can_edit', 'Can Edit'),
        ('can_delete', 'Can Delete')
        )

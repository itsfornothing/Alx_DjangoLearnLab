from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
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
    


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        permissions = (
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        )

    def __str__(self):
        return self.title


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


class UserProfile(models.Model):
    ROLE_CHOICES = [
    ("admin", "Admin"),
    ('librarian', 'Librarian'),
    ('member', 'Member'),
    ]       

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


    
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

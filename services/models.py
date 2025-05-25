from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('design', 'Design'),
        ('writing', 'Writing'),
        ('coding', 'Coding'),
        ('other', 'Other'),
        ('web', 'Web Development'),
        ('marketing', 'Marketing'),
    ]


    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
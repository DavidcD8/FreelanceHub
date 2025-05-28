from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField
from  taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _



class Service(models.Model):
    CATEGORY_CHOICES = [
        ('design', 'Design'),
        ('writing', 'Writing'),
        ('coding', 'Coding'),
        ('other', 'Other'),
        ('web', 'Web Development'),
        ('marketing', 'Marketing'),
    ]
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ]

    FRAMEWORK_CHOICES = [
        ('django', 'Django'),
        ('react', 'React'),
        ('flask', 'Flask'),
        ('node', 'Node.js'),
        ('bootstrap', 'Bootstrap'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    languages = MultiSelectField(choices=LANGUAGE_CHOICES, blank=True)
    frameworks = MultiSelectField(choices=FRAMEWORK_CHOICES, blank=True)


    def __str__(self):
        return self.title





class Profile(models.Model):

    LEVEL_MAP = {
        'pro': 'Pro Seller',
        'top': 'Top Rated Freelancer',
        'verified': 'Verified Freelancer',
        'new': 'New Seller',
    }

    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=20,choices=EXPERIENCE_CHOICES,default='beginner',help_text="Select your experience level")

    @property
    def average_rating(self):
        ratings = UserRating.objects.filter(seller=self.user)
        if ratings.exists():
            total = sum(r.rating for r in ratings)
            return total / ratings.count()
        return None



    
class UserRating(models.Model):
    rater = models.ForeignKey(User, related_name='given_ratings', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='received_ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return f"Rating {self.rating} by {self.rater.username} for {self.seller.username}"
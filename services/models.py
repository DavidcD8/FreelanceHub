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
    LEVEL_CHOICES = [
        ('new', 'New Seller'),
        ('verified', 'Verified Freelancer'),
        ('top', 'Top Rated Freelancer'),
        ('pro', 'Pro Seller'),
    ]
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
    level = models.CharField(max_length=20,choices=LEVEL_CHOICES,default='new',editable=False,help_text="Seller level is assigned automatically")

    @property
    def computed_level(self):
        service_count = self.user.service_set.count()

        if service_count >= 10:
            return self.LEVEL_MAP['pro']
        elif service_count >= 5:
            return self.LEVEL_MAP['top']
        elif service_count >= 1:
            return self.LEVEL_MAP['verified']
        else:
            return self.LEVEL_MAP['new']

    def save(self, *args, **kwargs):
        # Automatically update level based on service count before saving
        self.level = next(
            # generator expression that loops through all the key-value pairs
            key for key, val in self.LEVEL_MAP.items() if val == self.computed_level 
        )
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username}'s Profile"
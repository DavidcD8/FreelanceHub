from .models import Service

def category_choices(request):
    return {
        'categories': Service.CATEGORY_CHOICES
    }

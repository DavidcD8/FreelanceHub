from django import template

register = template.Library()

@register.filter
def star_rating(rating):
    try:
        rating = int(round(float(rating)))
    except (ValueError, TypeError):
        rating = 0
    full_stars = '★' * rating
    empty_stars = '☆' * (5 - rating)
    return full_stars + empty_stars

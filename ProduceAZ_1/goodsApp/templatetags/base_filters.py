from django import template
from goodsApp.models import NavLink
register = template.Library()

@register.simple_tag
def get_nav_links():
    return NavLink.objects.filter(active=True)
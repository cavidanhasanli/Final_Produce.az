from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(AboutPage)
admin.site.register(Partner)
admin.site.register(NavLink)
admin.site.register(Post)

admin.site.register(Event)
admin.site.register(HeaderModel)
admin.site.register(BackgroundImage)
admin.site.register(ContactUs)


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     fields = ('title', 'image', 'description', )
#     list_display = ('title',)
#     list_filter = ('created_at',)
#     search_fields = ('title',)

# @admin.register(Category)
# class (admin.ModelAdmin):
#     fields = ('title', 'image',)
#     list_display = ('title',)
#     search_fields = ('title',)


# @admin.register(Products)
# class ProductsAdmin(admin.ModelAdmin):
#     fields = ('title', 'image', 'description', 'long description', )
#     # list_display = ('title',)
#     list_filter = ('created_at',)
#     search_fields = ('title',)
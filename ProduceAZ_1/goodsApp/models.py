from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    slug =  models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Products(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    image = models.ImageField(upload_to='categories')
    price = models.FloatField()
    contact = models.CharField(max_length=255, blank=False, null=True)
    email = models.EmailField(max_length=60, blank=False, null=True)
    made_in = models.CharField(max_length=255, blank=False, null=True)
    url = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField(blank=False, null=True)
    add_info = models.CharField(max_length=255, blank=False, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AboutPage(models.Model):
    title = models.CharField(max_length=255,blank=True,null=False)
    text = models.CharField(max_length=255,blank=True,null=False)
    background_img = models.ImageField(max_length=255,blank=True,null=False)
    image = models.ImageField(upload_to='aboutpage_images')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Partner(models.Model): 
    partner_name = models.CharField(max_length=255,blank=True,null=False)
    partner_image = models.ImageField(upload_to='partner_image')
    partner_des = models.CharField(max_length=255,blank=True,null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NavLink(models.Model):
    title = models.CharField(max_length=255,blank=False,null=False) 
    url = models.CharField(max_length=255,blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



# class Post(models.Model):
#     title = models.CharField(max_length=255, null = True)
#     description = models.CharField(max_length=255, null = True, blank = True)
#     text = models.TextField(null = True, blank = True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to = 'blog_images')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return self.title or self.id



class Event(models.Model):
    title = models.CharField(max_length=255, null = True)
    description = models.CharField(max_length=255, null = True, blank = True)
    text = models.TextField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'blog_images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    test_date = models.DateField(null = True, blank = True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.title or self.id

class Post(models.Model):
    title = models.CharField(max_length=255, null = True)
    description = models.CharField(max_length=255, null = True, blank = True)
    text = models.TextField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'blog_images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateField(null = True, blank = True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True,blank=True)


    def __str__(self):
        return self.title or self.id


class HeaderModel(models.Model):
    title = models.CharField(max_length=244)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class BackgroundImage(models.Model):
    header = models.ForeignKey('HeaderModel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='background')

    def __str__(self):
        return self.header.title

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}"

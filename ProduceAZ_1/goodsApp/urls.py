from django.urls import path
from .views import *

app_name = 'goodsApp'

urlpatterns = [
    path('', PartnerView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('products/', get_products, name='products'),
    path('products/<int:cat_id>', get_category, name='get_category'),
    path('products_detail/<int:prod_id>', get_detail, name='get_detail'),
    path('ajax/<sort_by>', sorting, name='sorting'),

    path('blog/', get_blog, name="get_blog"),
    path('blog/<int:id>', get_blog_detail, name="get_blog_detail"),
    path('event/', create_event, name="create_event"),
    path('event/<int:id>', get_event_detail, name="get_event_detail"),
    path('event/<str:month>', get_event_archieve, name="get_event_archieve"),
    path('event/category/<str:slug>', get_category_event, name='get_category_event'),
    # path('search/', search_products, name='search_results'),
    path('blog/', get_blog, name="get_blog"),
    path('blog/<int:id>', get_blog_detail, name="get_blog_detail"),
    path('blog/<str:month>', get_archieve, name="get_archieve"),
    path('blog/category/<str:cat_id>', get_category_blog, name='get_category_blog'),
    path("contact/", contact, name="contact"),

]

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, UpdateView
from django.contrib.auth.models import User
from goodsApp.forms import *
from django.db.models import Q
from .models import *
from django.http import HttpResponse, JsonResponse
import calendar


def category_filter(name):
    category = Category.objects.all()
    result = []
    for i in category:
        events = eval(f'i.{name}_set.all()')
        # events = i.event_set.all()
        if events:
            result.append(i)
    return result


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = AboutPage.objects.last()
        return context


class PartnerView(ListView):
    model = Partner
    context_object_name = 'partners'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = Products.objects.order_by('-created_at')[0:8]
        context["blogs"] = Post.objects.order_by('?')[0:3]
        context["products"] = Products.objects.order_by('?')[0:3]
        try:
            context['backgrounds'] = HeaderModel.objects.all().first().backgroundimage_set.all()
            context['header'] = HeaderModel.objects.all()[0]
        except:
            pass

        context['randoms'] = Products.objects.all()[0:7]
        context['events'] = Event.objects.all()[0:9]
        print(context)
        return context


def get_blog(request):
    post_list = Post.objects.all()

    if request.method == 'POST':
        search = request.POST.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=search) | Q(text__icontains=search) | Q(description__icontains=search))

    paginator = Paginator(post_list, 2)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts
    }
    return render(request, 'blog.html', context)


def get_blog_detail(request, id):
    post = Post.objects.get(id=id)

    context = {
        'post': post
    }
    return render(request, 'blog-detail.html', context)


# ----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------API for jquery drop down------------------------------

def sorting(request, sort_by):
    if request.method == 'POST':
        cat_id = request.POST.get('cat_id')
        if cat_id:
            products = Products.objects.filter(category__id=cat_id).order_by(sort_by)
        else:
            products = Products.objects.order_by(sort_by)
        product_list = list(products.values('id', 'name', 'price', 'image'))

        return JsonResponse(product_list, safe=False)

    # -----------------------------------------------------------------------------------------------------------------


# **********************************************Products***************************************************
def get_products(request):
    product_list = Products.objects.all()
    if request.is_ajax():
        result = []
        for i in product_list:
            obj = {'name': i.name}
            result.append(obj)

        return JsonResponse({
            'name': result
        })

    if request.method == 'POST':
        query = request.POST.get('q')
        product_list = Products.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query) | Q(price__icontains=query) | Q(
                created_at__icontains=query))

    categories = Category.objects.all()

    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    len_product = product_list.count()
    page_num = products.number
    start = (page_num - 1) * 6 + 1
    end = 6 * page_num
    if end > len_product:
        end = len_product

    context = {
        'categories': categories,
        'products': products,
        'len_product': len_product,
        'start': start,
        'end': end,
    }

    return render(request, 'product.html', context)


# ---------------------------------------------------------------Categories----------------------------------------
def get_category(request, cat_id):
    categories = Category.objects.all()
    product_list = Products.objects.filter(category__id=cat_id)

    if request.method == 'POST':  # for searching field in categories
        query = request.POST.get('q')
        product_list = Products.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query) | Q(price__icontains=query) | Q(
                created_at__icontains=query))

    paginator = Paginator(product_list, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    len_product = product_list.count()
    page_num = products.number
    start = (page_num - 1) * 6 + 1
    end = 6 * page_num
    if end > len_product:
        end = len_product

    context = {
        'cat_id': cat_id,
        'categories': categories,
        'products': products,
        'len_product': len_product,
        'start': start,
        'end': end,
    }

    return render(request, 'product.html', context)


# ---------------------------------------------------------Detail Of Product ---------------------------------------
def get_detail(request, prod_id):
    product = Products.objects.get(id=prod_id)
    context = {
        'product': product,
    }
    return render(request, 'product-detail.html', context)


# ------------------------------------------------------------------------------------------------------------------

def create_event(request):
    event_list = Event.objects.all()

    if 'search'  in  request.GET:
        search = request.GET.get('search')
        event_list = Event.objects.filter(
            Q(title__icontains=search) | Q(text__icontains=search) | Q(description__icontains=search))

    paginator = Paginator(event_list, 2)

    first_count = Event.objects.filter(end_date__month=1).count()
    second_count = Event.objects.filter(end_date__month=12).count()
    third_count = Event.objects.filter(end_date__month=11).count()

    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'events': events,
        'first_count': first_count,
        'second_count': second_count,
        'third_count': third_count,
        'categories': category_filter('event')
    }
    return render(request, 'event2.html', context)


def get_event_detail(request, id):
    event = Event.objects.get(id=id)

    context = {
        'event': event,
        'category': category_filter('event'),
    }
    return render(request, 'event-detail.html', context)


def get_event_archieve(request, month):
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    index = months.index(month) + 1
    event_list = Event.objects.filter(end_date__month=index)

    if 'search' in  request.GET:
        search = request.GET.get('search')
        event_list = Event.objects.filter(
            Q(title__icontains=search) | Q(text__icontains=search) | Q(description__icontains=search))

    first_count = Event.objects.filter(end_date__month=1).count()
    second_count = Event.objects.filter(end_date__month=12).count()
    third_count = Event.objects.filter(end_date__month=11).count()

    paginator = Paginator(event_list, 2)

    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'events': events,
        'first_count': first_count,
        'second_count': second_count,
        'third_count': third_count,
        'categories': category_filter('event'),

    }
    return render(request, 'event2.html', context)


def get_category_event(request, slug):
    categories = Category.objects.all()
    event_list = Event.objects.filter(category__slug=slug)

    if 'search' in  request.GET:  # for searching field in categories
        query = request.GET.get('search')
        event_list = Event.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query) | Q(description__contains=query) | Q(
                created_at__icontains=query))

    paginator = Paginator(event_list, 2)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    len_product = event_list.count()
    page_num = products.number
    start = (page_num - 1) * 6 + 1
    end = 6 * page_num
    if end > len_product:
        end = len_product
    # paginator = Paginator(event_list, 2)

    first_count = Event.objects.filter(end_date__month=1).count()
    second_count = Event.objects.filter(end_date__month=12).count()
    third_count = Event.objects.filter(end_date__month=11).count()

    context = {

        'categories': category_filter('event'),
        'events': products,
        'first_count': first_count,
        'second_count': second_count,
        'third_count': third_count,


    }

    return render(request, 'event2.html', context)


# blogs
def get_blog(request):
    post_list = Post.objects.all()

    if 'search' in request.GET:
        search = request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=search) | Q(text__icontains=search) | Q(description__icontains=search))

    paginator = Paginator(post_list, 2)

    first_count = Post.objects.filter(test_date__year=2020, test_date__month=1).count()
    second_count = Post.objects.filter(test_date__year=2019, test_date__month=11).count()
    third_count = Post.objects.filter(test_date__year=2019, test_date__month=12).count()

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'first_count': first_count,
        'second_count': second_count,
        'third_count': third_count,
        'category': category_filter('post')
    }
    return render(request, 'blog.html', context)


def get_blog_detail(request, id):
    post = Post.objects.get(id=id)

    context = {
        'post': post
    }
    return render(request, 'blog-detail.html', context)


def get_archieve(request, month):
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    index = months.index(month) + 1
    post_list = Post.objects.filter(test_date__month=index)

    if request.method == 'POST':
        search = request.POST.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=search) | Q(text__icontains=search) | Q(description__icontains=search))

    first_count = Post.objects.filter(test_date__month=1).count()
    second_count = Post.objects.filter(test_date__month=12).count()
    third_count = Post.objects.filter(test_date__month=11).count()

    paginator = Paginator(post_list, 2)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'category': category_filter('post'),
        'posts': posts,
        'first_count': first_count,
        'second_count': second_count,
        'third_count': third_count,
    }
    return render(request, 'blog.html', context)


def get_category_blog(request, cat_id):
    post_list = Post.objects.filter(category__slug=cat_id)

    if request.method == 'POST':  # for searching field in categories
        query = request.POST.get('q')
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query) | Q(description__contains=query) | Q(
                created_at__icontains=query))

    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    first_count = Post.objects.filter(test_date__month=1).count()
    second_count = Post.objects.filter(test_date__month=12).count()
    third_count = Post.objects.filter(test_date__month=11).count()

    context = {

        'category': category_filter('post'),
        'posts': posts,
        'first_count': first_count,
        'second_count': second_count,
        'third_count': third_count,

    }

    return render(request, 'blog.html', context)


def contact(request):
    context = {}
    context["forms"] = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.info(request, "Ugurla elave olundunuz")
            form.save()
            return redirect('goodsApp:index')
        else:
            messages.error(request, "Form duzgun deyil {}".format(form.errors.as_text))

    return render(request, "contact.html", context)

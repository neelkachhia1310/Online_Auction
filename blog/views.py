from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from orders.models import order
from django.contrib.auth.models import User
from .filters import PostFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def home(request):
    
    posts = Post.objects.all()
    
    return render(request, 'blog/home.html', {'posts':posts})





class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'base_price', 'raising_price', 'product_category', 'date', 'hour', 'minite']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'base_price', 'raising_price', 'product_category', 'date', 'hour', 'minite']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(status="bidding")

class ElectronicListView(ListView):
    model = Post
    template_name = 'blog/electronic.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(status="bidding", product_category="electronic")

class ArtListView(ListView):
    model = Post
    template_name = 'blog/art.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(status="bidding", product_category="art")

class PropertiesListView(ListView):
    model = Post
    template_name = 'blog/properties.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(status="bidding", product_category="propertie")

def electronics(request):
    s = Post.objects.filter(product_category="electronic",status='bidding')
    return render(request, 'blog/electronic.html', {'s': s})

def art(request):
    s = Post.objects.filter(product_category="art",status='bidding')
    return render(request, 'blog/art.html', {'s': s})

def properties(request):
    s = Post.objects.filter(product_category="propertie",status='bidding')
    return render(request, 'blog/properties.html', {'s': s})

def details(request):
    s = Post.objects.get(id=request.GET['num1'])
    return render(request, 'blog/auction.html', {'s': s})


def auction(request):
    s = Post.objects.get(id=request.GET['num1'])
    if (request.GET['inc'] == 'yes'):
        if (s.sell_price == 0):
            s.sell_price = s.base_price
        else:
            s.sell_price = s.raising_price + s.sell_price
        s.status = 'bidding'
        # s.sell_price = 200 + s.sell_price
        s.sell_customer_name = request.user.username
        s.save()
        reload = 'yes'
    else:
        reload = 'no'
    return render(request, 'blog/auction.html', {'s': s, 'reload': reload})

def sold(request):
    s = Post.objects.get(id=request.GET['num1'])

    if(request.GET['do']=='yes'):
        if (s.status == 'bidding' and s.sell_price == 0 ):
            s.status = 'unsold'
        else:
            s.status = 'sold'
        s.save()
    else:
        return render(request, 'blog/auction.html', {'s': s, 'reload': 'no'})

    return render(request, 'blog/sold.html', {'s': s})

class MyItemListView(ListView):
    model = Post
    template_name = 'blog/myitem.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(sell_customer_name=self.request.user.username)

def myitem(request):
    s = Post.objects.filter(sell_customer_name=request.user.username)

    return render(request, 'blog/myitem.html', {'s': s})


class MyaddedListView(ListView):
    model = Post
    template_name = 'blog/myadded.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(author__username=self.request.user.username)

def myadded(request):
    s = Post.objects.filter(author__username=request.user.username)

    return render(request, 'blog/myadded.html', {'s': s})

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)

def history(request):
    s = Post.objects.filter(status="sold") | Post.objects.filter(status="unsold")

    return render(request, 'blog/history.html', {'s': s})

class PostFilterListView(ListView):
    model=Post
    template_name = 'blog/searchpost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

def products_payment(request):
    s = Post.objects.get(id=request.GET['num1'])
    if(request.user.username != s.sell_customer_name):
        return render(request, 'blog/history.html', {'s': s})
    else:
        return render(request, 'blog/payment_page.html', {'s': s})

def checkout(request):
    if request.method == "POST":
        name = request.POST.get('firstname','')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip = request.POST.get('zip','')
        #product_id3 = request.POST.get('productid','')
        username = request.user.username
        id3=request.GET['num1']
        oo = order(payment_status="complete",name=name,email=email,address=address,city=city,state=state,zipcode=zip,product_id = id3)
        oo.save()
        #product_id = int(product_id3)
        confer = Post.objects.get(id= id3)
        if confer.sell_customer_name != username:
            return render(request, 'post/myitem/')
        payment_done = Post.objects.get(sell_customer_name=username, id= id3)
        payment_done.payment_status = "complete"
        payment_done.save()

        subject = "Payment Successful"
        message = "Payment is successful for your order. \n Total Ammount ="+str(payment_done.sell_price) + "\n Name="+name+"\n Address="+address+"\n City="+city+"\n State="+state+"\n Zipcode="+str(zip)
        from_email = settings.EMAIL_HOST_USER
        email_user = email
        to_list = [  email_user ]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return render(request, 'blog/payment_done.html', {'product': payment_done , 'sender1': oo})
    else:
        return render(request, 'post/myitem/')


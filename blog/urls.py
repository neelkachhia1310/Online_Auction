from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostFilterListView,
    ElectronicListView,
    ArtListView,
    PropertiesListView,
    MyaddedListView,
    MyItemListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('electronics/',ElectronicListView.as_view() , name='electronic'),
    path('art/', ArtListView.as_view(), name='art'),
    path('properties/', PropertiesListView.as_view(), name='properties'),
    path('history/', views.history, name='history'),
    path('searchpost/', views.PostFilterListView.as_view(), name='search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/live_auc/',views.details, name="detail-auc"),
    path('post/live_auction/',views.auction, name="auction-live"),
    path('post/sold/',views.sold, name="sold-auc"),
    path('post/myitem/',MyItemListView.as_view(), name="sold-adwae"),
    path('post/myadded/',MyaddedListView.as_view(), name="addeddwae"),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/product_payment/',views.products_payment, name="products_payment"),
    path('post/checkout/',views.checkout, name="checkout"),
    
]

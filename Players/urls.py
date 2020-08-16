from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('searchplayer/', views.PlayerListView.as_view(), name='search'),
    path('auction/',views.auction),
    path('details/',views.details),
    path('sold/',views.sold,name="sold"),
    path('history/',views.history,name='history'),
    path('your_players/',views.your_players,name='history'),
    
]

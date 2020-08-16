from django.shortcuts import render, redirect
from .models import player
from users.models import Profile
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .filters import PlayerFilter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
    pla = player.objects.filter(status='bidding')
    return render(request, 'index.html', {'pla': pla})


def about(request):
    return render(request, 'about.html')


def auction(request):
    s = player.objects.get(player_name=request.GET['num1'])
    reload='yes'
    if (request.GET['inc'] == 'yes'):
        if (s.sell_price == 0):
            s.sell_price = s.base_price
        else:
            s.sell_price = s.raising_price + s.sell_price
        s.status = 'bidding'
        # s.sell_price = 200 + s.sell_price
        s.sell_teamName = request.user.username
        s.save()
    else:
        reload = 'no'
        
    try:
        v = Profile.objects.get(user__username=request.user.username)
    except Profile.DoesNotExist:
        v = None

    return render(request, 'auction.html', {'s': s, 'reload': reload, 'v': v})

def details(request):
    s = player.objects.get(player_name=request.GET['num1'])
    try:
        v = Profile.objects.get(user__username=request.user.username)
    except Profile.DoesNotExist:
        v = None

    return render(request, 'auction.html', {'s': s, 'v':v })

def sold(request):
    s = player.objects.get(player_name=request.GET['num1'])
    if (s.status == 'bidding' and s.sell_price == 0):
        s.status = 'unsold'
    else:
        s.status = 'sold'
    s.save()
    return render(request, 'sold.html', {'s': s})


def history(request):
    s = player.objects.filter(status="sold") | player.objects.filter(status="unsold")

    return render(request, 'history.html', {'s': s})

@login_required
def your_players(request):
    s1 = player.objects.filter(sell_teamName=request.user.username, player_role='Batsman')
    s2 = player.objects.filter(sell_teamName=request.user.username, player_role='Bowler')
    s3 = player.objects.filter(sell_teamName=request.user.username, player_role='AllRounder')
    return render(request, 'your_players.html', {'s1': s1, 's2': s2, 's3': s3})

class PlayerListView(ListView):
    model=player
    template_name = 'searchplayer.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PlayerFilter(self.request.GET, queryset=self.get_queryset())
        return context
    

    


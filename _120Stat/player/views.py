from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from .models import Player

def index(request):
	all_players = Player.objects.all()
	context = {
		'all_players': all_players
	}
	return render(request, 'player/index.html', context)

def detail(request, player_id):
	try:
		player = Player.objects.get(pk = player_id)
	except Player.DoesNotExist:
		raise Http404("Player does not exist") 
	return render(request, 'player/detail.html', {'player': player})


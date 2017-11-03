from django.http import HttpResponse
from .models import Player

def index(request):
	all_players = Player.objects.all()
	html = ''
	for player in all_players:
		url = '/player/' + str(player.id) + '/'
		html += '<a href= "' + url + '">' + player.lastname + '</a><br>'
	return HttpResponse(html)

def detail(request, player_id):
	return HttpResponse("<h2>Details for player (Zaq is a fucker). Id: " + str(player_id) + "</h2>")

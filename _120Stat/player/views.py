from django.shortcuts import render, get_object_or_404
from .models import Player, YearStats

def index(request):
	all_players = Player.objects.all()
	context = {
		'all_players': all_players
	}
	return render(request, 'player/index.html', context)

def detail(request, player_id):
	player = get_object_or_404(Player, pk=player_id)
	# try:
	# 	player = Player.objects.get(pk = player_id)
	# except Player.DoesNotExist:
	# 	raise Http404("Player does not exist") 
	return render(request, 'player/detail.html', {'player': player})

def important(request, player_id):
	player = get_object_or_404(Player, pk=player_id)
	try: 
		selected_year = player.yearstats_set.get(pk = request.POST['yearstat'])
	except (KeyError, YearStats.DoesNotExist):
		return render( request, 'player/detail.html', {
			'player': player,
			'error_message': "You did not select a valid year",
		})
	else:
		selected_year.is_important = True
		selected_year.save()
		return render(request, 'player/detail.html', {'player': player})

'''
    Contains view for Stats
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.forms.formsets import formset_factory

from stats.models import Player
from stats.forms import PlayerForm

def about_view(request):
    ''' This view simply renders the About page '''
    template_name = "stats/about.html"

    return render(request, template_name)


class HomeView(TemplateView):
    '''
        This view will render a set of forms for users to enter player names.
        It also will process user input to get player names, calling StatView to
        process and display player stats.
    '''

    template_name = "stats/home.html"
    PlayerFormSet = formset_factory(PlayerForm, extra=4)

    def get(self, request):
        ''' Render home.html, passing in our form, when a user visits home page '''
        return render(request, self.template_name, {'formset': self.PlayerFormSet})

    def post(self, request):
        '''
            Gathers user input and validates it upon the user clicking the Submit button.
            Calls StatView to display the stats
        '''
        formset = self.PlayerFormSet(request.POST)
        players = list()

        if formset.is_valid():
            for form in formset:
                # will hold player name if a name was in the form
                # or false otherwise
                player_name = form.cleaned_data.get('player_name', False)
                if player_name != False:
                    # can use nfldb.player_search(db, player_name) to determine player name
                    #  - protects against slight misspellings
                    # see https://github.com/BurntSushi/nfldb/wiki/Fuzzy-player-name-matching
                    players.append(player_name.title())

            request.session['players'] = players

            return StatView.as_view()(request)
            # return redirect('stats:statistics')

        # if data invalid, request user input again. Need to show some sort of error here too.
        return render(request, self.template_name, {'formset': formset})

class StatView(ListView):
    '''
        This view will be called by HomeView. It can receive player names entered by the user,
        process the names to get stats, and display the stats.
    '''

    template_name = 'stats/statistics.html'

    def post(self, request):
        '''
            This function is called when a POST request is made when HomeView renders this page.
            It creates the player objects and renders the statistics page that displays the stats.
        '''


        player_names = request.session['players']

        players = list()
        for player in player_names:
            players.append(Player(player, None))

        player_dict = {}
        for player in players:
            player_dict[player.name] = player.get_player()
        '''
        data_dict format:

            Players: {
                            "Player Name": {
                                            BasicInfo: {"info1": n
                                                        "info2": n}
                                            CareerStats: {"stat1": n
                                                          "stat2": n}
                                            FantasyStats: {"stat1": n
                                                           "stat2": n}
                                            YearlyStats: {
                                                          year1: {
                                                                  Summary: {"stat1": n
                                                                            "stat2": n}
                                                                  1: {"stat1": n
                                                                      "stat2": n} }    <--- list of week numbers with stats
                                                          year2: ...
                                                         }
                                            }
                            }
        '''
        data_dict = {}
        data_dict['Players'] = player_dict
        return render(request, self.template_name, data_dict)

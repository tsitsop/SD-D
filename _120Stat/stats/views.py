# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import PlayerForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.forms.formsets import formset_factory

from stats.models import Player

import nfldb

class ContactView(TemplateView):
    template_name = "stats/basic.html"
    def get(self, request):
        return render(request,self.template_name,{'content':["Names","Zachary Maurer"]})

class HomeView(TemplateView):
    '''
        This view will render a set of forms for users to enter player names.
        It also will process user input to get player names, calling StatView to
        process and display player stats.
    '''

    template_name = "stats/home.html"
    PlayerFormSet = formset_factory(PlayerForm, extra=4)

    def get(self, request):
        # will render home.html, passing in our form
        return render(request, self.template_name, {'formset': self.PlayerFormSet})

    # when the user hits submit, a POST request is created. The below function is called.
    def post(self, request):
        formset = self.PlayerFormSet(request.POST)
        players = list()

        if formset.is_valid():
            for form in formset:
                # will hold player name if a name was in the form
                # or false otherwise
                player_name = form.cleaned_data.get('player_name', False)
                if player_name != False:
                    players.append(player_name)

            request.session['players'] = players

            return StatView.as_view()(request)
            # return redirect('stats:statistics')

        # if data invalid, request user input again. Need to show some sort of error here too.
        return render(request, self.template_name, {'form': form})

class StatView(ListView):
    '''
        This view will be called by HomeView. It can receive player names entered by the user,
        process the names to get stats, and display the stats.
    '''

    template_name = 'stats/test.html'

    def post(self,request):
        player_names = request.session['players']

        players = list()
        for player in player_names:
            players.append(Player(player))

        dataDict = {}
        playerDict = {}
        dataDict['year'] = 2015

        for player in players:
            playerDict[player.name] = {}
            playerDict[player.name]["BasicInfo"] = player.get_info()
            playerDict[player.name]["CarrerStats"] = player.get_stats()
            playerDict[player.name]["FantasyStats"] = player.get_fantasy()
            playerDict[player.name]["YearlyStats"] = player.get_yearly_stats()
        dataDict['players'] = playerDict
        '''
        dataDict = {

                    year: number
                    players:{
                                "Player Name": {

                                                    BasicInfo: [("stat1",n),]
                                                    CarrerInfo: [("stat1",n),]
                                                    FantasyStats:
                                                    YearlyStats: [[year1]
                                                                  [year2]]
                                             }
                            }

                    }
        '''
        return render(request,self.template_name,dataDict)

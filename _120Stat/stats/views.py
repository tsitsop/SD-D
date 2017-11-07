# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import PlayerForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.forms.formsets import formset_factory

from _120_Player.Player import Player
import nfldb

class ContactView(TemplateView):
    template_name = "stats/basic.html"
    def get(self, request):
        return render(request,self.template_name,{'content':["Names","Zachary Maurer"]})

class HomeView(TemplateView):
    template_name = "stats/home.html"
    PlayerFormSet = formset_factory(PlayerForm, extra=2)
    
    def get(self, request):
        # will render home.html, passing in our form
        return render(request, self.template_name, {'formset': self.PlayerFormSet})

    # when the user hits submit, a POST request is created. The below function is called.
    def post(self, request):
        formset = self.PlayerFormSet(request.POST)
        players = list()

        if formset.is_valid():
            for form in formset:
                players.append(form.cleaned_data['player_name'])

            request.session['players'] = players

            return StatView.as_view()(request)
            # return redirect('stats:statistics')

        # if data invalid, request user input again. Need to show some sort of error here too.
        return render(request, self.template_name, {'form': form})

class StatView(ListView):
    template_name = 'stats/statistics.html'

    def post(self,request):

        db = nfldb.connect()

        player_names = request.session['players']

        players = list()
        for player in player_names:
            players.append(Player(player, db, 2015))
            
        dataDict = {}
        playerDict = {}
        dataDict['year'] = 2015

        for player in players:
            playerDict[player.name] = player.getData()

        dataDict['players'] = playerDict

        '''
        dataDict = {

                    year: number
                    players:{
                                "Tom Brady": [("stat1",n),]
                                "Other Guy": [("stat1",n),]
                            }

                    }
        '''
        return render(request,self.template_name,dataDict)

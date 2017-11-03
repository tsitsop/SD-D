# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import PlayerForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from _120_Player.Player import Player
import nfldb

class ContactView(TemplateView):
    template_name = "stats/basic.html"
    def get(self, request):
        return render(request,self.template_name,{'content':["Names","Zachary Maurer"]})

class HomeView(TemplateView):
    template_name = "stats/home.html"
    def get(self, request):
        form = PlayerForm()

        # will render home.html, passing in our form
        return render(request, self.template_name, {'form': form})

    # when the user hits submit, a POST request is created. The below function is called.
    def post(self, request):
        # fills the form out witht he data received from POST request
        form = PlayerForm(request.POST)

        if form.is_valid():
            # makes sure no SQL injections???? also, 'player_name' is the name of the field.
            # we defined it in forms.py
            player_name = form.cleaned_data['player_name']

            # if valid data, we want to render our statistics page. Need to get the player data too.

            request.session['player_1'] = player_name
            request.session['player_2'] = "Philip Rivers"
            return StatView.as_view()(request)

        # if data invalid, request user input again. Need to show some sort of error here too.
        return render(request, self.template_name, {'form': form})

class StatView(ListView):
    template_name = 'stats/statistics.html'

    def post(self,request):

        db = nfldb.connect()

        player1_name = request.session['player_1']
        player2_name = request.session['player_2']

        player1 = Player(player1_name,db,2015)
        player2 = Player(player2_name,db,2015)

        player1.update()
        player2.update()

        dataDict = {}
        playerDict = {}
        dataDict['year'] = 2015

        playerDict[player1_name] = player1.getData()
        playerDict[player2_name] = player2.getData()

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

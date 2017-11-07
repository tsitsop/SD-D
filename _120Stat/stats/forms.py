from django import forms
    
class PlayerForm(forms.Form):
    player_name = forms.CharField()
    
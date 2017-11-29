from django import forms
    
class PlayerForm(forms.Form):
    player_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Player Name'}))
    
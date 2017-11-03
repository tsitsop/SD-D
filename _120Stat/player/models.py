from django.db import models

#Tom Brady primarykey 1
class Player(models.Model):
	firstname = models.CharField(max_length = 200)
	lastname = models.CharField(max_length = 200)
	team = models.CharField(max_length = 100)
	team_logo = models.CharField(max_length = 500)

	def __str__(self):
		return self.firstname + ' ' + self.lastname

class YearStats(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	year = models.IntegerField(default = 0)
	passingyards = models.IntegerField()
	rushingyards = models.IntegerField()

	def __str__(self):
		return str(self.player) + ' ' + str(self.year)

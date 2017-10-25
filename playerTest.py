import nfldb
from Player import Player
db = nfldb.connect()

Tom = Player("Tom Brady",db,2015)
print Tom.update()
#print "Tom Brady"
#print Tom.getData()
print"===================="

Todd = Player("Todd Gurley",db,2015)
print Todd.update()

#print "Todd Gurley"
#print Todd.getData()

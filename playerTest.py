import nfldb
from Player import Player
db = nfldb.connect()


Tom = Player("Tom Brady",db,2015)

print Tom.getData()

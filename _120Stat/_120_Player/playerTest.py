import nfldb
from Player import Player
import nfldb.types as types

db = nfldb.connect()



Tom = Player("Tom Brady",db,2015)
Tom.update()
print "Tom Brady"
d = Tom.getData()
for e in d:
    print e[0],":",e[1]

print"===================="
Todd = Player("Todd Gurley",db,2015)
Todd.update()
print "Todd Gurley"
d = Todd.getData()
for e in d:
    print e[0],":",e[1]


Antonio = Player("Antonio Brown",db,2015)
Antonio.update()
print "=================="
print "Antonio Brown"

d = Antonio.getData()

for e in d:
    print e[0],":",e[1]

Blair = Player("Blair Walsh",db,2015)
Blair.update()
print "=================="
print "Blair Walsh"

d = Blair.getData()

for e in d:
    print e[0],":",e[1]

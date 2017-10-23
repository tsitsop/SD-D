import nfldb


class Player:
   def __init__(self,name,data,year):
      self.name = name
      self.db = data
      self.year = year
   def getData(self):
      q = nfldb.Query(self.db)
      q.game(season_year=self.year, season_type='Regular')
      q.player(full_name=self.name)
      r = []
      for y in q.as_aggregate():
          #Debug Stuff
          print self.name
          print "Receiving Yards: ",y.receiving_yds
          print "Rushing Yards: ",y.rushing_yds
          print "Passing Yards: ",y.passing_yds
          print "Offensive Touchdowns: ",y.offense_tds
          print "Points: ",y.points
          print "Was Sacked: ",y.passing_sk
          print "Rusing Attempts",y.rushing_att
          r = [y.receiving_yds,y.rushing_yds,y.passing_yds]
      return r

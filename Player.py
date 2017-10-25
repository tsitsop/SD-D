import nfldb
import nfldb.types as types

class Player:
   def __init__(self,name,data,year):
      self.name = name
      self.db = data
      self.year = year
   def update(self):
    q = nfldb.Query(self.db)
    q.game(season_year=self.year, season_type='Regular')
    q.player(full_name=self.name)

    for y in q.as_aggregate():


	#Incomplete list of stats per position, need to coordinate with someone who knows more about football

            #If player is Quarterback
        pos = y.guess_position
        if pos == types.Enums.player_pos.QB:
            #Stats we care about
            self.defense_tkl = y.defense_tkl

            self.receiving_rec = y.receiving_rec
            self.receiving_yds = y.receiving_yds
            self.receiving_tar = y.receiving_tar
            self.receiving_yac_yds = y.receiving_yac_yds


            self.rushing_yds = y.rushing_yds
            self.rushing_att = y.rushing_att

            self.passing_int = y.passing_int
            self.passing_sk = y.passing_sk
            self.passing_cmp = y.passing_cmp
            self.passing_incmp = y.passing_incmp
            self.passing_tds = y.passing_tds
            self.passing_incmp_air_yds = y.passing_incmp_air_yds
            self.passing_cmp_air_yds = y.passing_cmp_air_yds
            self.passing_sk_yds = y.passing_sk_yds
            self.passing_att = y.passing_att
            self.passing_yds = y.passing_yds

            self.fumbles_rec = y.fumbles_rec
            self.fumbles_tot = y.fumbles_tot
            self.fumbles_forced = y.fumbles_forced
            self.fumbles_lost = y.fumbles_lost

            #Stats we dont
            self.rushing_twoptmissed = None
            self.rushing_twopta = None
            self.rushing_tds = None

        elif pos == types.Enums.player_pos.RB:
            #Stats we care about
            self.rushing_twoptmissed = y.rushing_twoptmissed
            self.rushing_twopta = y.rushing_twopta
            self.rushing_tds = y.rushing_tds
            self.fumbles_tot = y.fumbles_tot
            self.fumbles_forced = y.fumbles_forced
            self.fumbles_lost = y.fumbles_lost
            self.receiving_yac_yds = y.receiving_yac_yds
            self.receiving_rec = y.receiving_rec
            self.rushing_yds = y.rushing_yds
            self.receiving_yds = y.receiving_yds
            self.rushing_att = y.rushing_att
            self.receiving_tar = y.receiving_tar
            #Stats we dont
            self.defense_tkl = None

            self.passing_int = None
            self.passing_sk = None
            self.passing_cmp = None
            self.passing_incmp = None
            self.passing_tds = None
            self.passing_incmp_air_yds = None
            self.passing_cmp_air_yds = None
            self.passing_sk_yds = None
            self.passing_att = None
            self.passing_yds = None

            self.fumbles_rec = None


        r = y
    return r
   def getData(self):
	#adding more
       r = []
       r.append(("Defensive Tackles",self.defense_tkl))
       r.append(("Recieving Yards",self.receiving_yds))
       r.append(("Rushing Yards",self.rushing_yds))
       r.append(("Passing Interceptions",self.passing_int))
       r.append(("Fumbles Recovered",self.fumbles_rec))
       r.append(("Passing Yards",self.passing_yds))
       return r

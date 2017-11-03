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
            #If player is Quarterback
        self.pos = y.guess_position
        if self.pos == types.Enums.player_pos.QB:
            #Stats we care about
            self.passing_att = y.passing_att
            self.passing_cmp = y.passing_cmp
            self.passing_incmp = y.passing_incmp
            self.passing_yds = y.passing_yds
            self.passing_tds = y.passing_tds
            self.passing_int = y.passing_int

            self.fumbles_tot = y.fumbles_tot
            self.fumbles_lost = y.fumbles_lost

            self.passing_sk = y.passing_sk
            self.rushing_yds = y.rushing_yds
            self.rushing_att = y.rushing_att
            self.rushing_tds = y.rushing_tds



            #Stats we dont
            '''
            self.rushing_twoptmissed = None
            self.rushing_twopta = None
            self.defense_tkl = y.defense_tkl
            self.receiving_rec = y.receiving_rec
            self.receiving_yds = y.receiving_yds
            self.receiving_tar = y.receiving_tar
            self.receiving_yac_yds = y.receiving_yac_yds
            self.passing_incmp_air_yds = y.passing_incmp_air_yds
            self.passing_cmp_air_yds = y.passing_cmp_air_yds
            self.passing_sk_yds = y.passing_sk_yds
            self.fumbles_rec = y.fumbles_rec
            self.fumbles_forced = y.fumbles_forced
            '''
        elif self.pos == types.Enums.player_pos.RB:
            #Stats we care about

            self.rushing_att = y.rushing_att
            self.rushing_yds = y.rushing_yds
            self.rushing_tds = y.rushing_tds
            self.fumbles_tot = y.fumbles_tot
            self.fumbles_lost = y.fumbles_lost
            self.receiving_tar = y.receiving_tar
            self.receiving_rec = y.receiving_rec
            self.receiving_yds = y.receiving_yds
            self.receiving_tds = y.receiving_tds
            self.receiving_yac_yds = y.receiving_yac_yds

            #Stats we dont
            '''
            self.rushing_twoptmissed = y.rushing_twoptmissed
            self.rushing_twopta = y.rushing_twopta
            self.fumbles_forced = y.fumbles_forced


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
            '''
        elif self.pos == types.Enums.player_pos.WR or  self.pos == types.Enums.player_pos.TE:
            #Stats we care about
            self.fumbles_tot = y.fumbles_tot
            self.fumbles_lost = y.fumbles_lost
            self.receiving_tar = y.receiving_tar
            self.receiving_rec = y.receiving_rec
            self.receiving_yds = y.receiving_yds
            self.receiving_tds = y.receiving_tds
            self.receiving_yac_yds = y.receiving_yac_yds

        elif self.pos == types.Enums.player_pos.K:
            #Stats we care about
            '''
                - field goals attempted
                - field goals missed
                - extra points attempted
                - extra points missed
                -- if they store stuff based on yardage we also want that. Ideally want the distance for each kick, and if the kicker did/didnt make it

                {'kicking_i20': 10L,
                 'kicking_fgm_yds': 1264L,
                  'kicking_all_yds': 3481L,
                   'kicking_fgmissed_yds': 225L,
                    'kicking_tot': 86L,
                     'kicking_touchback': 47L,
                      'kicking_fgmissed': 5L,
                       'kicking_xpmade': 30L,
                       'kicking_yds': 5651L,
                       'kicking_fgb': 1L,
                       'kicking_fga': 39L,
                       'kicking_xpmissed': 3L,
                        'kicking_fgm': 34L,
                         'kicking_xpa': 33L}


            '''
            self.kicking_fga = y.kicking_fga
            self.kicking_fgmissed = y.kicking_fgmissed
            self.kicking_xpa = y.kicking_xpa
            self.kicking_xpmissed = y.kicking_xpmissed

            self.kicking_fgm_yds = y.kicking_fgm_yds

   def getData(self):
    r = []
    if self.pos == types.Enums.player_pos.QB:
        r.append(("Passing Attempts",self.passing_att))
        r.append(("Passing Completions",self.passing_cmp))
        r.append(("Passing Incompletions",self.passing_incmp))
        r.append(("Passing Yards",self.passing_yds))
        r.append(("Passing Touchdowns",self.passing_tds))
        r.append(("Passing Interceptions",self.passing_int))

        r.append(("Fumbles Total",self.fumbles_tot))
        r.append(("Fumbles lost",self.fumbles_lost))

        r.append(("Passing Sacks",self.passing_sk))
        r.append(("Rushing Yards",self.rushing_yds))
        r.append(("Rushing Attempts",self.rushing_att))
        r.append(("Rushing Touchdowns",self.rushing_tds))
    elif self.pos == types.Enums.player_pos.RB:
        r.append(("Rushing Attempts",self.rushing_att))
        r.append(("Rushing Yards",self.rushing_yds))
        r.append(("Rushing Touchdowns",self.rushing_tds))
        r.append(("Fumbles Total",self.fumbles_tot))
        r.append(("Fumbles Lost",self.fumbles_lost))
        r.append(("Recieving Targets",self.receiving_tar))
        r.append(("Recieving Receptions",self.receiving_rec))
        r.append(("Recieving Yards",self.receiving_yds))
        r.append(("Recieving Touchdowns",self.receiving_tds))
        r.append(("Recieving Yards after catch (yac)",self.receiving_yac_yds))
    elif self.pos == types.Enums.player_pos.WR or  self.pos == types.Enums.player_pos.TE:
        r.append(("Fumbles Total",self.fumbles_tot))
        r.append(("Fumbles Lost",self.fumbles_lost))
        r.append(("Recieving Targets",self.receiving_tar))
        r.append(("Recieving Receptions",self.receiving_rec))
        r.append(("Recieving Yards",self.receiving_yds))
        r.append(("Recieving Touchdowns",self.receiving_tds))
        r.append(("Recieving Yards after catch (yac)",self.receiving_yac_yds))
    elif self.pos == types.Enums.player_pos.K:
        r.append(("Field Goals Attempted",self.kicking_fga))
        r.append(("Field Goals Missed",self.kicking_fgmissed))
        r.append(("Extra Points Attempted",self.kicking_xpa))
        r.append(("Extra Points Missed",self.kicking_xpmissed))

        r.append(("Field Goal Made Yards",self.kicking_fgm_yds))

    return r

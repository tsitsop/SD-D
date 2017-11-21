# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import nfldb
import nfldb.types as types
from enum import Enum



class BasicInfo(object):
    def __init__(self, name):
        self.name = name

        # connect to database to get info
        db = nfldb.connect()

        q = nfldb.Query(db)
        q.player(full_name=name)

        # this currently gets the first player returned
        #  so we may need to change in future
        info = q.as_players()[0] 
        
        # store basic info
        self.position = info.position
        self.uniform_number = info.uniform_number
        self.birthdate = info.birthdate
        self.height = info.height
        self.weight = info.weight
        self.college = info.college
        self.status = info.status
        self.team = info.team
        self.years_pro = info.years_pro

    def get_basic_info(self):
        data = list()

        data.append(("Position", self.position))
        data.append(("Uniform Number", self.uniform_number))
        data.append(("Birthdate", self.birthdate))
        data.append(("Height", self.height))
        data.append(("Weight", self.weight))
        data.append(("College", self.college))
        data.append(("Status", self.status))
        data.append(("Team", self.team))
        data.append(("Years Pro", self.years_pro))

        return data


class PositionStats(object):
    def __init__(self):
        self.passing_att = 0
        self.passing_cmp = 0
        self.passing_incmp = 0
        self.passing_yds = 0
        self.passing_incmp_air_yds = 0
        self.passing_cmp_air_yds = 0
        self.passing_tds = 0
        self.passing_int = 0
        self.passing_sk = 0

        self.rushing_att = 0
        self.rushing_yds = 0
        self.rushing_tds = 0

        self.receiving_tar = 0
        self.receiving_rec = 0
        self.receiving_yds = 0
        self.receiving_tds = 0
        self.receiving_yac_yds = 0

        self.fumbles_tot = 0
        self.fumbles_lost = 0

        self.kicking_fga = 0
        self.kicking_fgm = 0
        self.kicking_fgmissed = 0

        # maybe -- depends how this works. need to see if per kick or total kicks
        self.kicking_fgm_yds = 0
        self.kicking_fgmissed_yds = 0

        self.kicking_xpa = 0
        self.kicking_xpmade = 0
        self.kicking_xpmissed = 0

    def get_stats(self):
        data = list()

        data.append(("Passing Attempts", self.passing_att))
        data.append(("Passing Completions", self.passing_cmp))
        data.append(("Passing Incompletions", self.passing_incmp))
        data.append(("Passing Yards", self.passing_yds))
        data.append(("Passing Touchdowns", self.passing_tds))
        data.append(("Passing Interceptions", self.passing_int))
        data.append(("Passing Sacks", self.passing_sk))

        data.append(("Rushing Yards", self.rushing_yds))
        data.append(("Rushing Attempts", self.rushing_att))
        data.append(("Rushing Touchdowns", self.rushing_tds))

        data.append(("Recieving Targets", self.receiving_tar))
        data.append(("Recieving Receptions", self.receiving_rec))
        data.append(("Recieving Yards", self.receiving_yds))
        data.append(("Recieving Touchdowns", self.receiving_tds))
        data.append(("Recieving Yards After Catch (YAC)", self.receiving_yac_yds))

        data.append(("Fumbles Total", self.fumbles_tot))
        data.append(("Fumbles Lost", self.fumbles_lost))

        data.append(("Field Goals Attempted", self.kicking_fga))
        data.append(("Field Goals Missed", self.kicking_fgmissed))
        data.append(("Field Goal Made Yards", self.kicking_fgm_yds))
        data.append(("Extra Points Attempted", self.kicking_xpa))
        data.append(("Extra Points Missed", self.kicking_xpmissed))
        # may be missing some kicking stats

        return data


class QuarterbackStats(PositionStats):
    def __init__(self, name, position):
        super(QuarterbackStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)
        q.game(season_type='Regular')
        q.player(full_name=name, position=position)

        stats = q.as_aggregate()[0]

        self.passing_att = stats.passing_att
        self.passing_cmp = stats.passing_cmp
        self.passing_incmp = stats.passing_incmp
        self.passing_yds = stats.passing_yds
        self.passing_incmp_air_yds = stats.passing_incmp_air_yds
        self.passing_cmp_air_yds = stats.passing_cmp_air_yds
        self.passing_tds = stats.passing_tds
        self.passing_int = stats.passing_int
        self.passing_sk = stats.passing_sk

        self.rushing_att = stats.rushing_att
        self.rushing_yds = stats.rushing_yds
        self.rushing_tds = stats.rushing_tds

        self.fumbles_tot = stats.fumbles_tot
        self.fumbles_lost = stats.fumbles_lost


class RunningbackStats(PositionStats):
    def __init__(self, name, position): 
        super(RunningbackStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)
        q.game(season_type='Regular')
        q.player(full_name=name, position=position)

        stats = q.as_aggregate()[0]

        self.rushing_att = stats.rushing_att
        self.rushing_yds = stats.rushing_yds
        self.rushing_tds = stats.rushing_tds

        self.fumbles_tot = stats.fumbles_tot
        self.fumbles_lost = stats.fumbles_lost

        self.receiving_tar = stats.receiving_tar
        self.receiving_rec = stats.receiving_rec
        self.receiving_yds = stats.receiving_yds
        self.receiving_tds = stats.receiving_tds
        self.receiving_yac_yds = stats.receiving_yac_yds


class WideReceiverTightEndStats(PositionStats):
    def __init__(self, name, position):
        super(WideReceiverTightEndStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)
        q.game(season_type='Regular')
        q.player(full_name=name, position=position)

        stats = q.as_aggregate()[0]

        self.fumbles_tot = stats.fumbles_tot
        self.fumbles_lost = stats.fumbles_lost

        self.receiving_tar = stats.receiving_tar
        self.receiving_rec = stats.receiving_rec
        self.receiving_yds = stats.receiving_yds
        self.receiving_tds = stats.receiving_tds
        self.receiving_yac_yds = stats.receiving_yac_yds


class KickerStats(PositionStats):
    def __init__(self, name, position):
        super(KickerStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)
        q.game(season_type='Regular')
        q.player(full_name=name, position=position)

        stats = q.as_aggregate()[0]

        self.kicking_fga = stats.kicking_fga
        self.kicking_fgm = stats.kicking_fgm
        self.kicking_fgmissed = stats.kicking_fgmissed

        # maybe -- depends how this works. need to see if per kick or total kicks
        self.kicking_fgm_yds = stats.kicking_fgm_yds
        self.kicking_fgmissed_yds = stats.kicking_fgmissed_yds

        self.kicking_xpa = stats.kicking_xpa
        self.kicking_xpmade = stats.kicking_xpmade
        self.kicking_xpmissed = stats.kicking_xpmissed


class Player(object):
    def __init__(self, name):
        self.name = name

        self.basic_info = BasicInfo(name)

        position = self.basic_info.position

        # all of the classes here get CAREER stats - will need to modify to get yearly stats
        if position == types.Enums.player_pos.QB:
            self.position_stats = QuarterbackStats(name, position)
        elif position == types.Enums.player_pos.RB:
            self.position_stats = RunningbackStats(name, position)
        elif position == types.Enums.player_pos.WR or position == types.Enums.player_pos.WR:
            self.position_stats = WideReceiverTightEndStats(name, position)
        elif position == types.Enums.player_pos.K:
            self.position_stats = KickerStats(name, position)

        self.fantasy_stats = fantasy_scores(self.position_stats, 'Espn_Standard_Scoring')

    def get_data(self):
        data = list()

        basic = self.basic_info.get_basic_info()
        stats = self.position_stats.get_stats()
        # need to add get_scoring() for fantasy

        # Should probably do something different with return value.
        #  Will want to distinguish between these
        #  Dict of lists? 1st list is of basic info, 2nd of stats, 3rd of fantasy stuff
        data = basic + stats

        return data

class Espn_Standard_Scoring(Enum):
    PASSING_YDS = 0.04
    PASSING_TDS = 4
    PASSING_INT = -2

    RUSHING_YDS = 0.1
    RUSHING_TDS = 6

    RECEIVING_YDS = 0.1
    RECEIVING_TDS = 6

    FUMBLES_LOST = -2

    # Kicking won't work until figure out distance of each kick

class fantasy_scores(object):
    def __init__(self, position_stats, scoring_system):
        # default scoring system is ESPN standard
        scoring = Espn_Standard_Scoring

        self.passing_yds = position_stats.passing_yds * scoring.PASSING_YDS.value
        self.passing_tds = position_stats.passing_tds * scoring.PASSING_TDS.value
        self.passing_int = position_stats.passing_int * scoring.PASSING_INT.value

        self.rushing_yds = position_stats.rushing_yds * scoring.RUSHING_YDS.value
        self.rushing_tds = position_stats.rushing_tds * scoring.RUSHING_TDS.value

        self.receiving_yds = position_stats.receiving_yds * scoring.RECEIVING_YDS.value
        self.receiving_tds = position_stats.receiving_tds * scoring.RECEIVING_TDS.value

        self.fumbles_lost = position_stats.fumbles_lost * scoring.FUMBLES_LOST.value
    
'''
    This module contains the classes we will use to represent our data
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
import nfldb
import nfldb.types as types
import collections
from enum import Enum


class BasicInfo(object):
    '''
        contains non-statistical information about a player.
    '''
    def __init__(self, name):
        self.name = name

        # connect to database to get info
        db = nfldb.connect()

        q = nfldb.Query(db)
        q.player(full_name=name)

        # this currently gets the first player returned
        #  so we may need to change in future
        info = q.as_players()
        if len(info) > 0:
            info = info[0]
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
        else:
            self.position = types.Enums.player_pos.QB
            self.uniform_number = 1
            self.birthdate = "00/00/0000"
            self.height = 0
            self.weight = 0
            self.college = "RPI"
            self.status = "Nonexistent"
            self.team = "Free"
            self.years_pro = 0

    def get_basic_info(self):
        '''returns the data we got as a dictionary'''
        data = collections.OrderedDict()

        data["Position"] = self.position
        data["Uniform Number"] = self.uniform_number
        data["Birthdate"] = self.birthdate
        data["Height"] = self.height
        data["Weight"] = self.weight
        data["College"] = self.college
        data["Status"] = self.status
        data["Team"] = self.team
        data["Years Pro"] = self.years_pro

        return data


class PositionStats(object):
    '''
        Has default values for each statistic, parent class to each position
    '''
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
        '''returns all statistics as a dictionary'''
        data = collections.OrderedDict()

        data["Passing Attempts"] = self.passing_att
        data["Passing Completions"] = self.passing_cmp
        data["Passing Incompletions"] = self.passing_incmp
        data["Passing Yards"] = self.passing_yds
        data["Passing Touchdowns"] = self.passing_tds
        data["Passing Interceptions"] = self.passing_int
        data["Passing Sacks"] = self.passing_sk

        data["Rushing Yards"] = self.rushing_yds
        data["Rushing Attempts"] = self.rushing_att
        data["Rushing Touchdowns"] = self.rushing_tds

        data["Recieving Targets"] = self.receiving_tar
        data["Recieving Receptions"] = self.receiving_rec
        data["Recieving Yards"] = self.receiving_yds
        data["Recieving Touchdowns"] = self.receiving_tds
        data["Recieving Yards After Catch (YAC)"] = self.receiving_yac_yds

        data["Fumbles Total"] = self.fumbles_tot
        data["Fumbles Lost"] = self.fumbles_lost

        data["Field Goals Attempted"] = self.kicking_fga
        data["Field Goals Missed"] = self.kicking_fgmissed
        data["Field Goal Made Yards"] = self.kicking_fgm_yds
        data["Extra Points Attempted"] = self.kicking_xpa
        data["Extra Points Missed"] = self.kicking_xpmissed
        # may be missing some kicking stats

        return data


class QuarterbackStats(PositionStats):
    '''
    Member variables contain statistics specifically for a Quarterback
    '''
    def __init__(self, name, position, **keyword_params):
        super(QuarterbackStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)

        #case for carrer or yearly stats
        if 'year' in keyword_params:
            q.game(season_year=keyword_params['year'], season_type='Regular')
            if 'week' in keyword_params:
                q.game(week=keyword_params['week'])
        else:
            q.game(season_type='Regular')

        q.player(full_name=name, position=position)


        stats = q.as_aggregate()

        if len(stats) > 0:
            stats = stats[0]
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
    '''
    Member variables contain statistics specifically for a Running Back
    '''
    def __init__(self, name, position, **keyword_params):
        super(RunningbackStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)

        if 'year' in keyword_params:
            q.game(season_year=keyword_params['year'], season_type='Regular')
            if 'week' in keyword_params:
                q.game(week=keyword_params['week'])
        else:
            q.game(season_type='Regular')

        q.player(full_name=name, position=position)

        stats = q.as_aggregate()

        if len(stats) > 0:
            stats = stats[0]

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
    '''
    Member variables contain statistics specifically for a Wide Receiver or Tight End
    '''
    def __init__(self, name, position, **keyword_params):
        super(WideReceiverTightEndStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)

        if 'year' in keyword_params:
            q.game(season_year=keyword_params['year'], season_type='Regular')
            if 'week' in keyword_params:
                q.game(week=keyword_params['week'])
        else:
            q.game(season_type='Regular')

        q.player(full_name=name, position=position)

        stats = q.as_aggregate()

        if len(stats) > 0:
            stats = stats[0]

            self.fumbles_tot = stats.fumbles_tot
            self.fumbles_lost = stats.fumbles_lost

            self.receiving_tar = stats.receiving_tar
            self.receiving_rec = stats.receiving_rec
            self.receiving_yds = stats.receiving_yds
            self.receiving_tds = stats.receiving_tds
            self.receiving_yac_yds = stats.receiving_yac_yds


class KickerStats(PositionStats):
    '''
    Member variables contain statistics specifically for a Kicker
    '''
    def __init__(self, name, position, **keyword_params):
        super(KickerStats, self).__init__()

        db = nfldb.connect()

        q = nfldb.Query(db)

        if 'year' in keyword_params:
            q.game(season_year=keyword_params['year'], season_type='Regular')
            if 'week' in keyword_params:
                q.game(week=keyword_params['week'])
        else:
            q.game(season_type='Regular')

        q.player(full_name=name, position=position)

        stats = q.as_aggregate()

        if len(stats) > 0:
            stats = stats[0]

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
    '''
    Player object holds statistics and returns them in the proper format
    '''
    def __init__(self, name, scoring):
        self.name = name

        self.basic_info = BasicInfo(name)

        self.yearly_stats = collections.OrderedDict()
        position = self.basic_info.position

        # following statements will populate all fields for a player
        if position == types.Enums.player_pos.QB:
            self.position_stats = QuarterbackStats(name, position)
            for year in range(2017, 2008, -1):
                self.yearly_stats[year] = collections.OrderedDict()
                self.yearly_stats[year]['Summary'] = \
                        QuarterbackStats(name, position, year=year).get_stats()

                # for week in range(1, 18):
                #     self.yearly_stats[year][week] = \
                #             QuarterbackStats(name, position, year=year, week=week).get_stats()

        elif position == types.Enums.player_pos.RB:
            self.position_stats = RunningbackStats(name, position)
            for year in range(2017, 2008, -1):
                self.yearly_stats[year] = collections.OrderedDict()
                self.yearly_stats[year]['Summary'] = \
                        RunningbackStats(name, position, year=year).get_stats()

                # for week in range(1, 18):
                #     self.yearly_stats[year][week] = \
                #             RunningbackStats(name, position, year=year, week=week).get_stats()

        elif position == types.Enums.player_pos.WR or position == types.Enums.player_pos.WR:
            self.position_stats = WideReceiverTightEndStats(name, position)
            for year in range(2017, 2008, -1):
                self.yearly_stats[year] = collections.OrderedDict()
                self.yearly_stats[year]['Summary'] = \
                        WideReceiverTightEndStats(name, position, year=year).get_stats()

                # for week in range(1, 18):
                #     self.yearly_stats[year][week] = \
                #             WideReceiverTightEndStats(name, position, year=year, week=week)\
                #             .get_stats()

        elif position == types.Enums.player_pos.K:
            self.position_stats = KickerStats(name, position)
            for year in range(2017, 2008, -1):
                self.yearly_stats[year] = collections.OrderedDict()
                self.yearly_stats[year]['Summary'] = KickerStats(name, position, year=year)\
                    .get_stats()

                # for week in range(1, 18):
                #     self.yearly_stats[year][week] = \
                #             QuarterbackStats(name, position, year=year, week=week).get_stats()

        self.fantasy_stats = fantasy_scores(self.position_stats, scoring)

    def get_player(self):
        '''Returns dictionary containing each type of stats'''
        data = collections.OrderedDict()

        data["BasicInfo"] = self.get_info()
        data["CareerStats"] = self.get_stats()
        data["FantasyStats"] = self.get_fantasy()
        data["YearlyStats"] = self.get_yearly_stats()

        return data

    def get_info(self):
        '''Returns list containing basic info'''
        data = collections.OrderedDict()

        data = self.basic_info.get_basic_info()
        return data

    def get_stats(self):
        '''Returns list containing carrer statistics'''
        data = collections.OrderedDict()

        data = self.position_stats.get_stats()

        return data

    def get_fantasy(self):
        '''Returns list containing fantasy weighted statistics'''
        data = collections.OrderedDict()

        data = self.fantasy_stats.get_stats()
        return data

    def get_yearly_stats(self):
        '''Returns list containing yearly statistics'''
        data = collections.OrderedDict()
        data = self.yearly_stats
        return data


class Espn_Standard_Scoring(Enum):
    '''
    Holds standard fantasy scoring used by ESPN
    '''
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
    '''
        Holds and computes statistics weighted with fantasy scoring
    '''
    def __init__(self, position_stats, scoring_system):
        # default scoring system is ESPN standard
        if scoring_system == None:
            scoring = Espn_Standard_Scoring
        else:
            scoring = scoring_system
        self.passing_yds = position_stats.passing_yds * scoring.PASSING_YDS.value
        self.passing_tds = position_stats.passing_tds * scoring.PASSING_TDS.value
        self.passing_int = position_stats.passing_int * scoring.PASSING_INT.value

        self.rushing_yds = position_stats.rushing_yds * scoring.RUSHING_YDS.value
        self.rushing_tds = position_stats.rushing_tds * scoring.RUSHING_TDS.value

        self.receiving_yds = position_stats.receiving_yds * scoring.RECEIVING_YDS.value
        self.receiving_tds = position_stats.receiving_tds * scoring.RECEIVING_TDS.value

        self.fumbles_lost = position_stats.fumbles_lost * scoring.FUMBLES_LOST.value

    def get_stats(self):
        '''returns dictionary of fantasy statistics'''
        data = collections.OrderedDict()

        data["Passing Yards"] = self.passing_yds
        data["Passing Touchdowns"] = self.passing_tds
        data["Passing Interceptions"] = self.passing_int

        data["Russing Yards"] = self.rushing_yds
        data["Russing Touchdowns"] = self.rushing_tds

        data["Recieving Yards"] = self.receiving_yds
        data["Recieving Touchdowns"] = self.receiving_tds

        data["Fumbles Lost"] = self.fumbles_lost

        return data

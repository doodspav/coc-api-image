try:
    from urllib import quote_plus, urlretrieve #Python 2
except ImportError:
    from urllib.parse import quote_plus #Python 3
    from urllib.request import urlretrieve
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont
import numpy as np
import multiprocessing, requests, random, math, json, sys, os

class Player:
    def __init__(self, api_key):
        #main api stuff
        self.api_dom = 'https://api.clashofclans.com/v1/players/'
        self.headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer '+api_key
        }
        self.status_reasons = {
            200: 'OK',
            400: 'Incorrect request parameters.',
            403: 'Invalid API key.',
            404: 'Player tag does not exist.',
            429: 'Request was throttled, because amount of requests was above the threshold defined for the used API token.',
            500: 'Supercell fucked up somewhere.',
            501: 'Player does not have builder base unlocked.' #custom response, not given by supercell servers
            503: 'Supercell\'s servers are down for maintenance.'
        }
        #main profile names and levels
        self.main_troop_max_levels = [
        #    1  2  3  4  5  6  7  8  9  10  11  12
            [1, 1, 2, 2, 3, 3, 4, 5, 6, 7,  8,  8], #barb
            [1, 1, 2, 2, 3, 3, 4, 5, 6, 7,  8,  8], #arch
            [0, 1, 2, 2, 3, 3, 4, 5, 6, 7,  7,  7], #gob
            [1, 1, 1, 2, 2, 3, 4, 5, 6, 7,  8,  9], #gi
            [0, 0, 1, 2, 2, 3, 4, 5, 5, 6,  7,  8], #wb
            [0, 0, 0, 2, 2, 3, 4, 5, 6, 6,  7,  8], #bal
            [0, 0, 0, 0, 2, 3, 4, 5, 6, 7,  8,  9], #wiz
            [0, 0, 0, 0, 0, 1, 2, 3, 4, 4,  5,  5], #heal
            [0, 0, 0, 0, 0, 0, 2, 3, 4, 5,  6,  7], #drag
            [0, 0, 0, 0, 0, 0, 0, 3, 4, 6,  7,  8], #PEKKA
        #    1  2  3  4  5  6  7  8  9  10  11  12
            [0, 0, 0, 0, 0, 0, 2, 4, 5, 6,  7,  8], #minion
            [0, 0, 0, 0, 0, 0, 2, 4, 5, 6,  7,  8], #hog
            [0, 0, 0, 0, 0, 0, 0, 2, 4, 5,  6,  7], #valk
            [0, 0, 0, 0, 0, 0, 0, 2, 4, 5,  7,  8], #golem
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2,  3,  4], #witch
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 3,  4,  5], #hound
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2,  3,  4], #bowler
        #    1  2  3  4  5  6  7  8  9  10  11  12
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 4,  5,  6], #babydrag
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3,  5,  6], #miner
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  3], #ww
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  3], #bb
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  2,  3]  #edrag
        ]
        self.main_troop_order = ['Barbarian',
                                 'Archer',
                                 'Goblin',
                                 'Giant',
                                 'Wall Breaker',
                                 'Balloon',
                                 'Wizard',
                                 'Healer',
                                 'Dragon',
                                 'P.E.K.K.A',
                                 'Minion',
                                 'Hog Rider',
                                 'Valkyrie',
                                 'Golem',
                                 'Witch',
                                 'Lava Hound',
                                 'Bowler',
                                 'Baby Dragon',
                                 'Miner',
                                 'Wall Wrecker',
                                 'Battle Blimp',
                                 'Electro Dragon']
        self.main_troop_number = len(self.main_troop_order)
        self.main_spell_max_levels = [
        #    1  2  3  4  5  6  7  8  9  10  11  12
            [0, 0, 0, 0, 4, 4, 4, 5, 6, 7,  7,  7], #ls
            [0, 0, 0, 0, 0, 3, 4, 5, 6, 7,  7,  7], #hs
            [0, 0, 0, 0, 0, 0, 4, 5, 5, 5,  5,  5], #rs
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 3,  3,  3], #js
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 5,  6,  7], #fs
            [0, 0, 0, 0, 0, 0, 0, 2, 3, 4,  5,  5], #ps
            [0, 0, 0, 0, 0, 0, 0, 2, 3, 4,  4,  4], #eqs
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 4,  4,  4], #hs
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3,  5,  5], #cs
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 3,  4,  5]  #ss
        ]
        self.main_spell_order = ['Lightning Spell',
                                 'Healing Spell',
                                 'Rage Spell',
                                 'Jump Spell',
                                 'Freeze Spell',
                                 'Poison Spell',
                                 'Earthquake Spell',
                                 'Haste Spell',
                                 'Clone Spell',
                                 'Skeleton Spell']
        self.main_spell_number = len(self.main_spell_order)
        self.main_hero_max_levels = [
        #    1  2  3  4  5  6  7  8   9   10  11  12
            [0, 0, 0, 0, 0, 0, 5, 10, 30, 40, 50, 60], #bk
            [0, 0, 0, 0, 0, 0, 0, 0,  30, 40, 50, 60], #aq
            [0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  20, 30]  #gw
        ]
        self.main_hero_order = ['Barbarian King',
                                'Archer Queen',
                                'Grand Warden']
        self.main_hero_number = len(self.main_hero_order)
        #builder profile names and levels
        self.builder_troop_max_levels = [
        #    1  2  3  4  5   6   7   8
            [1, 4, 6, 8, 10, 12, 14, 16], #rb
            [0, 4, 6, 8, 10, 12, 14, 16], #sa
            [0, 0, 4, 8, 10, 12, 14, 16], #bm
            [0, 0, 4, 8, 10, 12, 14, 16], #bg
            [0, 0, 0, 8, 10, 12, 14, 16], #b
            [0, 0, 0, 0, 0,  0,  0,  16], #sp
            [0, 0, 0, 0, 10, 12, 14, 16], #cc
            [0, 0, 0, 0, 0,  0,  14, 16], #ds
            [0, 0, 0, 8, 10, 12, 14, 16], #bd
            [0, 0, 0, 0, 0,  12, 14, 16]  #nw
        ]
        self.builder_troop_order = ['Raged Barbarian',
                                    'Sneaky Archer',
                                    'Beta Minion',
                                    'Boxer Giant',
                                    'Bomber',
                                    'Super P.E.K.K.A',
                                    'Cannon Cart',
                                    'Drop Ship',
                                    'Baby Dragon',
                                    'Night Witch']
        self.builder_troop_number = len(self.builder_troop_order)
        self.builder_hero_max_levels = [
        #    1  2  3  4  5  6   7   8
            [0, 0, 0, 0, 5, 10, 20, 25] #bm
        ]
        self.builder_hero_order = ['Battle Machine']
        self.builder_hero_number = len(self.builder_hero_order)

    def draw_outline_shadow(self, draw, xy, udlr, text, font, text_colour=(255, 255, 255), shadow_colour=(0, 0, 0)):
        #xy is 2 element tuple == (x, y)
        #udlr is a 4 element tuple == (up, down, left, right)
        x, y = xy
        up, down, left, right = udlr
        #sides
        draw.text((x-left, y), text, shadow_colour, font=font)
        draw.text((x+right, y), text, shadow_colour, font=font)
        draw.text((x, y-up), text, shadow_colour, font=font)
        draw.text((x, y+down), text, shadow_colour, font=font)
        #corners
        draw.text((x-left, y-up), text, shadow_colour, font=font)
        draw.text((x-left, y+down), text, shadow_colour, font=font)
        draw.text((x+right, y-up), text, shadow_colour, font=font)
        draw.text((x+right, y+down), text, shadow_colour, font=font)
        #main text
        draw.text((x, y), text, text_colour, font=font)
        return draw

    def player_info(self, player_tag):
        #preferably sanitise the player_tag before this function
        encoded_tag = quote_plus(player_tag)
        url = self.api_dom + encoded_tag
        r = requests.get(url, headers=self.headers)
        self.player_dict = r.json()
        self.status_code = r.status_code

    def all_main_info(self):
        #global info
        self.level = self.player_dict["expLevel"]
        self.tag = self.player_dict["tag"]
        self.name = self.player_dict["name"]
        self.in_clan = True if "clan" in self.player_dict.keys() else False
        if self.in_clan == True:
            self.clan_name = self.player_dict["clan"]["name"]
            self.clan_tag = self.player_dict["clan"]["tag"]
            self.clan_level = self.player_dict["clan"]["clanLevel"]
            self.clan_badge_URL = self.player_dict["clan"]["badgeUrls"]["small"]
            self.clan_role = self.player_dict["role"]
        #home info
        self.th_level = self.player_dict["townHallLevel"]
        self.main_best_trophies = self.player_dict["bestTrophies"]
        self.main_trophies = self.player_dict["trophies"]
        self.troops_donated = self.player_dict["donations"]
        self.troops_received = self.player_dict["donationsReceived"]
        self.attack_wins = self.player_dict["attackWins"]
        self.defense_wins = self.player_dict["defenseWins"]
        self.war_stars = self.player_dict["warStars"]
        self.in_league = True if "league" in self.player_dict.keys() else False
        if self.in_league == True:
            self.league_name = self.player_dict["league"]["name"]
            self.league_id = self.player_dict["league"]["id"]
        #builder info
        self.has_builder_base = True if "builderHallLevel" in self.player_dict.keys() else False
        if self.has_builder_base == True:
            self.bh_level = self.player_dict["builderHallLevel"]
            self.builder_trophies = self.player_dict["versusTrophies"]
            self.builder_best_trophies = self.player_dict["bestVersusTrophies"]
            self.battle_wins = self.player_dict["versusBattleWins"]
            self.battle_win_count = self.player_dict["versusBattleWinCount"]
        tup = (self.in_clan, self.in_league, self.has_builder_base)
        return tup

    def all_legends_info(self):
        #current season rank doesnt work
        #return info loops from 1-999
        if "legendStatistics" in self.player_dict.keys():
            self.is_legend = True if "bestSeason" in self.player_dict["legendStatistics"].keys() else False
            self.was_legend = True if "previousSeason" in self.player_dict["legendStatistics"].keys() else False
        else:
            self.is_legend = False
            self.was_legend = False
        if self.is_legend == True:
            self.best_season_rank = self.player_dict["legendStatistics"]["bestSeason"]["rank"]
            self.best_season_trophies = self.player_dict["legendStatistics"]["bestSeason"]["trophies"]
            self.best_season_id = self.player_dict["legendStatistics"]["bestSeason"]["id"] #yyyy-mm
            self.legend_trophies = self.player_dict["legendStatistics"]["legendTrophies"]
        if self.was_legend == True:
            self.previous_season_rank = self.player_dict["legendStatistics"]["previousSeason"]["rank"]
            self.previous_season_trophies = self.player_dict["legendStatistics"]["previousSeason"]["trophies"]
            self.previous_season_id = self.player_dict["legendStatistics"]["previousSeason"]["id"] #yyyy-mm
        tup = (self.is_legend, self.was_legend)
        return tup

    def main_troop_list(self):
        levels = [troop["level"] for troop in self.player_dict["troops"] if troop["village"] == "home"]
        names = [troop["name"] for troop in self.player_dict["troops"] if troop["village"] == "home"]
        #add a 0 to levels if troop name is missing
        for i in range(self.main_troop_number):
            try:
                if names[i] != self.main_troop_order[i]:
                    names.insert(i, self.main_troop_order[i])
                    levels.insert(i, 0)
            except IndexError:
                levels.insert(i, 0)
        #make level a string if it's supermax, or float if it's max for the townhall
        for i in range(len(levels)):
            if levels[i] == self.main_troop_max_levels[i][-1]:
                levels[i] = str(levels[i])
            elif levels[i] == self.main_troop_max_levels[i][self.th_level-1]:
                levels[i] = float(levels[i])
        self.main_troop_levels = levels
        #list elements are int if nonmax, float if max, or string if supermax
        return self.main_troop_levels

    def builder_troop_list(self):
        levels = [troop["level"] for troop in self.player_dict["troops"] if troop["village"] == "builderBase"]
        names = [troop["name"] for troop in self.player_dict["troops"] if troop["village"] == "builderBase"]
        #add a 0 to levels if troop name is missing
        for i in range(self.builder_troop_number):
            try:
                if names[i] != self.builder_troop_order[i]:
                    names.insert(i, self.builder_troop_order[i])
                    levels.insert(i, 0)
            except IndexError:
                levels.insert(i, 0)
        #make level a string if it's supermax, or float if it's max for the builderhall
        for i in range(len(levels)):
            if levels[i] == self.builder_troop_max_levels[i][-1]:
                levels[i] = str(levels[i])
            elif levels[i] == self.builder_troop_max_levels[i][self.bh_level-1]:
                levels[i] = float(levels[i])
        self.builder_troop_levels = levels
        #list elements are int if nonmax, float if max, or string if supermax
        return self.builder_troop_levels

    def main_spell_list(self):
        if "spells" in self.player_dict.keys():
            levels = [spell["level"] for spell in self.player_dict["spells"] if spell["village"] == "home"]
            names = [spell["name"] for spell in self.player_dict["spells"] if spell["village"] == "home"]
            #add a 0 to levels if spell name is missing
            for i in range(self.main_spell_number):
                try:
                    if names[i] != self.main_spell_order[i]:
                        names.insert(i, self.main_spell_order[i])
                        levels.insert(i, 0)
                except IndexError:
                    levels.insert(i, 0)
            #make level a string if it's supermax, or float if it's max for the townhall
            for i in range(len(levels)):
                if levels[i] == self.main_spell_max_levels[i][-1]:
                    levels[i] = str(levels[i])
                elif levels[i] == self.main_spell_max_levels[i][self.th_level-1]:
                    levels[i] = float(levels[i])
            self.main_spell_levels = levels
        else:
            self.main_spell_levels = [0]*self.main_spell_number
        #list elements are int if nonmax, float if max, or string if supermax
        return self.main_spell_levels

    def main_hero_list(self):
        if "heroes" in self.player_dict.keys():
            levels = [hero["level"] for hero in self.player_dict["heroes"] if hero["village"] == "home"]
            names = [hero["name"] for hero in self.player_dict["heroes"] if hero["village"] == "home"]
            #add a 0 to levels if hero name is missing
            for i in range(self.main_hero_number):
                try:
                    if names[i] != self.main_hero_order[i]:
                        names.insert(i, self.main_hero_order[i])
                        levels.insert(i, 0)
                except IndexError:
                    levels.insert(i, 0)
            #make level a string if it's supermax, or float if it's max for the townhall
            for i in range(len(levels)):
                if levels[i] == self.main_hero_max_levels[i][-1]:
                    levels[i] = str(levels[i])
                elif levels[i] == self.main_hero_max_levels[i][self.th_level-1]:
                    levels[i] = float(levels[i])
            self.main_hero_levels = levels
        else:
            self.main_hero_levels = [0]*self.main_hero_number
        #list elements are int if nonmax, float if max, or string if supermax
        return self.main_hero_levels

    def builder_hero_list(self):
        if "heroes" in self.player_dict.keys():
            levels = [hero["level"] for hero in self.player_dict["heroes"] if hero["village"] == "builderBase"]
            names = [hero["name"] for hero in self.player_dict["heroes"] if hero["village"] == "builderBase"]
            #add a 0 to levels if hero name is missing
            for i in range(self.builder_hero_number):
                try:
                    if names[i] != self.builder_hero_order[i]:
                        names.insert(i, self.builder_hero_order[i])
                        levels.insert(i, 0)
                except IndexError:
                    levels.insert(i, 0)
            #make level a string if it's supermax, or float if it's max for the builderhall
            for i in range(len(levels)):
                if levels[i] == self.builder_hero_max_levels[i][-1]:
                    levels[i] = str(levels[i])
                elif levels[i] == self.builder_hero_max_levels[i][self.bh_level-1]:
                    levels[i] = float(levels[i])
            self.builder_hero_levels = levels
        else:
            self.builder_hero_levels = [0]*self.builder_hero_number
        #list elements are int if nonmax, float if max, or string if supermax
        return self.builder_hero_levels

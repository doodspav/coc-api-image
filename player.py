#name: player (other one is clan)
try:
    from urllib import quote_plus, urlretrieve #Python 2
except ImportError:
    from urllib.parse import quote_plus #Python 3
    from urllib.request import urlretrieve
import requests
from PIL import Image, ImageFont, ImageDraw
import math
import json
import numpy as np


class player:
    def __init__(self, api_key):
        #main api stuff
        self.api_dom = "https://api.clashofclans.com/v1/players/"
        self.headers = {
            "Accept":"application/json",
            "authorization":"Bearer "+api_key
            }
        self.status_reasons = {200:"OK",
                            400:"Incorrect request parameters.",
                            403:"Invalid API key.",
                            404:"Player hashtag does not exist.",
                            429:"Request was throttled, because amount of requests was above the threshold defined for the used API token.",
                            500:"Supercell fucked up somewhere.",
                            503:"Supercell's servers are down for maintenance."}
        #main profile stuff
        self.main_troop_max_levels = [7,7,7,8,7,7,8,5,6,6,7,7,6,7,3,4,3,5,5]
        self.main_troop_order = ["Barbarian",
                                "Archer",
                                "Goblin",
                                "Giant",
                                "Wall Breaker",
                                "Balloon",
                                "Wizard",
                                "Healer",
                                "Dragon",
                                "P.E.K.K.A",
                                "Minion",
                                "Hog Rider",
                                "Valkyrie",
                                "Golem",
                                "Witch",
                                "Lava Hound",
                                "Bowler",
                                "Baby Dragon",
                                "Miner"]
        self.main_troop_number = len(self.main_troop_order)
        self.main_spell_max_levels = [7,7,5,3,6,5,4,4,5,4]
        self.main_spell_order = ["Lightning Spell",
                                "Healing Spell",
                                "Rage Spell",
                                "Jump Spell",
                                "Freeze Spell",
                                "Poison Spell",
                                "Earthquake Spell",
                                "Haste Spell",
                                "Clone Spell",
                                "Skeleton Spell"]
        self.main_spell_number = len(self.main_spell_order)
        self.main_hero_max_levels = [50,50,20]
        self.main_hero_order = ["Barbarian King",
                                "Archer Queen",
                                "Grand Warden"]
        self.main_hero_number = len(self.main_hero_order)
        #builder profile stuff
        self.builder_troop_max_levels = [14,14,14,14,14,14,14,14,14,14]
        self.builder_troop_order = ["Raged Barbarian",
                                    "Sneaky Archer",
                                    "Beta Minion",
                                    "Boxer Giant",
                                    "Bomber",
                                    "Super P.E.K.K.A",
                                    "Cannon Cart",
                                    "Drop Ship",
                                    "Baby Dragon",
                                    "Night Witch"]
        self.builder_troop_number = len(self.builder_troop_order)
        self.builder_hero_max_levels = [20]
        self.builder_hero_order = ["Battle Machine"]
        self.builder_hero_number = len(self.builder_hero_order)

    def player_info(self, player_tag):
        #preferably sanitise the player_tag before this function
        encoded_tag = quote_plus(player_tag)
        url = self.api_dom + encoded_tag
        r = requests.get(url, headers=self.headers)
        self.player_dict = r.json()
        self.status_code = r.status_code
        return self.player_dict

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
        #make level a string if it's max
        for i in range(len(levels)):
            if levels[i] == self.main_troop_max_levels[i]:
                levels[i] = str(levels[i])
        self.main_troop_levels = levels
        #list elements are int if nonmax or string if max
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
        #make level a string if it's max
        for i in range(len(levels)):
            if levels[i] == self.builder_troop_max_levels[i]:
                levels[i] = str(levels[i])
        self.builder_troop_levels = levels
        #list elements are int if nonmax or string if max
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
            #make level a string if it's max
            for i in range(len(levels)):
                if levels[i] == self.main_spell_max_levels[i]:
                    levels[i] = str(levels[i])
            self.main_spell_levels = levels
        else:
            self.main_spell_levels = [0]*self.main_spell_number
        #list elements are int if nonmax or string if max
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
            #make level a string if it's max
            for i in range(len(levels)):
                if levels[i] == self.main_hero_max_levels[i]:
                    levels[i] = str(levels[i])
            self.main_hero_levels = levels
        else:
            self.main_hero_levels = [0]*self.main_hero_number
        #list elements are int if nonmax or string if max
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
            #make level a string if it's max
            for i in range(len(levels)):
                if levels[i] == self.builder_hero_max_levels[i]:
                    levels[i] = str(levels[i])
            self.builder_hero_levels = levels
        else:
            self.builder_hero_levels = [0]*self.builder_hero_number
        #list elements are int if nonmax or string if max
        return self.builder_hero_levels

    def main_info(self):
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
        #player rank doesnt work - loops from 1-999, doesnt show your actual rank above 999
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

    def legends_info(self):
        if "legendStatistics" in self.player_dict.keys():
            self.is_legend = True if "bestSeason" in self.player_dict["legendStatistics"].keys() else False
            self.was_legend = True if "previousSeason" in self.player_dict["legendStatistics"].keys() else False
        else:
            self.is_legend = False
        if self.is_legend == True:
            self.best_season_rank = self.player_dict["legendStatistics"]["bestSeason"]["rank"]
            self.best_season_trophies = self.player_dict["legendStatistics"]["bestSeason"]["trophies"]
            self.best_season_id = self.player_dict["legendStatistics"]["bestSeason"]["id"] #20xx-xx (year,month)
            self.legend_trophies = self.player_dict["legendStatistics"]["legendTrophies"]
        if self.was_legend == True:
            self.previous_season_rank = self.player_dict["legendStatistics"]["previousSeason"]["rank"]
            self.previous_season_trophies = self.player_dict["legendStatistics"]["previousSeason"]["trophies"]
            self.previous_season_id = self.player_dict["legendStatistics"]["previousSeason"]["id"] #20xx-xx (year,month)
        tup = (self.is_legend, self.was_legend)
        return tup

#change clan badges not to have I,II,III in the badge image
#have a nicer legends badge
#change name and clan name to not show blanks
    def main_picture_info(self):
        #global stuff
        self.main_blank = Image.open("cocapifiles/blank_profile.png")
        draw = ImageDraw.Draw(self.main_blank)
        white = 255,255,255
        black = 0,0,0
        leagues = ["u","b3","b2","b1","s3","s2","s1","g3","g2","g1","c3","c2","c1","m3","m2","m1","ch3","ch2","ch1","t3","t2","t1","l"]
        league_cups = [399,499,599,799,999,1199,1399,1599,1799,1999,2199,2399,2599,2799,2999,3199,3499,3799,4099,4399,4699,4999,10000000]
        league_id_to_text = {29000001:"Bronze League III",
                            29000002:"Bronze League II",
                            29000003:"Bronze_League_I",
                            29000004:"Silver League III",
                            29000005:"Silver League II",
                            29000006:"Silver League I",
                            29000007:"Gold League III",
                            29000008:"Gold League II",
                            29000009:"Gold League I",
                            29000010:"Crystal League III", 
                            29000011:"Crystal League II", 
                            29000012:"Crystal League I", 
                            29000013:"Master League III", 
                            29000014:"Master League II", 
                            29000015:"Master League I", 
                            29000016:"Champion League III", 
                            29000017:"Champion League II",
                            29000018:"Champion League I", 
                            29000019:"Titan League III", 
                            29000020:"Titan League II", 
                            29000021:"Titan League I", 
                            29000022:"Legend League"}

        #bottom number stuff (bn)
        bn_font = ImageFont.truetype("cocapifiles/fonts/CCBackBeat-Light_5.ttf", 30)
        bn_x = [418,847,1260,1748] #x coordinate of rightmost pixel of each of the 4 numbers
        bn_y = 402 #y coordinate of the topmost pixel (all 4 have the same)
        numbers = [self.troops_donated, self.troops_received, self.attack_wins, self.defense_wins]
        for i in range(4):
            width, height = bn_font.getsize(str(numbers[i]))
            x = bn_x[i] - width
            draw.text((x,bn_y), str(numbers[i]), white, font=bn_font)

        #war stars
        ws_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        ws_x, ws_y = 1127,315 #top left pixel of the war stars number
        draw.text((ws_x+2,ws_y), str(self.war_stars), black, font=ws_font)
        draw.text((ws_x-2,ws_y), str(self.war_stars), black, font=ws_font)
        draw.text((ws_x,ws_y-2), str(self.war_stars), black, font=ws_font)
        draw.text((ws_x,ws_y+6), str(self.war_stars), black, font=ws_font)
        draw.text((ws_x,ws_y), str(self.war_stars), white, font=ws_font)

        #all time best trophies
        if self.main_best_trophies > 0:
            atb_img = Image.open("cocapifiles/all_time_best_blank.png")
            self.main_blank.paste(atb_img, box=(1373,242))
            #putting the badge
            i = 0
            while i < len(league_cups):
                if self.main_best_trophies > league_cups[i]:
                    i += 1
                else:
                    break
            if leagues[i] != "u": #unranked
                atb_badge = Image.open("cocapifiles/atbbadges/" + leagues[i] + ".png")
                self.main_blank.paste(atb_badge, box=(1390,285))
            #putting trophies number
            atb_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
            atb_x, atb_y = 1565,314
            draw.text((atb_x-2,atb_y), str(self.main_best_trophies), black, font=atb_font)
            draw.text((atb_x+2,atb_y), str(self.main_best_trophies), black, font=atb_font)
            draw.text((atb_x,atb_y-2), str(self.main_best_trophies), black, font=atb_font)
            draw.text((atb_x,atb_y+6), str(self.main_best_trophies), black, font=atb_font)
            draw.text((atb_x,atb_y), str(self.main_best_trophies), white, font=atb_font)

        #league text
        if self.in_league == True:
            league_text = league_id_to_text[self.league_id]
        else:
            league_text = "Unranked"
        lt_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 29)
        lt_x, lt_y = 1263,74
        draw.text((lt_x-2,lt_y), league_text, black, font=lt_font)
        draw.text((lt_x+2,lt_y), league_text, black, font=lt_font)
        draw.text((lt_x,lt_y-2), league_text, black, font=lt_font)
        draw.text((lt_x,lt_y+5), league_text, black, font=lt_font)
        draw.text((lt_x,lt_y), league_text, white, font=lt_font)

        #current cups
        cc_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 50)
        cc_x, cc_y = 1340,139
        draw.text((cc_x+2,cc_y), str(self.main_trophies), black, font=cc_font)
        draw.text((cc_x-2,cc_y), str(self.main_trophies), black, font=cc_font)
        draw.text((cc_x,cc_y-2), str(self.main_trophies), black, font=cc_font)
        draw.text((cc_x,cc_y+7), str(self.main_trophies), black, font=cc_font)
        draw.text((cc_x,cc_y), str(self.main_trophies), white, font=cc_font)

        #current badge
        if self.in_league == True:
            badge_start_x = {29000001:"1043", 29000002:"1043", 29000003:"1043", 29000004:"1043", 29000005:"1043", 29000006:"1043", 29000007:"1042", 29000008:"1042", 29000009:"1042", 29000010:"1013", 29000011:"1013", 29000012:"1013", 29000013:"1025", 29000014:"1025", 29000015:"1025", 29000016:"1019", 29000017:"1019", 29000018:"1019", 29000019:"1026", 29000020:"1026", 29000021:"1026", 29000022:"1036"}
            badge_start_y = {29000001:"40", 29000002:"40", 29000003:"40", 29000004:"56", 29000005:"56", 29000006:"56", 29000007:"14", 29000008:"14", 29000009:"14", 29000010:"49", 29000011:"49", 29000012:"49", 29000013:"11", 29000014:"11", 29000015:"11", 29000016:"33", 29000017:"33", 29000018:"33", 29000019:"35", 29000020:"35", 29000021:"35", 29000022:"48"}
            bt_x, bt_y = int(badge_start_x[self.league_id]),int(badge_start_y[self.league_id])
            badge_name = league_id_to_text[self.league_id].replace(" ","_")
            badge_img = Image.open("cocapifiles/mainbadges/" + badge_name + ".png")
            self.main_blank.paste(badge_img, box=(bt_x,bt_y))

        #xp level
        xp_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 33)
        xp_middle_pixel = 71 #x value (y value doesnt matter)
        xp_y = 50 #top of number
        width, height = xp_font.getsize(str(self.level))
        xp_x = xp_middle_pixel - math.floor(width/2)
        draw.text((xp_x+1,xp_y), str(self.level), black, font=xp_font)
        draw.text((xp_x-1,xp_y), str(self.level), black, font=xp_font)
        draw.text((xp_x,xp_y-1), str(self.level), black, font=xp_font)
        draw.text((xp_x,xp_y+5), str(self.level), black, font=xp_font)
        draw.text((xp_x,xp_y), str(self.level), white, font=xp_font)

        #name (still has issue of non standard characters appearing as blank)
        n_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        n_x, n_y = 127,29
        draw.text((n_x+2,n_y), self.name, black, font=n_font)
        draw.text((n_x-2,n_y), self.name, black, font=n_font)
        draw.text((n_x,n_y-2), self.name, black, font=n_font)
        draw.text((n_x,n_y+6), self.name, black, font=n_font)
        draw.text((n_x,n_y), self.name, white, font=n_font)

        #tag
        grey = 80,85,114
        t_font = ImageFont.truetype("cocapifiles/fonts/CCBackBeat-Light_5.ttf", 32)
        t_x, t_y = 128,81
        draw.text((t_x,t_y), self.tag, grey, font=t_font)

        #clan stuff
        if self.in_clan == True:
            #clan name
            cn_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 26)
            cn_x, cn_y = 124,126
            draw.text((cn_x+2,cn_y), self.clan_name, black, font=cn_font)
            draw.text((cn_x-2,cn_y), self.clan_name, black, font=cn_font)
            draw.text((cn_x,cn_y-2), self.clan_name, black, font=cn_font)
            draw.text((cn_x,cn_y+4), self.clan_name, black, font=cn_font)
            draw.text((cn_x,cn_y), self.clan_name, white, font=cn_font)
            #clan role
            role_dict = {"admin":"Elder", "member":"Member", "coLeader":"Co-leader", "leader":"Leader"}
            role_img = Image.open("cocapifiles/role/"+role_dict[self.clan_role]+".png")
            self.main_blank.paste(role_img, box=(118,161))
            #clan badge
            urlretrieve(self.clan_badge_URL, "cocapifiles/temp_clan_badge.png")
            backround = Image.open("cocapifiles/clan_badge_backround.png")
            badge = Image.open("cocapifiles/temp_clan_badge.png")
            badge_array = np.array(badge)
            backround_array = np.array(backround)
            w1,h1 = badge.size
            w2,h2 = backround.size
            if (w1 != w2) or (h1 != h2):
                raise ValueError("Images do not have the same dimensions.")
            x,y = 0,0
            while (x<h1) and (y<w1):
                if badge_array[x,y,3] == 255: #255 means it's fully opaque
                    backround_array[x,y] = badge_array[x,y]
                x += 1
                if x == h1:
                    x = 0
                    y += 1
            composite_small = Image.fromarray(backround_array, "RGBA")
            size = 84,84
            composite = composite_small.resize(size, Image.ANTIALIAS)
            self.main_blank.paste(composite, box=(29,122))

        return self.main_blank

#make legends badges nicer
    def main_picture_legends(self):
        #global stuff
        self.legends_blank = Image.open("cocapifiles/blank_legends.png")
        draw = ImageDraw.Draw(self.legends_blank)
        white = 255,255,255
        black = 0,0,0

        #all text
        legend_texts = []
        months = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"Septmeber", "10":"October", "11":"November", "12":"December"}
        best_year = str(self.best_season_id)[0:4]
        best_month = months[str(self.best_season_id)[5:]]
        legend_texts.append("Best: %s %s Season" % (best_month,best_year))
        if self.was_legend == True:
            previous_year = str(self.previous_season_id)[0:4]
            previous_month = months[str(self.previous_season_id)[5:]]
            legend_texts.append("Previous: %s %s Season" % (previous_month,previous_year))
        else:
            legend_texts.append("Previous Season:")
        legend_texts.append("Legend Trophies")
        lt_x = [169,763,1436] #left most x pixel
        lt_y = 62 #top most y pixel
        lt_font = ImageFont.truetype("cocapifiles/fonts/CCBackBeat-Light_5.ttf", 28)
        for i in range(len(legend_texts)):
            draw.text((lt_x[i]+2,lt_y), legend_texts[i], black, font=lt_font)
            draw.text((lt_x[i]-2,lt_y), legend_texts[i], black, font=lt_font)
            draw.text((lt_x[i],lt_y-2), legend_texts[i], black, font=lt_font)
            draw.text((lt_x[i],lt_y+3), legend_texts[i], black, font=lt_font)
            draw.text((lt_x[i],lt_y+5), legend_texts[i], black, font=lt_font)
            draw.text((lt_x[i],lt_y), legend_texts[i], white, font=lt_font)

        #previous season
        if self.was_legend == True:
            digits_to_font_size = {1:35,2:26,3:22,4:18,5:18,6:18}
            digits = len(str(self.previous_season_rank))
            #previous season rank
            if digits < 7:
                font_size = digits_to_font_size[digits]
                psr_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", font_size)
                width, height = psr_font.getsize(str(self.previous_season_rank))
                psr_x = 810 - math.floor(width/2)
                ps_y = 130 - math.floor(height/2)
                draw.text((psr_x+2,psr_y), str(self.previous_season_rank), black, font=psr_font)
                draw.text((psr_x-2,psr_y), str(self.previous_season_rank), black, font=psr_font)
                draw.text((psr_x,psr_y-2), str(self.previous_season_rank), black, font=psr_font)
                draw.text((psr_x,psr_y+4), str(self.previous_season_rank), black, font=psr_font)
                draw.text((psr_x,psr_y), str(self.previous_season_rank), white, font=psr_font)
            #previous season trophies
            pst_x, pst_y = 935,135
            pst_font = nf4 = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 32)
            draw.text((pst_x+2,pst_y), str(self.previous_season_trophies), black, font=pst_font)
            draw.text((pst_x-2,pst_y), str(self.previous_season_trophies), black, font=pst_font)
            draw.text((pst_x,pst_y-2), str(self.previous_season_trophies), black, font=pst_font)
            draw.text((pst_x,pst_y+5), str(self.previous_season_trophies), black, font=pst_font)
            draw.text((pst_x,pst_y), str(self.previous_season_trophies), white, font=pst_font)
        else:
            dnp_img = Image.open("cocapifiles/didNotPlace.png")
            self.legends_blank.paste(dnp_img, (750,93))

        #legend trophies
        lt_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 35)
        lt_x, lt_y = 1576,124
        draw.text((lt_x+2,lt_y), str(self.legend_trophies), black, font=lt_font)
        draw.text((lt_x-2,lt_y), str(self.legend_trophies), black, font=lt_font)
        draw.text((lt_x,lt_y-2), str(self.legend_trophies), black, font=lt_font)
        draw.text((lt_x,lt_y+6), str(self.legend_trophies), black, font=lt_font)
        draw.text((lt_x,lt_y), str(self.legend_trophies), white, font=lt_font)

        #best season trophies
        bst_x, bst_y = 277,130
        bst_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        draw.text((bst_x+2,bst_y), str(self.best_season_trophies), black, font=bst_font)
        draw.text((bst_x-2,bst_y), str(self.best_season_trophies), black, font=bst_font)
        draw.text((bst_x,bst_y-2), str(self.best_season_trophies), black, font=bst_font)
        draw.text((bst_x,bst_y+6), str(self.best_season_trophies), black, font=bst_font)
        draw.text((bst_x,bst_y), str(self.best_season_trophies), white, font=bst_font)

        #best season rank
        digits_to_font_size = {1:50,2:40,3:34,4:25,5:24,6:24}
        digits = len(str(self.best_season_rank))
        if digits < 7:
            font_size = digits_to_font_size[digits]
            bsr_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", font_size)
            width, height = bsr_font.getsize(str(self.best_season_rank))
            bsr_x = 91 - math.floor(width/2)
            bsr_y = 102 - math.floor(height/2)
            draw.text((bsr_x+2,bsr_y), str(self.best_season_rank), black, font=bsr_font)
            draw.text((bsr_x-2,bsr_y), str(self.best_season_rank), black, font=bsr_font)
            draw.text((bsr_x,bsr_y-2), str(self.best_season_rank), black, font=bsr_font)
            draw.text((bsr_x,bsr_y+5), str(self.best_season_rank), black, font=bsr_font)
            draw.text((bsr_x,bsr_y), str(self.best_season_rank), white, font=bsr_font)

        return self.legends_blank
#new files that are required:
#nonmax_level.png, max_level.png
#nonmax_hero_level.png (max_hero_level is the same siza as max_level)
#find out what level_font is (size and font)
    def main_picture_troops(self, troop_levels=None, spell_levels=None, hero_levels=None):
        #global stuff
        self.troops_blank = Image.open("cocapifiles/blank_troops.png")
        icon_xy = {"Barbarian":(219,82),"Archer":(301,82),"Goblin":(463,82),"Giant":(382,82),"Wall_Breaker":(545,82),"Balloon":(627,82),"Wizard":(708,82),"Healer":(790,82),"Dragon":(872,82),"P.E.K.K.A":(953,82),"Minion":(382,162),"Hog_Rider":(463,162),"Valkyrie":(545,162),"Golem":(627,162),"Witch":(708,162),"Lava_Hound":(790,162),"Bowler":(872,162),"Baby_Dragon":(219,162),"Miner":(301,162),
                    "Lightning_Spell":(1056,83),"Healing_Spell":(1137,83),"Rage_Spell":(1219,83),"Jump_Spell":(1301,83),"Freeze_Spell":(1381,83),"Poison_Spell":(1137,163),"Earthquake_Spell":(1219,163),"Haste_Spell":(1301,163),"Clone_Spell":(1056,163),"Skeleton_Spell":(1381,163),
                    "Barbarian_King":(1481,83),"Archer_Queen":(1561,83),"Grand_Warden":(1643,83)}
        icon_path = "cocapifiles/Icons/"
        level_font = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 11)
        white = 255,255,255
        black = 0,0,0

        #town hall image
        th_img = Image.open("cocapifiles/townHall/"+str(self.th_level)+".png")
        self.troops_blank.paste(th_img, box=(0,20))

        #troop levels
        if troop_levels == None:
            troop_levels = self.main_troop_levels
        for i in range(self.main_troop_number):
            if troop_levels[i] != 0:
                icon_name = self.main_troop_order[i].replace(" ","_")
                troop_img = Image.open(icon_path+icon_name+".png")
                if troop_levels[i] != 1:
                    if type(troop_levels[i]) == int:
                        #not max
                        level_img = Image.open(icon_path+"nonmax_level.png")
                    else:
                        #max
                        level_img = Image.open(icon_path+"max_level.png")
                    width, height = level_img.size
                    w, h = math.floor(width/2), math.floor(height/2)#middle point
                    x, y = level_font.getsize(str(troop_levels[i]))
                    x, y = (w-x),(h-y) #top left of the number
                    draw = ImageDraw.Draw(level_img)
                    draw.text((x+1,y), str(troop_levels[i]), black, font=level_font)
                    draw.text((x-1,y), str(troop_levels[i]), black, font=level_font)
                    draw.text((x,y-1), str(troop_levels[i]), black, font=level_font)
                    draw.text((x,y+3), str(troop_levels[i]), black, font=level_font)
                    draw.text((x,y), str(troop_levels[i]), white, font=level_font)
                    troopimg2 = troop_img.crop(box=(5,44,(5+width),(44+height)))
                    troopimg3 = Image.alpha_composite(troopimg2, level_img)
                    troop_img.paste(troopimg3, box=(5,44))
                self.troops_blank.paste(troop_img, box=icon_xy[icon_name])

        #spell levels
        if spell_levels == None:
            spell_levels = self.main_spell_levels
        for i in range(self.main_spell_number):
            if spell_levels[i] != 0:
                icon_name = self.main_spell_order[i].replace(" ","_")
                spell_img = Image.open(icon_path+icon_name+".png")
                if spell_levels[i] != 1:
                    if type(spell_levels[i]) == int:
                        #not max
                        level_img = Image.open(icon_path+"nonmax_level.png")
                    else:
                        #max
                        level_img = Image.open(icon_path+"max_level.png")
                    width, height = level_img.size
                    w, h = math.floor(width/2), math.floor(height/2)
                    x, y = level_font.getsize(str(troop_levels[i]))
                    x, y = (w-x),(h-y) #top left of the number
                    draw = ImageDraw.Draw(level_img)
                    draw.text((x+1,y), str(spell_levels[i]), black, font=level_font)
                    draw.text((x-1,y), str(spell_levels[i]), black, font=level_font)
                    draw.text((x,y-1), str(spell_levels[i]), black, font=level_font)
                    draw.text((x,y+3), str(spell_levels[i]), black, font=level_font)
                    draw.text((x,y), str(spell_levels[i]), white, font=level_font)
                    spellimg2 = spell_img.crop(box=(5,44,(5+width),(44+height)))
                    spellimg3 = Image.alpha_composite(spellimg2, level_img)
                    spell_img.paste(spellimg3, box=(5,44))
                self.troops_blank.paste(spell_img, box=icon_xy[icon_name])

        #hero levels
        if hero_levels == None:
            hero_levels = self.main_hero_levels
        for i in range(self.main_hero_number):
            if hero_levels[i] != 0:
                icon_name = self.main_hero_order[i].replace(" ","_")
                hero_img = Image.open(icon_path+icon_name+".png")
                if type(hero_levels[i]) == int:
                    #not max
                    level_img = Image.open(icon_path+"nonmax_hero_level.png")
                else:
                    #max
                    level_img = Image.open(icon_path+"max_level.png")
                width, height = level_img.size
                w, h = math.floor(width/2), math.floor(height/2)
                x, y = level_font.getsize(str(troop_levels[i]))
                x, y = (w-x),(h-y) #top left of the number
                draw = ImageDraw.Draw(level_img)
                draw.text((x+1,y), str(hero_levels[i]), black, font=level_font)
                draw.text((x-1,y), str(hero_levels[i]), black, font=level_font)
                draw.text((x,y-1), str(hero_levels[i]), black, font=level_font)
                draw.text((x,y+3), str(hero_levels[i]), black, font=level_font)
                draw.text((x,y), str(hero_levels[i]), white, font=level_font)
                heroimg2 = hero_img.crop(box=(5,44,(5+width),(44+height)))
                heroimg3 = Image.alpha_composite(heroimg2, level_img)
                hero_img.paste(heroimg3, box=(5,44))
                self.troops_blank.paste(hero_img, box=icon_xy[icon_name])
        return self.troops_blank

    def builder_picture_all(self):
        print(hi)

    def main_full_profile(self, player_tag, path="", name="test", ext=".jpg"):
        ext_to_type = {".jpg":"JPEG",".png":"PNG"}
        info = self.player_info(player_tag)
        if self.status_code == 200:
            troops = self.main_troop_list()
            spells = self.main_spell_list()
            heroes = self.main_hero_list()
            main = self.main_info()
            legends = self.legends_info()
            mpi = self.main_picture_info()
            w_mpi, h_mpi = mpi.size
            mpt = self.main_picture_troops()
            w_mpt, h_mpt = mpt.size
            if self.is_legend == True:
                mpl = self.main_picture_legends()
                w_mpl, h_mpl = mpl.size
            else:
                w_mpl, h_mpl = 0,0
            x = w_mpi
            y = h_mpi + h_mpl + h_mpt
            profile_img = Image.new("RGB", (x,y), color=0)
            profile_img.paste(mpi)
            if self.is_legend == True:
                profile_img.paste(mpl, box=(0,h_mpi))
            profile_img.paste(mpt, box=(0,h_mpi+h_mpl))
            profile_img.save(path+name+ext,ext_to_type[ext])
        return self.status_code
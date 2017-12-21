import requests
import json
import urllib
from PIL import Image, ImageFont, ImageDraw
import math
import numpy as np

class cocapi:
    def __init__(self):
        api_key = "Your API key goes here." #PUT YOUR API KEY HERE
        self.api_dom = "https://api.clashofclans.com/v1"
        self.players = "/players/"
        self.headers = {
    	    "Accept":"application/json",
    	    "authorization":"Bearer "+api_key
    	    }
        self.statusReasons = {200:"OK",400:"Incorrect request parameters.",403:"Invalid API key.",404:"Player hashtag does not exist.",429:"Request was throttled, because amount of requests was above the threshold defined for the used API token.",500:"Supercell fucked up somewhere.",503:"Supercell's servers are down for maintenance."}
        self.maxTroopLevels = [7,7,7,8,7,7,8,5,6,6,7,7,6,7,3,4,3,5,5]
        self.Ntroops = 19
        self.troopOrder = ["Barbarian","Archer","Goblin","Giant","Wall Breaker","Balloon","Wizard","Healer","Dragon","P.E.K.K.A","Minion","Hog Rider","Valkyrie","Golem","Witch","Lava Hound","Bowler","Baby Dragon","Miner"]
        self.maxSpellLevels = [7,7,5,3,6,5,4,4,5,4]
        self.Nspells = 10
        self.spellOrder = ["Lightning Spell","Healing Spell","Rage Spell","Jump Spell","Freeze Spell","Poison Spell","Earthquake Spell","Haste Spell","Clone Spell","Skeleton Spell"]
        self.maxHeroLevels = [50,50,20]
        self.Nheroes = 3
        self.heroOrder = ["Barbarian King","Archer Queen","Grand Warden"]

    def player_info(self, player_tag):
        self.encoded_tag = urllib.quote_plus(player_tag)
        url = self.api_dom+self.players+self.encoded_tag
        r = requests.get(url, headers=self.headers)
        self.player_dict = r.json()
        self.statusCode = r.status_code
        return self.player_dict

    def troop_list(self, player_dict):
        i = 0
        self.troopLevels = []
        self.troopNames = []
        length_troops = len(self.player_dict["troops"])
        while i < length_troops:
            self.troopLevels.append(self.player_dict["troops"][i]["level"])
            self.troopNames.append(str(self.player_dict["troops"][i]["name"]))
            i = i+1
        i = 0
        while i < self.Ntroops:
            try:
                if self.troopNames[i] != self.troopOrder[i]:
                    self.troopNames.insert(i, self.troopOrder[i])
                    self.troopLevels.insert(i, 0)
            except IndexError:
                self.troopLevels.insert(i, 0)
            else:
                pass
            i = i+1
        i = 0
        self.finalTroopLevels = []
        while i <self.Ntroops:
            if self.troopLevels[i] == self.maxTroopLevels[i]:
                self.finalTroopLevels.append(str(self.troopLevels[i]) + "max")
            else:
                self.finalTroopLevels.append(self.troopLevels[i])
            i = i+1
        return self.finalTroopLevels

    def spell_list(self, player_dict):
        if "spells" in self.player_dict.keys():
            i = 0
            self.spellLevels = []
            self.spellNames = []
            length_spells = len(self.player_dict["spells"])
            while i < length_spells:
                self.spellLevels.append(self.player_dict["spells"][i]["level"])
                self.spellNames.append(str(self.player_dict["spells"][i]["name"]))
                i = i+1
            i = 0
            while i < self.Nspells:
                try:
                    if self.spellNames[i] != self.spellOrder[i]:
                        self.spellNames.insert(i, self.spellOrder[i])
                        self.spellLevels.insert(i, 0)
                except IndexError:
                    self.spellLevels.insert(i, 0)
                else:
                    pass
                i = i+1
            i = 0
            self.finalSpellLevels = []
            while i <self.Nspells:
                if self.spellLevels[i] == self.maxSpellLevels[i]:
                    self.finalSpellLevels.append(str(self.spellLevels[i]) + "max")
                else:
                    self.finalSpellLevels.append(self.spellLevels[i])
                i = i+1
        else:
            self.finalSpellLevels = 0
        return self.finalSpellLevels

    def hero_list(self, player_dict):
        if "heroes" in self.player_dict.keys():
            i = 0
            self.heroLevels = []
            self.heroNames = []
            length_heroes = len(self.player_dict["heroes"])
            while i < length_heroes:
                self.heroLevels.append(self.player_dict["heroes"][i]["level"])
                self.heroNames.append(str(self.player_dict["heroes"][i]["name"]))
                i = i+1
            i = 0
            while i < self.Nheroes:
                try:
                    if self.heroNames[i] != self.heroOrder[i]:
                        self.heroNames.insert(i, self.heroOrder[i])
                        self.heroLevels.insert(i, 0)
                except IndexError:
                    self.heroLevels.insert(i, 0)
                else:
                    pass
                i = i+1
            i = 0
            self.finalHeroLevels = []
            while i <self.Nheroes:
                if self.heroLevels[i] == self.maxHeroLevels[i]:
                    self.finalHeroLevels.append(str(self.heroLevels[i]) + "max")
                else:
                    self.finalHeroLevels.append(self.heroLevels[i])
                i = i+1
        else:
            self.finalHeroLevels = 0
        return self.finalHeroLevels

    def legend_statistics(self, player_dict):
        self.legendStatusInfo = []
        if "legendStatistics" in self.player_dict.keys():
            if "bestSeason" in self.player_dict["legendStatistics"].keys():
                self.legendStatus = 2
                self.bestSeasonRank = self.player_dict["legendStatistics"]["bestSeason"]["rank"]
                self.bestSeasonTrophies = self.player_dict["legendStatistics"]["bestSeason"]["trophies"]
                self.bestSeasonDate = self.player_dict["legendStatistics"]["bestSeason"]["id"]
                self.legendTrophies = self.player_dict["legendStatistics"]["legendTrophies"]
                self.legendStatusInfo.extend(["bestSeason Rank, Trophies, Date", "legendTrophies"])
                if "previousSeason" in self.player_dict["legendStatistics"].keys():
                    self.previousSeasonRank = self.player_dict["legendStatistics"]["previousSeason"]["rank"]
                    self.previousSeasonTrophies = self.player_dict["legendStatistics"]["previousSeason"]["trophies"]
                    self.previousSeasonDate = self.player_dict["legendStatistics"]["previousSeason"]["id"]
                    self.legendStatusInfo.append("previousSeason Rank, Trophies, Date")
                else:
                    self.legendStatus = 1
            else:
                self.legendStatus = 0
        else:
            self.legendStatus = 0
        self.legendStatusInfo.insert(0, self.legendStatus)
        return self.legendStatusInfo

    def main_info(self, player_dict):
        mainInfo = []
        self.playerLevel = self.player_dict["expLevel"]
        self.playerTag = self.player_dict["tag"]
        self.playerName = self.player_dict["name"]
        self.playerThLevel = self.player_dict["townHallLevel"]
        self.playerBestTrophies = self.player_dict["bestTrophies"]
        self.playerTrophies = self.player_dict["trophies"]
        #maybe check rank to see if you need to put a number on the legends badge
        self.playerWarStars = self.player_dict["warStars"]
        self.playerTroopsDonated = self.player_dict["donations"]
        self.playerTroopsReceived = self.player_dict["donationsReceived"]
        self.playerAttacksWon = self.player_dict["attackWins"]
        self.playerDefensesWon = self.player_dict["defenseWins"]
        if "clan" in self.player_dict.keys():
            self.ifClan = 1
            self.clanName = self.player_dict["clan"]["name"]
            self.clanTag = self.player_dict["clan"]["tag"]
            self.clanLevel = self.player_dict["clan"]["clanLevel"]
            self.clanBadgeURL = self.player_dict["clan"]["badgeUrls"]["small"]
            self.clanRole = self.player_dict["role"]
        else:
            self.ifClan = 0
        if "league" in self.player_dict.keys():
            self.ifLeague = 1
            self.leagueName = self.player_dict["league"]["name"]
            self.leagueID = self.player_dict["league"]["id"]
        else:
            self.ifLeague = 0
        ifClanLeague = []
        ifClanLeague.extend([self.ifClan, self.ifLeague])
        return ifClanLeague

    def picture_legends(self):
        self.legends_blank = Image.open("cocapifiles/blank_legends.png")
        draw = ImageDraw.Draw(self.legends_blank)
        nf1 = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 31)
        nf2 = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 23)
        nf3 = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        nf4 = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 32)
        nf5 = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 35)
        tf1 = ImageFont.truetype("cocapifiles/fonts/CCBackBeat-Light_5.ttf", 28)
        npxs1 = {"0":30, "1":15, "2":24, "3":24, "4":29, "5":24, "6":27, "7":24, "8":28, "9":27}
        npxs2 = {"0":23, "1":11, "2":17, "3":18, "4":21, "5":18, "6":20, "7":17, "8":21, "9":19}
        months = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"Septmeber", "10":"October", "11":"November", "12":"December"}
        cb1x = 91 #x value of the centre of badge1
        cb2x = 810 #x value of the centre of badge2
        white = 255,255,255
        black = 0,0,0

        i = 0
        p1 = 0
        p2 = 0
        while i < len(str(self.bestSeasonRank)):
            p1 = p1 + npxs1[str(self.bestSeasonRank)[i]]
            i = i+1
        if self.legendStatus == 2:
            i = 0
            while i < len(str(self.previousSeasonRank)):
                p2 = p2 + npxs2[str(self.previousSeasonRank)[i]]
                i = i+1
        else:
            pass

        xb1 = cb1x - math.floor(p1/2)
        yb1 = 102
        xb2 = cb2x - math.floor(p2/2)
        yb2 = 130
        xc1 = 277
        yc1 = 130
        xc2 = 935
        yc2 = 135
        xc3 = 1576
        yc3 = 124
        xt1a = 169
        xt1b = 763
        xt1c = 1436
        yt1 = 62

        best_year = str(self.bestSeasonDate)[0:4]
        best_month = months[str(self.bestSeasonDate)[5:]]
        s1 = "Best: " + best_month + " " + best_year + " Season"
        if self.legendStatus == 2:
            previous_year = str(self.previousSeasonDate)[0:4]
            previous_month = months[str(self.previousSeasonDate)[5:]]
            s2 = "Previous: " + previous_month + " " + previous_year + " Season"
        else:
            s2 = "Previous Season:"
        s3 = "Legend Trophies"

        draw.text((xb1+2,yb1), str(self.bestSeasonRank), black, font=nf1) #right
        draw.text((xb1-2,yb1), str(self.bestSeasonRank), black, font=nf1) #left
        draw.text((xb1,yb1-2), str(self.bestSeasonRank), black, font=nf1) #up
        draw.text((xb1,yb1+5), str(self.bestSeasonRank), black, font=nf1) #down 3
        draw.text((xb1,yb1), str(self.bestSeasonRank), white, font=nf1) #normal white

        if self.legendStatus == 2:
            draw.text((xb2+2,yb2), str(self.previousSeasonRank), black, font=nf2)
            draw.text((xb2-2,yb2), str(self.previousSeasonRank), black, font=nf2)
            draw.text((xb2,yb2-2), str(self.previousSeasonRank), black, font=nf2)
            draw.text((xb2,yb2+4), str(self.previousSeasonRank), black, font=nf2)
            draw.text((xb2,yb2), str(self.previousSeasonRank), white, font=nf2) #second badge
        else:
            didNotPlace = Image.open("cocapifiles/didNotPlace.png")
            self.legends_blank.paste(didNotPlace, (750,94))

        draw.text((xc1+2,yc1), str(self.bestSeasonTrophies), black, font=nf3)
        draw.text((xc1-2,yc1), str(self.bestSeasonTrophies), black, font=nf3)
        draw.text((xc1,yc1-2), str(self.bestSeasonTrophies), black, font=nf3)
        draw.text((xc1,yc1+6), str(self.bestSeasonTrophies), black, font=nf3)
        draw.text((xc1,yc1), str(self.bestSeasonTrophies), white, font=nf3) #first cups

        if self.legendStatus == 2:
            draw.text((xc2+2,yc2), str(self.previousSeasonTrophies), black, font=nf4)
            draw.text((xc2-2,yc2), str(self.previousSeasonTrophies), black, font=nf4)
            draw.text((xc2,yc2-2), str(self.previousSeasonTrophies), black, font=nf4)
            draw.text((xc2,yc2+5), str(self.previousSeasonTrophies), black, font=nf4)
            draw.text((xc2,yc2), str(self.previousSeasonTrophies), white, font=nf4) #second cups
        else:
            pass

        draw.text((xc3+2,yc3), str(self.legendTrophies), black, font=nf5)
        draw.text((xc3-2,yc3), str(self.legendTrophies), black, font=nf5)
        draw.text((xc3,yc3-2), str(self.legendTrophies), black, font=nf5)
        draw.text((xc3,yc3+6), str(self.legendTrophies), black, font=nf5)
        draw.text((xc3,yc3), str(self.legendTrophies), white, font=nf5) #third cups

        draw.text((xt1a+2,yt1), s1, black, font=tf1)
        draw.text((xt1a-2,yt1), s1, black, font=tf1)
        draw.text((xt1a,yt1-2), s1, black, font=tf1)
        draw.text((xt1a,yt1+3), s1, black, font=tf1)
        draw.text((xt1a,yt1+5), s1, black, font=tf1)
        draw.text((xt1a,yt1), s1, white, font=tf1) #first text

        draw.text((xt1b+2,yt1), s2, black, font=tf1)
        draw.text((xt1b-2,yt1), s2, black, font=tf1)
        draw.text((xt1b,yt1-2), s2, black, font=tf1)
        draw.text((xt1b,yt1+3), s2, black, font=tf1)
        draw.text((xt1b,yt1+5), s2, black, font=tf1)
        draw.text((xt1b,yt1), s2, white, font=tf1) #second text

        draw.text((xt1c+2,yt1), s3, black, font=tf1)
        draw.text((xt1c-2,yt1), s3, black, font=tf1)
        draw.text((xt1c,yt1-2), s3, black, font=tf1)
        draw.text((xt1c,yt1+3), s3, black, font=tf1)
        draw.text((xt1c,yt1+5), s3, black, font=tf1)
        draw.text((xt1c,yt1), s3, white, font=tf1) #third text

        return self.legends_blank

    def picture_main(self):
        self.mainblank = Image.open("cocapifiles/blank_profile.png")
        hf = ImageFont.truetype("cocapifiles/fonts/CCBackBeat-Light_5.ttf", 32)
        bn = ImageFont.truetype("cocapifiles/fonts/CCBackBeat-Light_5.ttf", 30)
        ws = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        xp = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 33)
        ln = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 29)
        cups = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 50)
        bestcups = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        role = ImageFont.truetype("cocapifiles/fonts/NotoNaskhArabic-Bold.ttf", 30)
        title = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 36)
        clan = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 26)
        draw = ImageDraw.Draw(self.mainblank)
        bnpxs = {"0":21, "1":11, "2":19, "3":20, "4":21, "5":20, "6":20, "7":17, "8":20, "9":20}
        xppxs = {"0":32, "1":16, "2":26, "3":25, "4":31, "5":26, "6":29, "7":25, "8":30, "9":28}
        LeagueIDText = {29000001:"Bronze League III", 29000002:"Bronze League II", 29000003:"Bronze_League_I", 29000004:"Silver League III", 29000005:"Silver League II", 29000006:"Silver League I", 29000007:"Gold League III", 29000008:"Gold League II", 29000009:"Gold League I", 29000010:"Crystal League III", 29000011:"Crystal League II", 29000012:"Crystal League I", 29000013:"Master League III", 29000014:"Master League II", 29000015:"Master League I", 29000016:"Champion League III", 29000017:"Champion League II", 29000018:"Champion League I", 29000019:"Titan League III", 29000020:"Titan League II", 29000021:"Titan League I", 29000022:"Legend League"}
        badge_start_x = {29000001:"1043", 29000002:"1043", 29000003:"1043", 29000004:"1043", 29000005:"1043", 29000006:"1043", 29000007:"1042", 29000008:"1042", 29000009:"1042", 29000010:"1013", 29000011:"1013", 29000012:"1013", 29000013:"1025", 29000014:"1025", 29000015:"1025", 29000016:"1019", 29000017:"1019", 29000018:"1019", 29000019:"1026", 29000020:"1026", 29000021:"1026", 29000022:"1036"}
        badge_start_y = {29000001:"40", 29000002:"40", 29000003:"40", 29000004:"56", 29000005:"56", 29000006:"56", 29000007:"14", 29000008:"14", 29000009:"14", 29000010:"49", 29000011:"49", 29000012:"49", 29000013:"11", 29000014:"11", 29000015:"11", 29000016:"33", 29000017:"33", 29000018:"33", 29000019:"35", 29000020:"35", 29000021:"35", 29000022:"48"} 
        lgs = ["u","b3","b2","b1","s3","s2","s1","g3","g2","g1","c3","c2","c1","m3","m2","m1","ch3","ch2","ch1","t3","t2","t1","l"]
        lgcups = [399,499,599,799,999,1199,1399,1599,1799,1999,2199,2399,2599,2799,2999,3199,3499,3799,4099,4399,4699,4999,10000000]
        role_d = {"admin":"Elder", "member":"Member", "coLeader":"Co-leader", "leader":"Leader"}
        hx = 128
        hy = 81
        bnxa_right = 418
        bnxb_right = 847
        bnxc_right = 1260
        bnxd_right = 1748
        bny = 402
        wsx = 1127
        wsy = 315
        xpx_middle = 71
        xpy = 50
        lnx = 1263
        lny = 74
        cupsx = 1340
        cupsy = 139
        bestcupsx = 1565
        bestcupsy = 314
        rolex = 124
        roley = 164
        titlex = 127
        titley = 29
        clanx = 124
        clany = 126

        i = 0
        pxbna = 0
        while i < len(str(self.playerTroopsDonated)):
            pxbna = pxbna + bnpxs[str(self.playerTroopsDonated)[i]]
            i = i+1
        i = 0
        pxbnb = 0
        while i < len(str(self.playerTroopsReceived)):
            pxbnb = pxbnb + bnpxs[str(self.playerTroopsReceived)[i]]
            i = i+1
        i = 0
        pxbnc = 0
        while i < len(str(self.playerAttacksWon)):
            pxbnc = pxbnc + bnpxs[str(self.playerAttacksWon)[i]]
            i = i+1
        i = 0
        pxbnd = 0
        while i < len(str(self.playerDefensesWon)):
            pxbnd = pxbnd + bnpxs[str(self.playerDefensesWon)[i]]
            i = i+1
        pxxp = 0
        i = 0
        while i < len(str(self.playerLevel)):
            pxxp = pxxp + xppxs[str(self.playerLevel)[i]]
            i = i+1

        bnxa = bnxa_right - pxbna
        bnxb = bnxb_right - pxbnb
        bnxc = bnxc_right - pxbnc
        bnxd = bnxd_right - pxbnd
        xpx = xpx_middle - math.floor(pxxp/2)

        hfc = 80,85,114
        white = 255,255,255
        black = 0,0,0

        draw.text((hx,hy), self.playerTag, hfc, font=hf) #hashtag

        draw.text((bnxa,bny), str(self.playerTroopsDonated), white, font=bn) #bottom numbers
        draw.text((bnxb,bny), str(self.playerTroopsReceived), white, font=bn)
        draw.text((bnxc,bny), str(self.playerAttacksWon), white, font=bn)
        draw.text((bnxd,bny), str(self.playerDefensesWon), white, font=bn)

        draw.text((wsx+2,wsy), str(self.playerWarStars), black, font=ws)
        draw.text((wsx-2,wsy), str(self.playerWarStars), black, font=ws)
        draw.text((wsx,wsy-2), str(self.playerWarStars), black, font=ws)
        draw.text((wsx,wsy+6), str(self.playerWarStars), black, font=ws)
        draw.text((wsx,wsy), str(self.playerWarStars), white, font=ws) #war stars

        draw.text((xpx+1, xpy), str(self.playerLevel), black, font=xp)
        draw.text((xpx-1, xpy), str(self.playerLevel), black, font=xp)
        draw.text((xpx, xpy-1), str(self.playerLevel), black, font=xp)
        draw.text((xpx, xpy+5), str(self.playerLevel), black, font=xp)
        draw.text((xpx, xpy), str(self.playerLevel), white, font=xp) #xp

        if self.ifLeague == 1:
            leagueText = LeagueIDText[self.leagueID]
        else:
            leagueText = "Unranked"
        draw.text((lnx-2,lny), leagueText, black, font=ln)
        draw.text((lnx+2,lny), leagueText, black, font=ln)
        draw.text((lnx,lny-2), leagueText, black, font=ln)
        draw.text((lnx,lny+5), leagueText, black, font=ln)
        draw.text((lnx,lny), leagueText, white, font=ln) #league name

        draw.text((cupsx+2,cupsy), str(self.playerTrophies), black, font=cups)
        draw.text((cupsx-2,cupsy), str(self.playerTrophies), black, font=cups)
        draw.text((cupsx,cupsy-2), str(self.playerTrophies), black, font=cups)
        draw.text((cupsx,cupsy+7), str(self.playerTrophies), black, font=cups)
        draw.text((cupsx,cupsy), str(self.playerTrophies), white, font=cups) #main cups

        if self.ifLeague == 1:
            x = int(badge_start_x[self.leagueID])
            y = int(badge_start_y[self.leagueID])
            badge_name = LeagueIDText[self.leagueID].replace(" ","_")
            badge = Image.open("cocapifiles/mainbadges/" + badge_name + ".png")
            self.mainblank.paste(badge, box=(x,y))
        else:
            pass

        if self.playerBestTrophies > 0:
            atbb = Image.open("cocapifiles/all_time_best_blank.png")
            self.mainblank.paste(atbb, box=(1373,242))
            draw.text((bestcupsx-2, bestcupsy), str(self.playerBestTrophies), black, font=bestcups)
            draw.text((bestcupsx+2, bestcupsy), str(self.playerBestTrophies), black, font=bestcups)
            draw.text((bestcupsx, bestcupsy-2), str(self.playerBestTrophies), black, font=bestcups)
            draw.text((bestcupsx, bestcupsy+6), str(self.playerBestTrophies), black, font=bestcups)
            draw.text((bestcupsx, bestcupsy), str(self.playerBestTrophies), white, font=bestcups) #best cups
        else:
            pass

        i = 0
        while i < len(lgcups):
            if self.playerBestTrophies > lgcups[i]:
                i = i+1
            else:
                break
        if lgs[i] == "u":
            pass
        else:
            atb_badge = Image.open("cocapifiles/atbbadges/" + lgs[i] + ".png")
            self.mainblank.paste(atb_badge, box=(1390,285))

        if self.ifClan == 1:
            role_img = Image.open("cocapifiles/role/" + role_d[self.clanRole] + ".png")
            self.mainblank.paste(role_img, box=(118,161))

            urllib.urlretrieve(self.clanBadgeURL, "cocapifiles/temp_clan_badge.png")
            badge1 = Image.open("cocapifiles/temp_clan_badge.png")
            backround = Image.open("cocapifiles/clan_badge_backround.png")
            badge_arr = np.array(badge1)
            back_arr = np.array(backround)
            w1, h1 = badge1.size
            w2, h2 = backround.size
            if (w2!=w1) or (h2!=h1):
                raise ValueError("Images do not have the same dimensions.")
            x = 0
            y = 0
            while (x<h1) and (y<w1):
                if badge_arr[x,y,3]==255:
                    back_arr[x,y] = badge_arr[x,y]
                x = x+1
                if x ==h1:
                    x=0
                    y=y+1
            composite_small = Image.fromarray(back_arr, "RGBA")
            size = 84,84
            composite = composite_small.resize(size, Image.ANTIALIAS)
            self.mainblank.paste(composite, box=(29,122))

            draw.text((clanx+2,clany), self.clanName, black, font=clan)
            draw.text((clanx-2,clany), self.clanName, black, font=clan)
            draw.text((clanx,clany-2), self.clanName, black, font=clan)
            draw.text((clanx,clany+4), self.clanName, black, font=clan)
            draw.text((clanx,clany+6), self.clanName, black, font=clan)
            draw.text((clanx,clany), self.clanName, white, font=clan)

        else:
            pass

        draw.text((titlex+2,titley),self.playerName,black,font=title)
        draw.text((titlex-2,titley),self.playerName,black,font=title)
        draw.text((titlex,titley-2),self.playerName,black,font=title)
        draw.text((titlex,titley+6),self.playerName,black,font=title)
        draw.text((titlex,titley),self.playerName,white,font=title)

        return self.mainblank

    def picture_troops(self):
        icon_path = "cocapifiles/Icons/"
        icon_xy = {"Barbarian":(219,82),"Archer":(301,82),"Goblin":(463,82),"Giant":(382,82),"Wall_Breaker":(545,82),"Balloon":(627,82),"Wizard":(708,82),"Healer":(790,82),"Dragon":(872,82),"P.E.K.K.A":(953,82),"Minion":(382,162),"Hog_Rider":(463,162),"Valkyrie":(545,162),"Golem":(627,162),"Witch":(708,162),"Lava_Hound":(790,162),"Bowler":(872,162),"Baby_Dragon":(219,162),"Miner":(301,162),"Lightning_Spell":(1056,83),"Healing_Spell":(1137,83),"Rage_Spell":(1219,83),"Jump_Spell":(1301,83),"Freeze_Spell":(1381,83),"Poison_Spell":(1137,163),"Earthquake_Spell":(1219,163),"Haste_Spell":(1301,163),"Clone_Spell":(1056,163),"Skeleton_Spell":(1381,163),"Barbarian_King":(1481,83),"Archer_Queen":(1561,83),"Grand_Warden":(1643,83)}
        leveltext = ImageFont.truetype("cocapifiles/fonts/Supercell-Magic_5.ttf", 13)
        leveltextpxs = {"0":13, "1":6, "2":10, "3":10, "4":12, "5":10, "6":11, "7":10, "8":12, "9":11}
        backround = Image.open("cocapifiles/blank_troops.png")
        th = Image.open("cocapifiles/townHall/" + str(self.playerThLevel) + ".png")
        backround.paste(th, box=(0,20))

        def put1on2(img1, img2):
            img3 = Image.alpha_composite(img2, img1)
            return img3

        i = 0
        while i < self.Ntroops:
            if self.finalTroopLevels[i] != 0:
                icon_name = self.troopOrder[i]
                if icon_name.find(" ") > -1:
                    icon_name = icon_name.replace(" ","_")
                troopimg1 = Image.open(icon_path + icon_name + ".png")
                if self.finalTroopLevels[i] != 1:
                    level_name = str(self.finalTroopLevels[i])
                    levelimg = Image.open(icon_path + level_name + ".png")
                    wL, hL = levelimg.size
                    troopimg2 = troopimg1.crop(box=(5,44,(5+wL),(44+hL)))
                    troopimg3 = put1on2(levelimg,troopimg2)
                    troopimg1.paste(troopimg3, box=(5,44))
                backround.paste(troopimg1, box=icon_xy[icon_name])
            i = i+1

        i = 0
        if self.finalSpellLevels != 0:
            while i < self.Nspells:
                if self.finalSpellLevels[i] != 0:
                    icon_name = self.spellOrder[i]
                    icon_name = icon_name.replace(" ","_")
                    spellimg1 = Image.open(icon_path + icon_name + ".png")
                    if self.finalSpellLevels[i] != 1:
                        level_name = str(self.finalSpellLevels[i])
                        levelimg = Image.open(icon_path + level_name + ".png")
                        wL, hL = levelimg.size
                        spellimg2 = spellimg1.crop(box=(5,44,(5+wL),(44+hL)))
                        spellimg3 = put1on2(levelimg,spellimg2)
                        spellimg1.paste(spellimg3, box=(5,44))
                    backround.paste(spellimg1, box=icon_xy[icon_name])
                i = i+1

        white = 255,255,255
        black = 0,0,0
        i = 0
        if self.finalHeroLevels != 0:
            while i < self.Nheroes:
                if self.finalHeroLevels[i] != 0:
                    icon_name = self.heroOrder[i]
                    icon_name = icon_name.replace(" ","_")
                    heroimg1 = Image.open(icon_path + icon_name + ".png")
                    if (len(str(self.finalHeroLevels[i])) == 5) or (len(str(self.finalHeroLevels[i])) == 1): #checking if it's Nmax or one digit
                        level_name = str(self.finalHeroLevels[i])
                        levelimg = Image.open(icon_path + level_name + ".png")
                        wL, hL = levelimg.size
                        heroimg2 = heroimg1.crop(box=(4,45,(4+wL),(45+hL)))
                        heroimg3 = put1on2(levelimg,heroimg2)
                        heroimg1.paste(heroimg3, box=(4,45))
                    else:
                    	levelimg = Image.open(icon_path + "nonmaxhero.png")
                    	wL, hL = levelimg.size
                    	heroimg2 = heroimg1.crop(box=(4,46,(4+wL),(46+hL)))
                    	heroimg3 = put1on2(levelimg,heroimg2)
                    	draw = ImageDraw.Draw(heroimg3)
                    	level = str(self.finalHeroLevels[i])
                    	heroy = 4
                    	hero_middle = 14
                    	m = 0
                    	hpxs = 0
                    	while m < len(level):
                    		hpxs = hpxs + leveltextpxs[level[m]]
                    		m = m+1
                    	herox = hero_middle - math.floor((hpxs/2))
                    	draw.text((herox-1, heroy), level, black, font=leveltext)
                    	draw.text((herox+1, heroy), level, black, font=leveltext)
                    	draw.text((herox, heroy-1), level, black, font=leveltext)
                    	draw.text((herox, heroy+3), level, black, font=leveltext)
                    	draw.text((herox, heroy), level, white, font=leveltext)
                    	heroimg1.paste(heroimg3, box=(4,46))
                    backround.paste(heroimg1, box=icon_xy[icon_name])
                i = i+1

        self.troops_blank = backround
        return self.troops_blank

    def makeProfile(self, player_hash, path="/var/www/html/", name="test"):
        info = self.player_info(player_hash)
        if self.statusCode == 200:
            troops = self.troop_list(info)
            spells = self.spell_list(info)
            heroes = self.hero_list(info)
            main = self.main_info(info)
            legendS = self.legend_statistics(info)
            pm = self.picture_main()
            wm, hm = pm.size
            pt = self.picture_troops()
            wt, ht = pt.size
            if self.legendStatus == 0:
                wl = 0
                hl = 0
            else:
                pl = self.picture_legends()
                wl, hl = pl.size
            x = wm
            y = hm + ht + hl
            new = Image.new("RGB", (x,y), color=0)
            new.paste(pm)
            if self.legendStatus != 0:
            	new.paste(pl, box=(0, hm))
            new.paste(pt, box=(0, hm + hl))
            new.save(path+name+ ".jpg", "JPEG")
            return self.statusCode
        else:
            return self.statusCode

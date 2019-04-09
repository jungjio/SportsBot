from discord.ext import commands
import lxml.etree as ET
import datetime
from datetime import date
import discord
import time
import os
import requests




TOKEN = os.environ['TOKEN']
client = discord.Client()


@client.event
async def on_message(message):
    if message.content.startswith('!nba streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/nbastreams/")

    if message.content.startswith('!mlb streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/MLBStreams/")

    if message.content.startswith('!soccer streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/redsoccer/")

    if message.content.startswith('!nfl streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/nflstreams/")

    if message.content.startswith('!ncaa streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/ncaaBBallStreams/")

    if message.content.startswith('!mma streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/MMAStreams/")

    if message.content.startswith('!cfb streams'):
        first_message = await client.send_message(message.channel, "https://www.reddit.com/r/CFBstreams")



#################################################################################################################################################################


    if message.content.startswith('!nba news'):
        today = (date.today()).strftime('%Y-%m-%d')
        today = today.replace("-", "")
        NBALINK = ("http://data.nba.net/10s/prod/v1/%s/scoreboard.json" %(today)) #replay with today 20190403
        print(NBALINK)

        r = requests.get(NBALINK)

        gamesJson = r.json()
        output = ''


        if gamesJson["numGames"] > 0:
            array =  gamesJson["games"]

            for x in range(len(array)):

                homeTeamScoreAndTriCode = array[x]["hTeam"]
                homeTeamScore = homeTeamScoreAndTriCode["score"]
                homeTeamTriCode = homeTeamScoreAndTriCode["triCode"]

                awayTeamScoreAndTriCode = array[x]["vTeam"]
                awayTeamScore = awayTeamScoreAndTriCode["score"]
                awayTeamTriCode = awayTeamScoreAndTriCode["triCode"]

                outstandingnews = array[x]["nugget"]['text']
                if outstandingnews != '':
                    output += "***"+ homeTeamTriCode + "*** vs ***"+ awayTeamTriCode +"*** : "+ outstandingnews + '\n'


        print(output)

        await client.send_message(message.channel, output)

#################################################################################################################################################################

    if message.content.startswith('!nba scores'):
        today = (date.today()).strftime('%Y-%m-%d')
        today = today.replace("-", "")
        NBALINK = ("http://data.nba.net/10s/prod/v1/%s/scoreboard.json" %(today)) #replay with today 20190403
        print(NBALINK)

        r = requests.get(NBALINK)

        gamesJson = r.json()
        output = ''


        if gamesJson["numGames"] > 0:
            array =  gamesJson["games"]
            embed=discord.Embed(title="NBA Sports Bot", description="Created by @J.io#5484", color=0x4480ff)
            embed.set_thumbnail(url="https://assets.materialup.com/uploads/347c48be-3ed3-4e80-87a0-3353405f0239/0x0ss-85.jpg")
            embed.add_field(name='NBA Scores', value='\u200b', inline=False)

            for x in range(len(array)):

              homeTeamScoreAndTriCode = array[x]["hTeam"]
              homeTeamScore = homeTeamScoreAndTriCode["score"]
              homeTeamTriCode = homeTeamScoreAndTriCode["triCode"]

              awayTeamScoreAndTriCode = array[x]["vTeam"]
              awayTeamScore = awayTeamScoreAndTriCode["score"]
              awayTeamTriCode = awayTeamScoreAndTriCode["triCode"]

              outstandingnews = array[x]["nugget"]['text']
              print(outstandingnews)

              period = array[x]["period"]['current']
              if (period==0):
                  outstandingnews = 'Game starts at ' + array[x]["startTimeEastern"]
              elif (period > 0 and outstandingnews ==''):
                  outstandingnews = 'Q' + str(period)  + ' | Minutes left :  ' + array[x]['clock']

              output = output + (homeTeamTriCode + ' ' + homeTeamScore + " - " +  awayTeamScore + ' ' + awayTeamTriCode + '\n' + outstandingnews + '\n')
              embed.add_field(name=(homeTeamTriCode + ' ' + homeTeamScore + " - " +  awayTeamScore + ' ' + awayTeamTriCode), value=outstandingnews, inline=False)

        else:
             embed.add_field(name="No NBA games today!", value="Sorry!", inline=False)

        print(output)

        await client.send_message(message.channel, embed=embed)





#################################################################################################################################################################




    if message.content.startswith('!mlb score'):
        MONTH = date.today().month
        if int(MONTH) <= 9:
          MONTH = "0" + str(MONTH)

        DAY = date.today().day
        if int(DAY) <= 9:
          DAY = "0" + str(DAY)

        YEAR = str(date.today().year)

        MLBLINK = ("http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/master_scoreboard.xml" %(YEAR, MONTH, DAY))
        awayTeamScore = []
        homeTeamScore = []
        awayTeam = []
        homeTeam = []
        status = []

        r = requests.get(MLBLINK)
        root = ET.fromstring(r.content)
        ouputMLB = ''

        for child in root.iter('r'):
            awayTeamScore.append(str(child.attrib['away']))
            homeTeamScore.append(str(child.attrib['home']))
        for child in root.iter('game'):
            awayTeam.append((child.attrib['away_team_city']))
            homeTeam.append((child.attrib['home_team_city']))
        for child in root.iter('status'):
            status.append((child.attrib['status']))

        print(homeTeam,homeTeamScore,awayTeamScore, awayTeam,status)
        print (homeTeamScore)


        #print(awayTeamScore,homeTeamScore,awayTeam,homeTeam)
        embed=discord.Embed(title="MLB SPORTS BOT", description="Created by @J.io#5484", color=0x4480ff)
        embed.set_thumbnail(url="https://assets.materialup.com/uploads/57a21b2b-de21-400f-8908-c5ff18b7ac63/preview.jpg")
        embed.add_field(name='MLB scores', value='\u200b', inline=False)

        if (len(homeTeamScore) != len(homeTeam)) and (len(awayTeamScore) != len(awayTeam)):
            for z in range((len(homeTeam) - len(homeTeamScore))):
                homeTeamScore.append('0')
                awayTeamScore.append('0')



        if (len(homeTeam) == 0 and len(homeTeam) ==0 and len(awayTeamScore) == 0 and len(homeTeamScore) == 0):
            embed.add_field(name='ERR: No Games Displayed on backend.', value='', inline=False)

        print(len(homeTeamScore))
        for x in range(len(homeTeam)):
            #ouputMLB += (homeTeam[x] + ' '  + homeTeamScore[x] + ' - ' + awayTeamScore[x] + ' ' + awayTeam[x] + '\n')
            embed.add_field(name=homeTeam[x] + ' '  + homeTeamScore[x] + ' - ' + awayTeamScore[x] + ' ' + awayTeam[x], value=status[x], inline=False)

        print(ouputMLB)

        await client.send_message(message.channel, embed=embed)






@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


while True:
    #client.wait_until_ready()
    client.run(TOKEN)
    # time.sleep(20)

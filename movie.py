import discord
import random
import tmdbsimple as tmdb
import os
from discord_slash import SlashCommand

tmdb.API_KEY = os.environ['APIKEY']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

disc = tmdb.Discover()
imgurl = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
linkurl = "https://www.themoviedb.org/movie/"

@slash.slash(name="ranmov",
             description="Random movie",
             guild_ids = ['SERVER IDS HERE'])
async def ranmov(ctx):
  year = random.randint(1970,2021)
  getpgs = disc.movie(primary_release_year=year, sort_by= "vote_count.desc", with_original_language = 'en', vote_count_gte= 10)

  tp = getpgs['total_pages']
  pg = random.randint(1,tp)

  themovie = random.choice(disc.movie(primary_release_year=year, sort_by= "vote_count.desc", page= pg, with_original_language = 'en', vote_count_gte= 10)['results'])

  moviegensids = list(themovie['genre_ids'])
  themoveinfo = tmdb.Movies(themovie['id']).info() # has more info about movie
  allgens = tmdb.Genres().movie_list()['genres']
  moviegens = ""
  for gen in allgens:
    if gen['id'] in moviegensids:
        moviegens = moviegens + gen['name'] + ", "
  if len(moviegens) != 0:
    moviegens = moviegens[:-2]

  embed=discord.Embed(title="Movie", color=0x2bff00)
  embed.add_field(name="Name:", value=themoveinfo['title'], inline=False)
  embed.add_field(name="Year:", value=themoveinfo['release_date'][:4], inline=False)
  embed.add_field(name="Genres:", value=moviegens, inline=False)
  embed.add_field(name="Rating:", value=themoveinfo['vote_average'], inline=False)
  embed.add_field(name="Link", value=linkurl+str(themoveinfo['id'])+themoveinfo['title'].replace(" ", "-"))
  embed.add_field(name="Story:", value=themoveinfo['overview'], inline=False)
  embed.set_image(url=imgurl+themoveinfo['poster_path'])
  await ctx.send(embed=embed)

@slash.slash(name="recmov",
             description="Three movie recommendations when given title. Multi word titles are done like so \"Spy Kids\"",
             guild_ids = ['SERVER IDS HERE'])
async def recmov(ctx, query):
  try:
    movsearch =  tmdb.Search().movie(query=query)['results'][0]
    movrecs = tmdb.Movies(movsearch['id']).recommendations()['results'][:3]

    embed=discord.Embed(title="Movie Recs", color=0x2bff00)
    embed.add_field(name="Given Movie:", value=movsearch['title'], inline=False)
    embed.add_field(name="Name:", value=movrecs[0]['title'], inline=False)
    embed.add_field(name="Link", value=linkurl+str(movrecs[0]['id'])+movrecs[0]['title'].replace(" ", "-"))
    embed.add_field(name="Name:", value=movrecs[1]['title'], inline=False)
    embed.add_field(name="Link", value=linkurl+str(movrecs[1]['id'])+movrecs[1]['title'].replace(" ", "-"))
    embed.add_field(name="Name:", value=movrecs[2]['title'], inline=False)
    embed.add_field(name="Link", value=linkurl+str(movrecs[2]['id'])+movrecs[2]['title'].replace(" ", "-"))
    embed.set_image(url=imgurl+movsearch['poster_path'])
    await ctx.send(embed=embed)
  except:
    await ctx.send("Bad Title")

@slash.slash(name="getmov",
             description="Info about movie when given title. Multi word titles are done like so \"Spy Kids\"",
             guild_ids = ['SERVER IDS HERE'])
async def getmov(ctx, query):
  try:
    movsearch =  tmdb.Search().movie(query=query)['results'][0]

    moviegensids = list(movsearch['genre_ids'])
    themoveinfo = tmdb.Movies(movsearch['id']).info() # has more info about movie
    allgens = tmdb.Genres().movie_list()['genres']
    moviegens = ""
    for gen in allgens:
      if gen['id'] in moviegensids:
          moviegens = moviegens + gen['name'] + ", "
    if len(moviegens) != 0:
      moviegens = moviegens[:-2]


    embed=discord.Embed(title="Movie", color=0x2bff00)
    embed.add_field(name="Name:", value=themoveinfo['title'], inline=False)
    embed.add_field(name="Year:", value=themoveinfo['release_date'][:4], inline=False)
    embed.add_field(name="Genres:", value=moviegens, inline=False)
    embed.add_field(name="Rating:", value=themoveinfo['vote_average'], inline=False)
    embed.add_field(name="Link", value=linkurl+str(themoveinfo['id'])+themoveinfo['title'].replace(" ", "-"))
    embed.add_field(name="Story:", value=themoveinfo['overview'], inline=False)
    embed.set_image(url=imgurl+themoveinfo['poster_path'])
    await ctx.send(embed=embed)
  except:
    await ctx.send("Bad Title")

    
  bot.run('DISCORD TOKEN')

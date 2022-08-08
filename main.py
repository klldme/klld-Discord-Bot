import discord.ext
import discord.ext.commands
import discord.embeds
import asyncio
import requests
import json
import random

#loads config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

bot = discord.ext.commands.AutoShardedBot(
    command_prefix=config['prefix'],
)
#removes default help command
bot.remove_command('help')

def random_embed_color():
    return discord.Color(random.randint(0, 0xFFFFFF))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def help(ctx):
    embed = discord.embeds.Embed(title="Help", description="This is a list of commands you can use", color=random_embed_color())
    embed.add_field(name="!help", value="Shows this message", inline=False)
    embed.add_field(name="!ping", value="Pong!", inline=False)
    embed.add_field(name="!aes", value="AES Encryption For Fortnite Paks", inline=False)
    embed.add_field(name="!news", value="Shows the newest news", inline=False)
    embed.add_field(name="!map", value="Shows the map", inline=False)
    embed.add_field(name="!search", value="Searches for a cosmetic information", inline=False)
    embed.set_footer(text="Requested by " + ctx.message.author.name)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.embeds.Embed(title="Pong!", description="Pong!", color=random_embed_color())
    embed.add_field(name="Latency", value=str(round(bot.latency * 1000)) + "ms", inline=False)
    embed.set_footer(text="Requested by " + ctx.message.author.name)
    await ctx.send(embed=embed)

@bot.command()
async def aes(ctx):
    r = requests.get('https://fortnite-api.com/v2/aes')
    #convert the response to json
    data = r.json()

    aes = data['data']['mainKey']

    embed = discord.embeds.Embed(title="AES Encryption", description="AES Encryption For Fortnite Paks", color=random_embed_color())
    embed.add_field(name="AES", value=aes, inline=False)
    embed.set_footer(text="Requested by " + ctx.message.author.name)
    await ctx.send(embed=embed)

@bot.command()
async def news(ctx):
    r = requests.get('https://fortnite-api.com/v2/news')
    #convert the response to json
    data = r.json()
    image = data['data']['br']['image']
    embed = discord.embeds.Embed(title="News", description="News", color=random_embed_color())
    embed.set_image(url=image)
    embed.set_footer(text="Requested by " + ctx.message.author.name)
    await ctx.send(embed=embed)

@bot.command()
async def map(ctx):
    r = requests.get('https://fortnite-api.com/v1/map')
    #convert the response to json
    data = r.json()

    map = data['data']['images']['pois']
    embed = discord.embeds.Embed(title="Map", color=random_embed_color())
    embed.set_image(url=map)
    embed.set_footer(text="Requested by " + ctx.message.author.name)
    await ctx.send(embed=embed)

@bot.command()
async def search(ctx, *, search):
    r = requests.get('https://fortnite-api.com/v2/cosmetics/br/search?name='+search)
    #convert the response to json
    data = r.json()
    id = data['data']['id']
    name = data['data']['name']
    rarity = data['data']['rarity']['displayValue']
    type = data['data']['type']['displayValue']
    image = data['data']['images']['icon']
    path = data['data']['path']
    gameplaytags = data['data']['gameplayTags'][1]
    added = data['data']['added']
    embed = discord.embeds.Embed(title="Search", description="Search", color=random_embed_color())
    embed.set_image(url=image)
    embed.add_field(name="ID", value=id, inline=False)
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Rarity", value=rarity, inline=False)
    embed.add_field(name="Type", value=type, inline=False)
    embed.add_field(name="Path", value=path, inline=False)
    embed.add_field(name="Gameplay Tags", value=gameplaytags, inline=False)
    embed.add_field(name="Added", value=added, inline=False)
    embed.set_footer(text="Requested by " + ctx.message.author.name)
    await ctx.send(embed=embed)


bot.run(config['token'])

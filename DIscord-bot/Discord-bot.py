from tokenize import String
import discord
from typing import Type
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
import json
import pandas as pd
from datetime import datetime
import requests
from discord.ext import commands 
import os
from dotenv import load_dotenv


cg = CoinGeckoAPI()
client = discord.Client()
bot = commands.Bot(command_prefix="$")

response = requests.get("https://newsapi.org/v2/everything?q=crypto&apiKey={b640b460e51d4a94b557f0c223632446}")
data = json.loads(response.text)

all_articles = data['articles']

def get_crypto_chart(token):
        chart_data = cg.get_coin_market_chart_by_id(id=f'{token}', vs_currency='aud', days='7')

        def unix_to_date(unix_time):
            timestamp = datetime.fromtimestamp((unix_time/1000))
            return f"{timestamp.strftime('%d-%m-%Y %H:%M:%S')}"


        new_data = {}

        for each in chart_data['prices']:
            date = unix_to_date(each[0])
            new_data[date] = each[1]

        df = pd.DataFrame({'Dates': new_data.keys(), 'Prices': new_data.values()})
        print(df.head())

        df.plot(x ='Dates', y='Prices', kind = 'line', legend = None)	
        plt.axis('off')
        plt.title(f'7-day historical market price of {token}', fontsize=15, color= 'white', fontweight='bold');


        filename =  "/Users/niccolomerlatti/Desktop/test.png"
        plt.savefig(filename, transparent=True)

        plt.close()




class Coin:
    def __init__(self, name):
        self.name = name.lower()
        
        self.coin_data = cg.get_coins_markets(vs_currency='aud', ids=f'{self.name}')
        
        self.coin_name = self.coin_data[0]['name']
        self.coin_image = self.coin_data[0]["image"]
        self.coin_price = "${:,}".format(self.coin_data[0]['current_price'])

        self.coin_circulating_supply = "{:,}".format(self.coin_data[0]["circulating_supply"])
        self.coin_market_cap = "{:,}".format(self.coin_data[0]['market_cap'])

        self.coin_high_24h = "${:,}".format(self.coin_data[0]['high_24h'])
        self.coin_low_24h = "${:,}".format(self.coin_data[0]['low_24h'])

        self.coin_price_change_percent = "{:,}%".format(round(self.coin_data[0]['price_change_percentage_24h'], 2))
        
        self.coin_ath_price = "${:,}".format(self.coin_data[0]["ath"])
        self.coin_ath_change_percent = "{:,}%".format(self.coin_data[0]["ath_change_percentage"])
        self.coin_atl = "${:,}".format(self.coin_data[0]["atl"])



btc = Coin('bitcoin')
xrp = Coin('ripple')
eth = Coin('ethereum')
bnb = Coin('binance')
sol = Coin('solana')
ada = Coin('cardano')
matic = Coin('polygon')
sand = Coin('sandbox')
mana = Coin('decentraland')
algo = Coin('algorand')


trending_data = cg.get_search_trending()
trending_tokens = []
count_1 = 1
for each in trending_data["coins"]:
    item = each["item"]["name"]
    trending_tokens.append(f"({count_1}). {item} \n")
    count_1 += 1

trending_coins = ''.join(trending_tokens)

market_percent_data = cg.get_global()
upcoming_ico_data = None
ongoing_ico_data = None
ended_ico_data = None

upcoming_ico_data = market_percent_data["upcoming_icos"]
ongoing_ico_data = market_percent_data["ongoing_icos"]
ended_ico_data = market_percent_data["ended_icos"]


market_cap_percentage_data = cg.get_search_trending()
market_cap_percentage = []
count_2 = 1
for k, v in market_percent_data["market_cap_percentage"].items():
    market_cap_percentage.append(f"({count_2}). {k}: {round(v, 2)}% \n")
    count_2 += 1
market_dom = ''.join(market_cap_percentage)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Converts user's input into a lowercase form
    message.content = message.content.lower().replace(' ', '')
    
    if message.author == client.user:
        return

    if message.content.startswith("$help"):
        await message.channel.send("""
        The following crypto prices are available, btc, eth, xrp, bnb, matic, sandbox, ada, and sol.
        To get the price of your chosen coin/token, simply put '$' before the ticker symbol of your token. For example $btc
        List of available commands:
        $trending""")

    if message.content.startswith("$trending"):
        await message.channel.send(f"Top 7 trending search coins\n-------------------------------------\n{trending_coins}")

    if message.content.startswith("$market_dominance"):
        await message.channel.send(f"Market Cap Percentage\n-------------------------------------\n{market_dom}")


    # Return the top 5 news articles related to crypto from the NewAPI.
    if message.content.startswith('$news'):
        count = 0
        await message.channel.send(f"Hey {author.user.name}, check your DMs for the todays Top 5 news articles")
        for each in all_articles:
            count += 1
            await message.author.send(f"**{count}:- {each['title']}**\n*{each['content']}*\n{each['url']}")
            if count == 5:
                break
    

    if message.content.startswith('$btc'):
        get_crypto_chart('bitcoin')
        
        #### Create the initial embed object ####
        embed=discord.Embed(title=f"{btc.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{btc.coin_image}")

        embed.add_field(name="Current Price ", value=btc.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= btc.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${btc.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= btc.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= btc.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= btc.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= btc.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= btc.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = btc.coin_atl, inline=True)
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$xrp'):
        get_crypto_chart('ripple')
        

        #### Create the initial em 
        embed=discord.Embed(title=f"{xrp.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{xrp.coin_image}")

        embed.add_field(name="Current Price ", value= xrp.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= xrp.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${xrp.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= xrp.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= xrp.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= xrp.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= xrp.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= xrp.coin_ath_change_percent , inline=True)
        embed.add_field(name="ATL ", value = xrp.coin_atl, inline=True)
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")


        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$eth'):
        get_crypto_chart('ethereum')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{eth.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{eth.coin_image}")

        embed.add_field(name="Current Price ", value = eth.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= eth.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${eth.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= eth.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= eth.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= eth.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= eth.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= eth.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = eth.coin_atl, inline=True)
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)

    
    if message.content.startswith('$bnb'):
        get_crypto_chart('binance')
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{bnb.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{bnb.coin_image}")

        embed.add_field(name="Current Price ", value= bnb.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= bnb.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${bnb.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= bnb.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= bnb.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= bnb.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value=bnb.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value=bnb.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = bnb.coin_atl, inline=True)

        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)
    
    if message.content.startswith('$ada'):
        get_crypto_chart('cardano')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{ada.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{ada.coin_image}")

        embed.add_field(name="Current Price ", value= ada.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= ada.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${ada.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= ada.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= ada.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= ada.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= ada.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= ada.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = ada.coin_atl, inline=True)
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$sol'):
        get_crypto_chart('solana')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{sol.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{sol.coin_image}")

        embed.add_field(name="Current Price ", value= sol.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= sol.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${sol.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= sol.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= sol.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= sol.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= sol.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= sol.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = sol.coin_atl, inline=True)
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$sand'):
        get_crypto_chart('sandbox')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{sand.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{sand.coin_image}")

        embed.add_field(name="Current Price ", value= sand.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= sand.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${sand.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= sand.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= sand.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= sand.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= sand.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= sand.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = sand.coin_atl, inline=True)
        
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)
    
    if message.content.startswith('$matic'):
        get_crypto_chart('polygon')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{matic.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{matic.coin_image}")

        embed.add_field(name="Current Price ", value= matic.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= matic.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${matic.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= matic.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= matic.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= matic.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= matic.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= matic.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = matic.coin_atl, inline=True)

        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)


    
    if message.content.startswith('$mana'):
        get_crypto_chart('decentraland')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{mana.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{mana.coin_image}")

        embed.add_field(name="Current Price ", value= mana.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= mana.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${mana.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= mana.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= mana.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= mana.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= mana.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= mana.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = mana.coin_atl, inline=True)

        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$algo'):
        get_crypto_chart('algorand')
        
        #### Create the initial embed object 
        embed=discord.Embed(title=f"{algo.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{algo.coin_image}")

        embed.add_field(name="Current Price ", value= algo.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= algo.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap ", value= f"${algo.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ", value= algo.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ", value= algo.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ", value= algo.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High ", value= algo.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change ", value= algo.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL ", value = algo.coin_atl, inline=True)
        
        file = discord.File("/Users/niccolomerlatti/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot")

        await message.channel.send(file=file, embed=embed)

client.run('Discord_Token')

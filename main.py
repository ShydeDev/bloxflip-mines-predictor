import hashlib
import random
import discord
import webcolors
import numpy
from discord.ext import commands

# skid settings
FOOTER_CONTENT = 'made by notshyde'
EMBED_COLOR = 'lightblue' # supports css3 colors or just random string
ROUND_ID_CHECK = False
BOT_TOKEN = 'your_bot_token_here'

# setup the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

def predict_tiles(round_id, num_tiles):
    random.seed(int(hashlib.md5(round_id.encode()).hexdigest(), 16)) # encode a round_id string into bytes, then hash bytes using md5, return as hexademical string and convert to int base-16 (hexademical)
    grid = numpy.full((5, 5), "❌", dtype=str) # create a grid full of crossmarks
    safe_tiles = set(range(25)) - set(random.sample(range(25), 25 - num_tiles)) # select random tiles from range 0 - 24
    if not (0 < num_tiles <= 25):
        raise ValueError("num_tiles must be between 0 and 25 inclusive")
    for tile in safe_tiles:
        grid[tile // 5, tile % 5] = "🟢" # set valid positions in grid with green circle
    return grid

def color_name_to_hex(color_name):
    try:
        hex_color_int = int(webcolors.name_to_hex(color_name).replace('#', ''), 16)
    except ValueError:
        hex_color_int = hash(color_name) & 0xFFFFFF
    return hex_color_int

@bot.command(name='mines', description='mines predictor')
async def mines(ctx, tile_predict: int, round_id: str):
    if len(round_id) != 36 and ROUND_ID_CHECK:
        await ctx.reply('invalid round id')
        return
    grid = '\n'.join([' '.join(row) for row in predict_tiles(round_id, tile_predict)]) # combine array rows into a string
    embed = discord.Embed(title="PREDICTION", description=f"```\n{grid}```", color=color_name_to_hex(EMBED_COLOR))
    embed.add_field(name="ROUND ID", value=f'\n```{round_id}```')
    embed.set_footer(text=FOOTER_CONTENT)
    await ctx.reply(embed=embed)

bot.run(BOT_TOKEN)

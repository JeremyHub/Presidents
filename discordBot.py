import discord
from discord.ext import commands
import sys
from io import BytesIO

from player import *
from game import *
from decks_and_cards import *
from presRound import *
from randomPlayer import *
from worstPlayer import *
from noTwoPlayer import *
from twoerPlayer import *
from personInputPlayer import *
from oldPlayer import *

client = commands.Bot(command_prefix=':')

def str_to_class(className):
    return getattr(sys.modules[__name__], className)

@client.event
async def on_ready():
    print('ready')

@client.command(aliases=['startbotgame', 'StartBotGame'])
async def startBotGame(ctx):
    await ctx.send('Please input the following parameters for your game:')
    name = ""
    numberOfPlayers = int
    numRounds = int
    passingRules = "none"
    numDecks = int
    amountOfNewPlayers = int
    shouldPrint = False
    anti = False
    restOfPlayers = Player
    newPlayers = Player

    orig_stdout, sys.stdout = sys.stdout, BytesIO()

    # await ctx.send('Name of the game?')
    # message = await client.wait_for('message')
    # name = str(message.content)
    #
    # await ctx.send('Number of players in the game?')
    # message = await client.wait_for('message')
    # numberOfPlayers = int(message.content)
    #
    # await ctx.send('Number of rounds?')
    # message = await client.wait_for('message')
    # numRounds = int(message.content)
    #
    # await ctx.send('What passing rules? (options: two, one, hybrid, none)')
    # message = await client.wait_for('message')
    # passingRules = str(message.content)
    #
    # await ctx.send('How many decks?')
    # message = await client.wait_for('message')
    # numDecks = int(message.content)
    #
    # await ctx.send('What players? (type def for default Player)')
    # message = await client.wait_for('message')
    # if not str(message.content) == 'def':
    #     restOfPlayers = str_to_class(message.content)
    #
    # await ctx.send('Print the game? (T or F) (if not, it will print heuristics)')
    # message = await client.wait_for('message')
    # if str(message.content).lower() == 't':
    #     shouldPrint = True
    # if str(message.content).lower() == 'f':
    #     shouldPrint = False
    #
    # await ctx.send('What should the other player be? (type def for default Player)')
    # message = await client.wait_for('message')
    # if not str(message.content) == 'def':
    #     newPlayers = str_to_class(message.content)
    #
    # await ctx.send('How many of those players?')
    # message = await client.wait_for('message')
    # amountOfNewPlayers = int(message.content)
    #
    # await ctx.send('Should they anti? (T or F)')
    # message = await client.wait_for('message')
    # if str(message.content).lower() == 't':
    #     anti = True
    # if str(message.content).lower() == 'f':
    #     anti = False

    # newGame = Game(numberOfPlayers, name, numRounds, passingRules, numDecks, restOfPlayers, shouldPrint, newPlayers, amountOfNewPlayers, anti)
    # newGame.startGame()
    game1 = Game(4, 'game1', 1, 'two', 1, Player, False, Player, 0, True)
    game1.startGame()

    output = sys.stdout.getvalue()
    # sys.stdout = orig_stdout
    await ctx.send(output)

client.run('NzY5MzM1Mjc2NjY0NzgyOTE4.X5NhTw.JDmc3an_0sSpaxoTayELuAXGNAo')

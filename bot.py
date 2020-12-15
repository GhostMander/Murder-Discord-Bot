import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

import random

load_dotenv()

client = commands.Bot(command_prefix = "m.", case_insensitive = True)
client.remove_command('help')


def knife_attack(attacked):
    attacked = random.choices([True, False], weights = [900, 100])
    if attacked:
        dmg = min(randint(10, 20), attacked.health)
        attacked.health -= dmg
        return True
    else:
        return False


def bow_attack(attacked):
    attacked = random.choices([True, False], weights = [600, 400])
    if attacked:
        dmg = min(randint(40, 50), attacked.health)
        attacked.health -= dmg
        return True
    else:
        return False


def gun_attack(attacked):
    attacked = random.choices([True, False], weights = [200, 800])
    if attacked:
        dmg = min(randint(90, 100), attacked.health)
        attacked.health -= dmg
        return True
    else:
        return False


class Dueler:
    def __init__(self, member: discord.Member):
        self.user = member
        self.health = 100

    @staticmethod
    def fight(weapon, opponent):
        if weapon == "knife":
            knife_attack(opponent)
        elif weapon == 'bow and arrow':
            bow_attack(opponent)
        elif weapon == 'gun':
            gun_attack(opponent)


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = 'murder'))
    print('Murder Ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Murder latency is {round(client.latency * 1000)}ms')


@client.command()
async def duel(ctx, member: discord.Member = None):
    if member is not None:
        weaponChoose = discord.Embed(
            title = f"Duel - __{ctx.author.display_name}__ against __{member.display_name}__",
            colour = discord.Colour(0x91a386),
            description = "Choose a Weapon to Fight!"
        )

        weaponChoose.set_author(
            name = f"{ctx.author}",
            icon_url = f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png"
        )

        weaponChoose.add_field(
            name = "🔪",
            value = "Knife! Melee Weapon that hits its mark almost every time!, but deals low damage!\nChance to hit  :  **90%**\nDamage Dealt :  **10 - 20**"
        )
        weaponChoose.add_field(
            name = "🏹",
            value = "Bow and Arrow! Ranged Weapon that has a mediocre chance to hit, and deals mediocre damage!\nChance to hit  :  **60%**\nDamage Dealt :  **40 - 50**"
        )
        weaponChoose.add_field(
            name = "🔫",
            value = "Gun! Ranged Weapon that has the highest damage, but recoil makes it miss a few times!\nChance to hit  :  **20%**\nDamage Dealt :  **90 - 100**"
        )

        chooseMsg = await ctx.send(embed = weaponChoose)

        weapon = []
        booleans = [False, False]

        await chooseMsg.add_reaction('🔪')
        await chooseMsg.add_reaction('🏹')
        await chooseMsg.add_reaction('🔫')

        def check(reaction, user):
            a = user == ctx.author
            b = str(reaction.emoji)
            c = user == member
            if a:
                if booleans[0]:
                    b = None
                if b == '🔪':
                    weapon.append((ctx.author.display_name, "Knife"))
                    booleans[0] = True
                elif b == '🏹':
                    weapon.append((ctx.author.display_name, "Bow and Arrow"))
                    booleans[0] = True
                elif b == '🔫':
                    weapon.append((ctx.author.display_name, "Gun"))
                    booleans[0] = True
            elif c:
                if booleans[1]:
                    b = None
                if b == '🔪':
                    weapon.append((member.display_name, "Knife"))
                    booleans[1] = True
                elif b == '🏹':
                    weapon.append((member.display_name, "Bow and Arrow"))
                    booleans[1] = True
                elif b == '🔫':
                    weapon.append((member.display_name, "Gun"))
                    booleans[1] = True
            return booleans[0] and booleans[1]

        try:
            reaction, user = await client.wait_for(event = 'reaction_add', timeout = 15.0, check = check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout. You took too long!')

        else:
               duelSim = discord.Embed(
                   title = f"Begin! - __{ctx.author.display_name}__ vs __{member.display_name}__",
                   colour = discord.Colour(0x91a386),
                   description = f"{weapon[0][0]} chose {weapon[0][1]} and {weapon[1][0]} chose {weapon[1][1]}"
               )

               duelSim.add_field(
                   name = f"__{ctx.author.display_name}__", inline=True,
                   value = "`health go brrr`"
                )

               duelSim.add_field(
                   name = f"__{member.display_name}__", inline=True,
                   value = "`health go brrr`"
               )

               duelSim.add_field(
                   name = "\u200b", inline=False,
                   value = "`bop`"
               )

               await ctx.send(embed = duelSim)

    else:
        await ctx.send("Mention a user to duel with.")


client.run(os.getenv('DISCORD_TOKEN'))

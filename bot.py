import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

import random

load_dotenv()

client = commands.Bot(command_prefix = "m.", case_insensitive = True)
client.remove_command('help')

async def reaction_remover(message):
    msg = await message.channel.fetch_message(message.id)
    for i in msg.reactions:
        l = await i.users().flatten()
        if len(l) == 1:
            continue
        for j in l:
            if j.id != 787288248094687252:
                await msg.remove_reaction(i.emoji, j)

def knife_attack(attacked):
    killed = random.choices([True, False], weights = [900, 100])[0]
    if killed:
        dmg = min([random.randint(10, 20), attacked.health])
        attacked.health -= dmg
        return dmg
    else:
        return 0


def bow_attack(attacked):
    killed = random.choices([True, False], weights = [600, 400])[0]
    if killed:
        dmg = min([random.randint(40, 50), attacked.health])
        attacked.health -= dmg
        return dmg
    else:
        return 0


def gun_attack(attacked):
    killed = random.choices([True, False], weights = [200, 800])[0]
    if killed:
        dmg = min([random.randint(90, 100), attacked.health])
        attacked.health -= dmg
        return dmg
    else:
        return 0


class Dueler:
    def __init__(self, member: discord.Member, weapon):
        self.user = member.display_name
        self.health = 100
        self.weapon = weapon

    def fight(self, opponent):
        if self.weapon.lower() == "knife":
            h_m = knife_attack(opponent)
        elif self.weapon.lower() == 'bow and arrow':
            h_m = bow_attack(opponent)
        elif self.weapon.lower() == 'gun':
            h_m = gun_attack(opponent)

        if not h_m:
            return f"*{self.user}* missed *{opponent.user}* While using {self.weapon}"
        return f"**{self.user}** hits **{opponent.user}** using {self.weapon} for a WHOPPING **{h_m}** Damage!"

    def healthBar(self):
        hearts = (self.health) // 10
        heartstr = "♥\u0020" * hearts
        deadstr = ('\u2661\u0020' * (10 - hearts)).strip("\u0020")
        return "`" + heartstr + deadstr + "`"

    def new_weapon(self, weapon):
        self.weapon = weapon


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = 'murder'))
    print('Murder Ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Murder latency is {round(client.latency * 1000)}ms')


@client.command()
async def quit(ctx):
    if ctx.author.id in [436973854485643264, 437491079869104138]:
        await ctx.send(f"As per the request of the Control Devil named {ctx.author.display_name}, I will murder myself.")
        await client.logout()


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
            icon_url = ctx.author.avatar_url
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

        weaponChoose.add_field(
            name = "\u3164", inline = False,
            value = "Choose the First Weapon for either Side. You have 15 seconds."
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

                if ctx.author in set([i[0] for i in weapon]):
                    if b in {'🔪', '🏹', '🔫'}:
                        for i in range(len(weapon)):
                            if weapon[i][0] == ctx.author:
                                weapon.pop(i)

                if b == '🔪':
                    weapon.append((ctx.author, "Knife"))
                    booleans[0] = True
                elif b == '🏹':
                    weapon.append((ctx.author, "Bow and Arrow"))
                    booleans[0] = True
                elif b == '🔫':
                    weapon.append((ctx.author, "Gun"))
                    booleans[0] = True

            elif c:
                if booleans[1]:
                    b = None

                if member in set([i[0] for i in weapon]):
                    if b in {'🔪', '🏹', '🔫'}:
                        for i in range(len(weapon)):
                            if weapon[i][0] == member:
                                weapon.pop(i)


                if b == '🔪':
                    weapon.append((member, "Knife"))
                    booleans[1] = True
                elif b == '🏹':
                    weapon.append((member, "Bow and Arrow"))
                    booleans[1] = True
                elif b == '🔫':
                    weapon.append((member, "Gun"))
                    booleans[1] = True
            return booleans[0] and booleans[1]

        try:
            reaction, user = await client.wait_for(event = 'reaction_add', timeout = 1.0, check = check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout. You took too long!')
            await reaction_remover(chooseMsg)
        else:
            for i, j in weapon:
                if i == ctx.author:
                    author = Dueler(i, j)
                elif i == member:
                    opponent = Dueler(i, j)

            await reaction_remover(chooseMsg)

            duelSim = discord.Embed(
                title = f"__{author.user}__ vs __{opponent.user}__",
                colour = discord.Colour(0x91a386),
                description = f"{author.user} chose **{author.weapon}** and {opponent.user} chose **{opponent.weapon}**"
            )

            duelSim.add_field(
                name = f"__{author.user} ({author.health}/100)__",
                value = author.healthBar()
            )

            duelSim.add_field(
                name = f"__{opponent.user} ({opponent.health}/100)__",
                value = opponent.healthBar()
            )

            duelSim.add_field(
                name = "\u200b", inline = False,
                value = author.fight(opponent)
            )

            duelSim.add_field(
                name = "\u200b", inline = False,
                value = opponent.fight(author)
            )

            await chooseMsg.edit(content = None, embed = duelSim)

    else:
        await ctx.send("Mention a user to duel with.")


client.run(os.getenv('DISCORD_TOKEN'))
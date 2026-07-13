import discord
import discord.colour
import asyncio
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import requests
from keep_alive import keep_alive
from flirts import flirts
from roles import roles, game_roles, rp_roles, special_roles

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

keep_alive()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = 'M', intents=intents, case_insensitive = True) #initializes bot

#Variables: 

purple = discord.Color.from_rgb(140, 0, 191)

bot.remove_command('help')

@bot.event
async def on_ready():
    print("Program Running")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the cult, {member.mention}. You can assign yourself server roles by typing 'MSurvey' and 'MGameRoles' in channels that have access to Mask-chan")

#Commands:

@bot.command()
async def askhelp(ctx):
    embed = discord.Embed(title = ":performing_arts: Mask Commands", color = purple, description = ("Mask-chan uses the 'M' prefix to accept commands.\n"
                                                                                    "* 1: MaskHelp - See a list of Mask-chan's usable commands.\n"
                                                                                    "* 2: MFlirt - 'MFlirt @userid' or 'MFlirt random' Mask-chan can flirt with a selected user.\n"
                                                                                    "* 3: MWeather - 'MWeather C/F/K' Checks the weather.\n"
                                                                                    "* 4: MSurvey - Administers the OFFICIAL, SUPER_SPECIAL, SERVER QUESTIONNAIRE™.\n"
                                                                                    "* 5: MGameRoles - Opt into receiving pings for specific video games.\n"
                                                                                    "* 6: MHMS - Challenge Mask-chan to Hamon-Masks-Spin. Try not to lose too often.\n"))
    help_menu = await ctx.send(embed = embed)

@bot.command()
async def Flirt(ctx, user: discord.Member):

    flirt_list = []

    flirt = random.choice(flirts)
    flirt_list.append(flirt)

    target = user or ctx.author
    if target == ctx.author:
        await ctx.send(f"I'm not here to get spicy with you, {ctx.author.display_name} :rolling_eyes:")
        await ctx.send(f"{target.mention} {flirt_list[0]}")
    elif target == bot.user:
        await ctx.send(f"I'd rather flirt with myself than you, {ctx.author.display_name}")
        await ctx.send(f"{target.mention} {flirt_list[0]}")
    elif target == user:
        await ctx.send(f"{target.mention} {flirt_list[0]}")
    else:
        await ctx.send(f"I can't find anyone to flirt with. Looks like I'm alone again ;(")

    flirt_list.clear()
    print(flirt_list)

@bot.command()
async def Weather(ctx, wtype = None):
    city = "Moab"
    api_key = os.getenv('WEATHER_API_KEY')
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature_K = data["main"]["temp"]
        temp_high_K = data["main"]["temp_max"]
        temp_low_K = data["main"]["temp_min"]
        feels_like_K = data["main"]["feels_like"]
        weather_description = data["weather"][0]["id"]

        temperature_C = (temperature_K - 273.15)
        feels_like_C = (feels_like_K - 273.15)
        temp_high_C = (temp_high_K - 273.15)
        temp_low_C = (temp_low_K - 273.15)

        temperature_F = ((temperature_C * (9/5)) + 32)
        feels_like_F = ((feels_like_C * (9/5)) + 32)
        temp_high_F = ((temp_high_C * (9/5)) + 32)
        temp_low_F = ((temp_low_C * (9/5)) + 32)

    else:
        print("An error occurred")

    if 200 <= weather_description <= 232: 
        weather_cond = "Looks like there's a heavy thunderstorm roaring through the skies :thunder_cloud_rain:. Stay safe!"
    elif 300 <= weather_description <= 321:
        weather_cond = "There's a light drizzle outside. I hear that's a good omen :white_sun_rain_cloud:."
    elif 500 <= weather_description <= 532: 
        weather_cond = "It's raining like CRAZY out there. My mask is erroding ;( :cloud_rain:."
    elif 600 <= weather_description <= 622: 
        weather_cond = "IT'S SNOWING :D. Time for a snowball fight! :snowman2:."
    elif weather_description == 701: 
        weather_cond = "There's a light mist in the air. :droplet:."
    elif weather_description == 721:
        weather_cond = "A thick haze fills the air. :purple_square: :fog:."
    elif weather_description == 711:
        weather_cond = "Mmm... Smells like a barbecue. WAIT, IT'S SMOKE! :fire::dash:."
    elif weather_description == 731 or weather_description == 751 or weather_description == 761:
        weather_cond = "*cough cough*, It's dust as far as the eye can see :desert::cloud_tornado:."
    elif weather_description == 741 or weather_description: 
        weather_cond = "It's foggy, I can barely see a thing :face_in_clouds:."
    elif weather_description == 762:
        weather_cond = "It finally burst. KRAKATOA! The skies are black with smoke and ash :volcano:."
    elif weather_description == 771:
        weather_cond = "squalls :dash:"
    elif weather_description == 781:
        weather_cond = "A tornado is tearing through the fields :cloud_tornado:."
    elif weather_description == 800:
        weather_cond = "Nothing but clear skies :sunglasses: :sunny:."
    elif 801 <= weather_description <= 805: 
        weather_cond = "The skies seem quite cloudy today :cloud:."
    else:
        weather_cond = "Buddy... You're not gonna believe this :flying_saucer:."


    if wtype == "K":
        await ctx.send(f"The temperature in Moab Utah is {temperature_K:.2f}°K, with a high of {temp_high_K:.2f}°F and a low of {temp_low_K:.2f}°F. It feels like {feels_like_K:.2f}°F.{weather_cond}")
    elif wtype == "C":
        await ctx.send(f"The temperature in Moab Utah is {temperature_C:.2f}°C, with a high of {temp_high_C:.2f}°F and a low of {temp_low_C:.2f}°F. It feels like {feels_like_C:.2f}°F. {weather_cond}")
    elif wtype == "F":
        await ctx.send(f"The temperature in Moab Utah is {temperature_F:.2f}°F, with a high of {temp_high_F:.2f}°F and a low of {temp_low_F:.2f}°F. It feels like {feels_like_F:.2f}°F. {weather_cond}")
    elif wtype == None:
        await ctx.send("Follow your command with either F for Farenheit, C for Celsius, or K for Kelvin")

@bot.command()
async def Survey(ctx):
    embed1 = discord.Embed(title = "Welcome to the OFFICIAL, SUPER-SPECIAL, SERVER QUESTIONNAIRE™", color = purple, description = "You will be asked a series of three 'yes/no' questions. Your answer to these questions determines your roles within the server. Each role has associated channels & pings. Are you ready?")
    embed2 = discord.Embed(title = "🪨 ROCK & STONE ⛏️", color = purple, description = "Do you play, or have you ever played, Deep Rock Galactic?\n(Both choices grant access to videogame-related channels)")
    embed3 = discord.Embed(title = "👺 ANIME 🏯", color = purple, description = "Would you like to be included in anime discussions and watch-alongs?")
    embed4 = discord.Embed(title = "🐲 ROLEPLAY GAMES 🎲", color = purple, description = "Would you like to be pinged for D&D / roleplay games? This role also grants access to supplamentary information, including D&D house rules.")
    embed_exit = discord.Embed(title = "EXITED SURVEY", color = purple, description = "You have opted out of completing the OFFICIAL, SUPER-SPECIAL, SERVER QUESTIONNAIRE™. Enjoy your day.")
    embed_complete = discord.Embed(title = "COMPLETE", color = purple, description = f"Congratulations, {ctx.author.display_name}. You have completed the OFFICIAL, SUPER-SPECIAL, SERVER QUESTIONNAIRE™. Feel free to retake the survey if you want to modify your roles.")

    role_S = discord.utils.get(ctx.guild.roles, name = roles[0])
    role_HS = discord.utils.get(ctx.guild.roles, name = roles[1])
    role_Ryu = discord.utils.get(ctx.guild.roles, name = roles[2])
    role_CI = discord.utils.get(ctx.guild.roles, name = roles[3])

    survey_reactions = ["✅", "❌"]

    try:
        poll_message = await ctx.send(embed = embed1) #Survey start

        await poll_message.add_reaction(survey_reactions[0])
        await poll_message.add_reaction(survey_reactions[1])

        #Read reactions for MSurvey
        def check_reaction(reaction, user):
            return (
            user == ctx.author
            and reaction.message.id == poll_message.id
            and str(reaction.emoji) in survey_reactions
            )

        reaction, user = await bot.wait_for("reaction_add", timeout = 60.0, check = check_reaction)

        if str(reaction.emoji) == survey_reactions[0]:
            print("check")

            poll_message2 = await ctx.send(embed = embed2) #Deep Rock Galactic

            await poll_message2.add_reaction(survey_reactions[0])
            await poll_message2.add_reaction(survey_reactions[1])

                #Read reactions for MSurvey
            def check_reaction2(reaction, user):
                return (
                user == ctx.author
                and reaction.message.id == poll_message2.id
                and str(reaction.emoji) in survey_reactions
                )

            reaction, user = await bot.wait_for("reaction_add", timeout = 60.0, check = check_reaction2)

            if str(reaction.emoji) == survey_reactions[0] and role_S and role_HS: #Need to make these commands give roles
                await ctx.author.remove_roles(role_HS)
                await ctx.author.add_roles(role_S)
                await ctx.send(f"You have received a role: '{role_S}'")

            elif str(reaction.emoji) == survey_reactions[1] and role_S and role_HS:
                await ctx.author.add_roles(role_HS)
                await ctx.author.remove_roles(role_S)
                await ctx.send(f"You have received a role: '{role_HS}'")

            elif str(reaction.emoji) == survey_reactions[1] and not role_HS:
                await ctx.send(f"The role '{roles[1]}' does not exist")

            elif str(reaction.emoji) == survey_reactions[1] and not role_S:
                await ctx.send(f"The role '{roles[0]}' does not exist")

            elif str(reaction.emoji) == survey_reactions[0] and not role_S:
                await ctx.send(f"The role '{roles[0]}' does not exist")

            elif str(reaction.emoji) == survey_reactions[0] and not role_HS:
                await ctx.send(f"The role '{roles[1]}' does not exist")

            poll_message3 = await ctx.send(embed = embed3) #Anime roles

            await poll_message3.add_reaction(survey_reactions[0])
            await poll_message3.add_reaction(survey_reactions[1])

            def check_reaction3(reaction, user):
                return (
                user == ctx.author
                and reaction.message.id == poll_message3.id
                and str(reaction.emoji) in survey_reactions
                )
        
            reaction, user = await bot.wait_for("reaction_add", timeout = 60.0, check = check_reaction3)

            if str(reaction.emoji) == survey_reactions[0] and role_Ryu:
                await ctx.author.add_roles(role_Ryu)
                await ctx.send(f"You have received a role: '{role_Ryu}'")

            elif str(reaction.emoji) == survey_reactions[1]:
                await ctx.author.remove_roles(role_Ryu)
                await ctx.send(f"You have removed a role: '{role_Ryu}'")

            poll_message4 = await ctx.send(embed = embed4) #Roleplay game roles

            await poll_message4.add_reaction(survey_reactions[0])
            await poll_message4.add_reaction(survey_reactions[1])

            def check_reaction4(reaction, user):
                return (
                user == ctx.author
                and reaction.message.id == poll_message4.id
                and str(reaction.emoji) in survey_reactions
                )
        
            reaction, user = await bot.wait_for("reaction_add", timeout = 60.0, check = check_reaction4)

            if str(reaction.emoji) == survey_reactions[0]:
                await ctx.author.add_roles(role_CI)
                await ctx.send(f"You have received a role: '{role_CI}'. This role will be activated when you participate in an active campaign.")

            elif str(reaction.emoji) == survey_reactions[1]:
                await ctx.author.remove_roles(role_CI)
                await ctx.send(f"You have removed a role: '{role_CI}'")

            poll_completed = await ctx.send(embed = embed_complete)
            return

        elif str(reaction.emoji) == survey_reactions[1]:
            print("cross")
            poll_exit = await ctx.send(embed = embed_exit)

    except asyncio.TimeoutError:
        poll_exit = await ctx.send(embed = embed_exit)
        await ctx.send(f"You took too long to react, {user.mention}. Session exited.")


@bot.command()
async def GameRoles(ctx):
    game_roles_embed = discord.Embed(title = "🎮 GAME ROLES", color = purple, description = ("While 'Game Roles' is active, a user can assign themselves roles to receive pings about specific video games.\n"
                                                                                          "Enter **the role** you would like to receive based on its associated games in the following list:\n"

                                                                                          "* **Sloppy Friends** - Gamble With Your Friends, PEAK, RV There Yet?, PICO PARK, FPS Chess, Supermarket Together, Cave Crawlers, Stumble Guys, Garry's Mod, Overcooked! 2.\n" 
                                                                                          "* **Cool Shooter** - Team Fortress 2, Splitgate, The Finals, Counter Strike.\n"
                                                                                          "* **Four Idiots** - Helldivers, Deep Rock Galactic, Risk of Rain 2, Risk of Rain Returns, Borderlands, Warhammer 40,000: Darktide, Warhammer: Vermintide 2.\n"
                                                                                          "* **Allay** - Minecraft.\n"
                                                                                          "* **Human-Eater** - Palworld, Sons Of The Forest, Muck, Abiotic Factor, Project Zomboid, Don't Starve Together, Unturned.\n"
                                                                                          "* **Mibles** - Marvel Rivals, Overwatch, Deadlock, Plants vs Zombies Garden Warfare.\n"
                                                                                          "* **Lethal Phobia** - Lethal Company, Phasmophobia, Content Warning, GTFO.\n"
                                                                                          "* **Heart of the Cards** - Tabletop Simulator, Magic: The Gathering, Yu-Gi-Oh!, Pokemon TCG, UNO.\n"
                                                                                          "* **Sea Thief** - Sea of Thieves, Pirate Fighting Simulator.\n"

                                                                                          "Roles are shared between several games due to genre similarities.\n"
                                                                                          "You don't need to own or be interested in *every* game within a role category - they simply reflect notification & gameplay preferences.\n"
                                                                                          "Game roles can be removed by following your comment with 'remove'\n"
                                                                                          "\n Role names are **Case-sensitive**. You need proper capitalization when referring to roles.\n"
                                                                                          "\n'Games Roles' can be exited by typing 'exit' or by waiting 60 seconds."))

    checking_roles = True

    await ctx.send(embed = game_roles_embed)

    def role_check(message):
        valid_items = []
        for role, games in game_roles.items():
            valid_items.append(role)
            valid_items.extend(games)

        return (message.author == ctx.author and
                message.channel == ctx.channel and
                (message.content in valid_items or
                message.content.lower() == "exit" or
                message.content.lower().endswith(" remove") and message.content[0:-7] in valid_items)
                )

    try:
        while checking_roles:
            role_select = (await bot.wait_for("message", timeout = 60.0, check = role_check)).content

            for role, games in game_roles.items():
                if role_select in games:
                    await ctx.send(f"'{role_select}' is a video game. Please type the role associated with that game.")
                    await ctx.send(f"'{role}' is the role associated with '{role_select}'")

            for role, games in game_roles.items():
                if role_select in role:
                    role_new = discord.utils.get(ctx.guild.roles, name = str(role_select))
                    if role_new not in ctx.author.roles:
                        await ctx.send(f"You have been assigned '{role_new}'")
                        await ctx.author.add_roles(role_new)
                    elif role_new in ctx.author.roles:
                        await ctx.send(f"{ctx.author.mention}, You already have '{role_new}'")

            for role, games in game_roles.items():
                if role_select.lower().endswith(" remove") and role_select[0:-7] == role:
                    role_new = discord.utils.get(ctx.guild.roles, name = str(role_select[0:-7]))
                    if role_new in ctx.author.roles:
                        await ctx.send(f"'{role_new}' has been removed from your server profile.")
                        await ctx.author.remove_roles(role_new)
                    elif role_new not in ctx.author.roles:
                        await ctx.send(f"{ctx.author.mention}, You do not have '{role_new}'")

            if role_select.lower() == "exit":
                await ctx.send(f"{ctx.author}, you have exited 'Game Roles'.")
                checking_roles = False
               
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to send a message, {ctx.author.mention}. Session exited")
        checking_roles = False

@bot.command()
async def HMS(ctx):
    embed_HMS = discord.Embed(title = "HAMON - MASKS - SPIN", color = purple, description = ("You are now playing Hamon-Masks-Spin. This is Mask-chan's version of rock paper scissors\n"
                                                                            "Hamon purifies vampires(masks),\n"
                                                                            "vampires(masks) infect spin-users,\n"
                                                                            "spin-users breach hamon's regeneration.\n"
                                                                            "Test Mask-chan's limits, and see how often you can win! Good luck >:D.\n"
                                                                            "\n* You can begin the program by typing hamon, masks, or spin. Mask-chan will respond"
                                                                            "\n* You can exit at any time by typing 'Araki', or by waiting 60 seconds."
                                                                            ))
    HMS_Choices_bot = ("Hamon", "Masks", "Spin")
    HMS_Choices_user = ("Hamon", "Masks", "Mask", "Spin", "Stand", "Araki")
    HMS_Choice_bot = []

    def HMS_Check(message):
        return (message.author == ctx.author and
         message.channel == ctx.channel and
         message.content.capitalize() in HMS_Choices_user
        )

    HMS_message = await ctx.send(embed = embed_HMS)

    HMS_score_bot = 0

    HMS_score_user = 0

    playing_HMS = True

    try:
        while playing_HMS:
            HMS_Random = random.choice(HMS_Choices_bot)
            HMS_Choice_bot.append(HMS_Random)

            HMS_Choice_user = (await bot.wait_for("message", timeout = 60.0, check = HMS_Check)).content

            await ctx.send(f"{HMS_Choice_bot[0]}")

            #Main event sequence. Long-ass if statement.
            if HMS_Choice_user.capitalize() == HMS_Choices_user[0]:
                if HMS_Choice_bot[0] == HMS_Choices_bot[0]:
                    await ctx.send("Our hamon streams used inverted polarity and cancelled each other out.")
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                elif HMS_Choice_bot[0] == HMS_Choices_bot[1]:
                    await ctx.send("NO! The force of your hamon is melting my flesh!\n*Hamon is antithetical to a vampire's existence.*")
                    HMS_score_user += 1
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                elif HMS_Choice_bot[0] == HMS_Choices_bot[2]:
                    await ctx.send("YOU FOOL! Spin is nature's ultimate weapon. Your puny bout of sunlight cannot hope counter my rotation.")
                    HMS_score_bot += 1
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")

            if HMS_Choice_user.capitalize() == HMS_Choices_user[1] or HMS_Choice_user.capitalize() == HMS_Choices_user[2]:
                if HMS_Choice_bot[0] == HMS_Choices_bot[0]:
                    await ctx.send("*The purifying waves of hamon wash across your decaying skin, evaporating your necrosis to ash*.\nYou can rest easy now, you poor soul.")
                    HMS_score_bot += 1
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                elif HMS_Choice_bot[0] == HMS_Choices_bot[1]:
                    await ctx.send("Two immortal beings, siphoning each others' blood, locked in brawl for all eternity.")
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                elif HMS_Choice_bot[0] == HMS_Choices_bot[2]:
                    await ctx.send("*You sprint towards Mask-chan in a bout of superhuman force. Mask-chan's flesh is frozen at your touch. The spinning ceases. You sink your fangs into her frail, defenseless neck.*")
                    HMS_score_user += 1
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")

            if HMS_Choice_user.capitalize() == HMS_Choices_user[3]:
                if HMS_Choice_bot[0] == HMS_Choices_bot[0]:
                    await ctx.send("AAH- I- I can't approach.\n*Mask-chan is stuck unable to close the distance as you salvo her with spinning projectiles*.")
                    HMS_score_user += 1
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                elif HMS_Choice_bot[0] == HMS_Choices_bot[1]:
                    await ctx.send("*Your spinning ball obliterates Mask-chan's left forearm. She briefly appreciates your powers before carving through your skull with a high-pressure fluid jet*")
                    HMS_score_bot += 1
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                elif HMS_Choice_bot[0] == HMS_Choices_bot[2]:
                    await ctx.send(f"*Impressed by your mastery of spin, Mask-chan extends her hand to offer a draw*.")
                    await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")

            if HMS_Choice_user.capitalize() == HMS_Choices_user[4]:
                await ctx.send("OH MY GOD! AN ENEMY STAND!\n*Before any further investigation can unfold, Mask-chan notices a fist-sized hole in her stomach and collapses*.")
                HMS_score_user += 1
                await ctx.send(f"(Current score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")

            if HMS_Choice_user.capitalize() == "Araki":
                await ctx.send("Wait, what were we doing? I completely forgot.")
                await ctx.send(f"(Final score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")
                playing_HMS = False
        
            HMS_Choice_bot.clear()

    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention} Your session timed out")
        await ctx.send(f"(Final score - {HMS_score_user} {ctx.author.display_name} : {HMS_score_bot} {bot.user.display_name})")


bot.run(token, log_handler = handler, log_level = logging.DEBUG)
from random import randint

from discord.ext import commands
from discord.ext.commands import Bot
from discord.file import File
from Config.config import Config
from embeds.command_embeds import CommandEmbeds
from embeds.help_embeds import HelpEmbeds
from time import sleep
import json
import re
import asyncio


# GET PREFIXES
def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(".")(client, message)

    with open("Config\\bot_prefixes.json", "r") as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(".")(client, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)


# PERMISSIONS
async def has_guild_permissions(ctx):
    check = False

    for roles in ctx.author.roles:
        if roles.permissions.administrator:
            check = True
    if ctx.author.id == ctx.guild.owner.id:
        check = True
    elif ctx.author.id == 204995313080074250:
        check = True

    return check


# INIT CLASSES
c = Config()
embeds = CommandEmbeds()
help_embeds = HelpEmbeds()


# BOT CONFIG
token = c.GetConfig("token")
client = Bot(command_prefix=get_prefix)
client.remove_command('help')


@client.event
async def on_ready():
    try:
        print("------------------------LOGIN-DETAILS------------------------")
        print("Logged in as " + client.user.name)
        print("Client User ID: " + str(client.user.id))
        print("Invite at: https://discordapp.com/oauth2/authorize?client_id=" + str(client.user.id)
              + "&permissions=51264&scope=bot")

    except Exception as e:
        print(e)


@client.command(pass_context=True)
@commands.check(has_guild_permissions)
async def setprefix(ctx, prefix):
    with open("Config\\bot_prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix
    await CommandEmbeds.update_command_embed(embeds, ctx, "Bot Prefix", prefix)

    with open("Config\\bot_prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.command(pass_context=True)
async def mad(ctx, story_name=None):
    with open("data\\stories.json", "r") as f:
        data = json.load(f)

    with open("data\\definitions.json", "r") as f:
        word_definitions = json.load(f)

    stories = data['stories']
    selected_story = None
    story_title = None
    m = None
    if story_name is None:
        random_index = randint(0, len(stories) - 1)
        selected_story = stories[random_index]
        m = re.findall('<(.+?)/>', selected_story['text'])
        story_title = selected_story['title']
    else:
        for story in stories:
            if story['title'].lower() == story_name.lower():
                selected_story = story
                story_title = selected_story['title']
                m = re.findall('<(.+?)/>', selected_story['text'])
    user_inputs = {}

    game_start_channel = ctx.channel.id

    if m:
        for word in m:
            words_def = word.split("::", 1)[1]
            for defs in word_definitions["definitions"]:
                if words_def == defs["desc"]:
                    definition_description = defs["type"]
            await ctx.channel.send(f"Enter a {definition_description}")
            sleep(2)
            try:
                def check(m):
                    if m.channel.id == game_start_channel and int(m.author.id) != 695050399316443186:
                        return m.content

                user_input_object = await client.wait_for('message', timeout=60.0, check=check)
                if user_input_object.channel.id == game_start_channel:
                    user_input = user_input_object.content
                    user_part = {word: user_input}
                    user_inputs.update(user_part)
            except asyncio.TimeoutError:
                    await ctx.channel.send("You took too long to respond, exiting.")

    story_array = selected_story['text'].split()
    output_story_array = []
    for word in story_array:
        word_concat = word.replace('<', '').replace('/>', '')
        output_story_array.append(word_concat)

    text = " ".join(output_story_array)

    for i, j in user_inputs.items():
        text = text.replace(i, f'**{j}**')

    await CommandEmbeds.story_output_embed(embeds, ctx, story_title, text)


@client.command(pass_context=True)
async def importlib(ctx):
    with open("data\\stories.json", "r") as f:
        data = json.load(f)

    with open("data\\definitions.json", "r") as f:
        word_definitions = json.load(f)

    if len(ctx.message.attachments) > 1:
        await ctx.channel.send("You've uploaded too many documents")
    elif len(ctx.message.attachments) == 0:
        await ctx.channel.send("You must attach a .txt file")

    else:
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.txt'):
            await ctx.channel.send("Your upload must be a .txt file")
            return

        attachment_bytes = await attachment.read()
        attachment_string = attachment_bytes.decode("utf-8")

        # Find all definitions in file and add them to def list if they don't exist
        m = re.findall('<(.+?)/>', attachment_string)
        if m:
            for word in m:
                if "::" in word:
                    def_found = False
                    words_def = word.split("::", 1)[1]
                    for definitions in word_definitions['definitions']:
                        if words_def == definitions['desc']:
                            def_found = True
                    if not def_found:
                        definitions = word_definitions["definitions"]
                        await ctx.channel.send(f"Please enter a type for '{word.split('::', 1)[1]}'")
                        user_input_object = await client.wait_for('message', timeout=60.0)
                        new_definition = {"desc": word.split('::', 1)[1], "type": user_input_object.content}
                        definitions.append(new_definition)

                        with open("data\\definitions.json", "w") as f:
                            json.dump(word_definitions, f, indent=4)
                else:
                    await ctx.channel.send(f"You have a definition typo for {word}. Please try upload again")
                    break

        # Add story to stories.json
        await ctx.channel.send(f"Please enter a title for this story")
        title_input = await client.wait_for('message', timeout=60.0)
        story_title = title_input.content

        stories = data["stories"]
        new_story = {"title": story_title, "text": attachment_string}
        stories.append(new_story)

        with open("data\\stories.json", "w") as f:
            json.dump(data, f, indent=4)

        await CommandEmbeds.story_add_embed(embeds, ctx, story_title)


@client.command(pass_context=True)
async def getdefinitions(ctx):
    with open("data\\definitions.json", "r") as f:
        word_definitions = json.load(f)

    await CommandEmbeds.definitions_embed(embeds, ctx, word_definitions['definitions'])


@client.command(pass_context=True)
async def adddefinition(ctx, code, type):
    with open("data\\definitions.json", "r") as f:
        word_definitions = json.load(f)

    definitions = word_definitions["definitions"]
    create_def = True
    for defs in definitions:
        if defs['desc'] == code:
            await ctx.channel.send(f"{code} has already been used as a definition. Please choose a new word type code.")
            create_def = False
            break
    if create_def:
        new_definition = {"desc": str(code), "type": str(type)}
        definitions.append(new_definition)

        with open("data\\definitions.json", "w") as f:
            json.dump(word_definitions, f, indent=4)

        await CommandEmbeds.add_command_embed(embeds, ctx, "Word Definition", code, type)


@client.command(pass_context=True)
async def importexample(ctx):
    prefix = get_prefix(client, ctx.message)
    file = File("example_story_import.txt", filename="example_story_import.txt")
    await ctx.channel.send(f"Here is an example story text file that you can import into the database. Make sure you "
                           f"run the `{prefix[2]}getdefinitions` command to see a list of the word definitions.",
                           file=file)


@client.command(pass_context=True)
async def availablestories(ctx):
    with open("data\\stories.json", "r") as f:
        data = json.load(f)

    await CommandEmbeds.stories_embed(embeds, ctx, data['stories'])


# HELP COMMANDS
@client.command(pass_context=True)
async def help(ctx, help_type=''):
    prefix = get_prefix(client, ctx.message)
    if help_type == '':
        await HelpEmbeds.get_help(help_embeds, ctx, prefix[2])
    if help_type.lower() == 'mad':
        await HelpEmbeds.help_mad_command(help_embeds, ctx, prefix[2])
    if help_type.lower() == 'importlib':
        await HelpEmbeds.help_importlib_command(help_embeds, ctx, prefix[2])
    if help_type.lower() == 'adddefinition':
        await HelpEmbeds.help_adddefinition_command(help_embeds, ctx, prefix[2])
    if help_type.lower() == 'getdefinitions':
        await HelpEmbeds.help_getdefinitions_command(help_embeds, ctx, prefix[2])
    if help_type.lower() == 'importexample':
        await HelpEmbeds.help_getdefinitions_command(help_embeds, ctx, prefix[2])
    if help_type.lower() == 'availablestories':
        await HelpEmbeds.help_availablestories_command(help_embeds, ctx, prefix[2])


client.run(token, bot=True, reconnect=True)

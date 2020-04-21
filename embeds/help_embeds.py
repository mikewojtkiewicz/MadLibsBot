import json
from discord.colour import Colour
from discord.embeds import Embed


class HelpEmbeds:
    async def get_help(self, ctx, prefix):
        embed = Embed(title="Available Commands", colour=Colour(0x6262e),
                      description="For more specific command help use `" + str(prefix) + "help [command]`")
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_author(name="Mad Libs Bot", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Game Commands:", value="mad", inline=True)
        embed.add_field(name="Config Commands:", value="adddefinition\ngetdefinitions\nimportlib\nimportexample",
                        inline=True)

        await ctx.channel.send(embed=embed)

    async def help_mad_command(self, ctx, prefix):
        embed = Embed(title="mad", colour=Colour(0x6262e),
                      description="Starts a Mad Libs Game. Can use story name in quotes as an optional parameter")

        embed.set_author(name="mad Command Help", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Usage", value="`" + str(prefix) + "mad 'story_name'`", inline=False)
        embed.add_field(name="Example", value="`" + str(prefix) + "mad 'Batman'`", inline=False)

        await ctx.channel.send(embed=embed)

    async def help_importlib_command(self, ctx, prefix):
        embed = Embed(title="importlib", colour=Colour(0x6262e),
                      description="Imports a story from a text file. You must upload the text file as an "
                                  "attachment to the command message in order for the upload to work.")

        embed.set_author(name="importlib Command Help", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Usage", value="`" + str(prefix) + "importlib`", inline=False)
        embed.add_field(name="Example", value="`" + str(prefix) + "importlib`", inline=False)

        await ctx.channel.send(embed=embed)

    async def help_adddefinition_command(self, ctx, prefix):
        embed = Embed(title="adddefinition", colour=Colour(0x6262e),
                      description="Adds a word definition to the database so that it can be used in an uploaded story")

        embed.set_author(name="adddefinition Command Help", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Usage", value="`" + str(prefix) + "adddefinition '{code{' '{word type description}'`",
                        inline=False)
        embed.add_field(name="Example", value="`" + str(prefix) + "adddefinition 'jj' 'Adjective'`", inline=False)

        await ctx.channel.send(embed=embed)

    async def help_getdefinitions_command(self, ctx, prefix):
        embed = Embed(title="getdefinitions", colour=Colour(0x6262e),
                      description="Responds with a list of the word definitions currently in use")

        embed.set_author(name="getdefinitions Command Help", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Usage", value="`" + str(prefix) + "getdefinitions`", inline=False)
        embed.add_field(name="Example", value="`" + str(prefix) + "getdefinitions`", inline=False)

        await ctx.channel.send(embed=embed)

    async def help_importexample_command(self, ctx, prefix):
        embed = Embed(title="importexample", colour=Colour(0x6262e),
                      description="Responds with an example import text file you can use to import into the "
                                  "story database")

        embed.set_author(name="importexample Command Help", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Usage", value="`" + str(prefix) + "importexample`", inline=False)
        embed.add_field(name="Example", value="`" + str(prefix) + "importexample`", inline=False)

        await ctx.channel.send(embed=embed)

    async def help_availablestories_command(self, ctx, prefix):
        embed = Embed(title="availablestories", colour=Colour(0x6262e),
                      description="Responds with a list of available story titles you can call directly")

        embed.set_author(name="availablestories Command Help", url="https://discord.gg/sJHwV8R",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Usage", value="`" + str(prefix) + "availablestories`", inline=False)
        embed.add_field(name="Example", value="`" + str(prefix) + "availablestories`", inline=False)

        await ctx.channel.send(embed=embed)

import json
from discord.colour import Colour
from discord.embeds import Embed


class CommandEmbeds:
    async def update_command_embed(self, ctx, update_type, update_value):
        embed = Embed(title="Action Complete", colour=Colour(0x6262e))

        embed.add_field(name="Updated " + str(update_type), value=str(update_type) + " set to " + str(update_value),
                        inline=True)

        await ctx.channel.send(embed=embed)

    async def add_command_embed(self, ctx, add_type, add_key, add_value):
        embed = Embed(title="Action Complete", colour=Colour(0x6262e))

        embed.add_field(name="Added New " + str(add_type), value=str(add_key) + " added and set to " + str(add_value),
                        inline=True)

        await ctx.channel.send(embed=embed)

    async def story_output_embed(self, ctx, title, story):
        embed = Embed(title="Mad Lib Story", colour=Colour(0x6262e))
        embed.add_field(name=title, value=story)

        await ctx.channel.send(embed=embed)

    async def story_add_embed(self, ctx, title):
        embed = Embed(title="Mad Lib Story Added", colour=Colour(0x6262e))
        embed.add_field(name="Story Name", value=title)
        embed.add_field(name="Added By", value=ctx.message.author)

        await ctx.channel.send(embed=embed)

    async def definitions_embed(self, ctx, definitions):
        embed = Embed(title="Mad Lib Definitions", colour=Colour(0x6262e))
        embed.add_field(name="How do I use these definitions?",
                        value="When uploading a story to the database, use the following definitions. For instance "
                              "if you wanted to have the bot ask for a noun, in your story use `<example::nn/>`. "
                              "Example being an example word that a user might choose.",
                        inline=False)
        for defs in definitions:
            embed.add_field(name=str(defs['type']), value=f"<example::{defs['desc']}/>")

        await ctx.channel.send(embed=embed)

    async def stories_embed(self, ctx, stories):
        embed = Embed(title="Mad Lib Available Stories", colour=Colour(0x6262e))
        available_stories = ""
        for story in stories:
            available_stories += f"{str(story['title'])}\n"

        embed.add_field(name="Available Story Titles", value=available_stories)

        await ctx.channel.send(embed=embed)

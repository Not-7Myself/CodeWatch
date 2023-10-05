import discord
from discord.ext import commands
import asyncio
import random
import os

token = os.environ["token"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents = intents)


motivational_quotes = ["*Believe in yourself!*", "*Stay Positive, work hard.*", "*Never stop learning.*"]

reminders = {}

@bot.command()
async def reminder(ctx, minutes : int, *, reminder : str):
    user_reminders = reminders.get(ctx.author.id, [])
    user_reminders.append((reminder, minutes))
    reminders[ctx.author.id] = user_reminders
    await ctx.send(f"Reminder set! We will remind you to {reminder} in {minutes} minutes.")
    await asyncio.sleep(minutes * 60)

    if (reminder, minutes) in reminders[ctx.author.id]:
        quote = random.choice(motivational_quotes)
        embed = discord.Embed(title="Reminder for your task:", description=f"**{reminder}**\n\n{quote}", color=discord.Colour.from_rgb(137,106,154))
        embed.set_footer(text="CodeWatch: www.example1.com | VSCode Extension: www.example2.com")
        await ctx.send(content=f'{ctx.author.mention}', embed=embed)

@bot.command()
async def delreminder(ctx, reminder : str):
    user_reminders = reminders.get(ctx.author.id, [])

    for rem in user_reminders:
        if rem[0] == reminder:
            user_reminders.remove(rem)
            await ctx.send("Your reminder was successfully deleted.")
            return

    await ctx.send("No such reminder found.")

@bot.command()
async def guide(ctx):
    guide_embed = discord.Embed(title="Usage Guide", color=discord.Colour.red())
    guide_embed.add_field(name="!reminder {minutes} {reminder message}",
                          value="This command sets a reminder. Replace {minutes} with how long to wait until reminding you and {reminder message} with your reminder.",
                          inline=False)
    guide_embed.add_field(name="!delreminder {reminder message}",
                          value="This command deletes an active reminder. Replace {reminder message} with the reminder you want to delete.",
                          inline=False)
    await ctx.send(embed=guide_embed)
  
bot.run(token)

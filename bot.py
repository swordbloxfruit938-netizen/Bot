import discord
from discord.ext import commands
import openai
import os

# Clé OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Intents Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    # Ignore les bots
    if message.author.bot:
        return

    # Si le bot est mentionné
    if bot.user in message.mentions:
        user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if not user_message:
            await message.channel.send("👋 Dis-moi quelque chose.")
            return

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es une IA Discord amicale, claire et utile. Réponds en français."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("❌ Erreur IA.")
            print(e)

    await bot.process_commands(message)

# Lancement du bot
bot.run(os.getenv("DISCORD_TOKEN"))
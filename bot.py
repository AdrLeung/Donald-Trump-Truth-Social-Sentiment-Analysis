import discord
import asyncio
from truthbrush.api import Api
from dotenv import load_dotenv
import os
from random import randint
import re

load_dotenv("secret.env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

TRUTH_USERNAME = "realDonaldTrump"

api = Api()
last_post_id = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_sentiment(content):
    return "stub"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(check_for_new_truths())

async def check_for_new_truths():
    global last_post_id
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("Could not find the specified channel.")
        return

    while not client.is_closed():
        try:
            posts = list(api.pull_statuses(TRUTH_USERNAME))
            if posts:
                latest_post = posts[0]
                if latest_post["id"] != last_post_id:
                    sentiment = get_sentiment(re.sub(r'<[^>]+>', '', latest_post["content"]).strip())
                    embed = discord.Embed(title = "New Post!", url = latest_post["url"], description = re.sub(r'<[^>]+>', '', latest_post["content"]).strip())
                    embed.set_author(name = "Donald J. Trump", url = "https://truthsocial.com/@realDonaldTrump")
                    embed.add_field(name = "Sentiment Analysis", value = sentiment, inline = False)
                    embed.add_field(name = "Summary", value = "Buy")

                    await channel.send(embed=embed)

                    print(f"Posted new Truth: {latest_post['url']}")
                    last_post_id = latest_post["id"]
                else:
                    print("No new post.")
        except Exception as e:
            print(f"Error fetching post: {e}")

        await asyncio.sleep(randint(300, 600))

client.run(DISCORD_TOKEN)
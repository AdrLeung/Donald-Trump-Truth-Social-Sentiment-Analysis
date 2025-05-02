import discord
import asyncio
from truthbrush.api import Api
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv("secret.env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

TRUTH_USERNAME = "realDonaldTrump"
CHECK_INTERVAL = 60

api = Api()
last_post_id = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
                    await channel.send(latest_post["url"])
                    print(f"Posted new Truth: {latest_post['url']}")
                    last_post_id = latest_post["id"]
                else:
                    print("No new post.")
        except Exception as e:
            print(f"Error fetching post: {e}")

        await asyncio.sleep(CHECK_INTERVAL)

client.run(DISCORD_TOKEN)
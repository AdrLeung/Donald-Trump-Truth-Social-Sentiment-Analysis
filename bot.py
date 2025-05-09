import discord
import asyncio
from truthbrush.api import Api
from dotenv import load_dotenv
import os
from random import randint
import re
import openai

load_dotenv("secret.env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

TRUTH_USERNAME = "realDonaldTrump"

openai.api_key = os.getenv("OPENAI_KEY")
api = Api()

last_post_id = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# helper function for check_for_new_truths() that generates the sentiment analysis by making an api request to openai
def get_sentiment(content):
    if re.sub('[^A-Za-z0-9 ]+', '', content) == "":
        return "Unable to generate sentiment for images or videos, please check the post manually."
    else:
        response = openai.responses.create(
            model = "gpt-4.1",
            instructions = 
            """You are a financial analyst.
            Given a social media post determine how the post might influence market sentiment on the S&P 500.
            Consider if the post aligns with or opposes recent trends.
            Use recent news to support your analysis and final decision.
            If the post is not related to the stock market, economy, companies, or macroeconomic indicators, return Neutral.
            Respond with:
            Positive, Neutral, or Negative

            Short explanation, max 3 sentences""",
            input = content,
            temperature = 0.1,
            max_output_tokens = 120
        )

        return response.output_text
    

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
                    content = re.sub(r'<[^>]+>', '', latest_post["content"]).strip()
                    sentiment = await asyncio.to_thread(get_sentiment, content)
                    embed = discord.Embed(title = "New Post!", url = latest_post["url"], description = re.sub(r'<[^>]+>', '', latest_post["content"]).strip())
                    embed.set_author(name = "Donald J. Trump", url = "https://truthsocial.com/@realDonaldTrump")
                    embed.add_field(name = "Sentiment Analysis", value = sentiment, inline = False)

                    await channel.send(embed=embed)

                    print(f"Posted new Truth: {latest_post['url']}")
                    last_post_id = latest_post["id"]
                else:
                    print("No new post.")
        except Exception as e:
            print(f"Error fetching post: {e}")

        await asyncio.sleep(randint(300, 600))

client.run(DISCORD_TOKEN)
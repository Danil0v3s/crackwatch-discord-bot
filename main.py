import asyncpraw, discord, os, asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

reddit_client_id = os.environ.get("reddit_client_id")
reddit_client_secret = os.environ.get("reddit_client_secret")

discord_client_key = os.environ.get("discord_client_key")
discord_channel_id = int(os.environ.get("discord_channel_id"))

started_at = datetime.utcnow().timestamp()
discord_client = discord.Client()

async def send_submission(submission, channel):
    embed = discord.Embed()
    embed.set_thumbnail(
        url="https://www.redditstatic.com/desktop2x/img/favicon/ms-icon-144x144.png"
    )
    embed.title = submission.link_flair_text
    embed.description = submission.title
    embed.set_footer(
        text=datetime.utcfromtimestamp(submission.created_utc).strftime(
            "%d-%m-%Y %H:%M"
        )
    )
    embed.url = f"https://reddit.com{submission.permalink}"

    try:
        images = submission.preview["images"]
        if len(images) > 0:
            embed.set_image(url=images[0]["source"]["url"])
    except Exception as e:
        print(e)

    await channel.send(embed=embed)

@discord_client.event
async def on_ready():
    print("connected to channel")

    reddit = asyncpraw.Reddit(
        client_id = reddit_client_id,
        client_secret = reddit_client_secret,
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    )
    channel = discord_client.get_channel(discord_channel_id)

    subreddit = await reddit.subreddit("CrackWatch")
    while not discord_client.is_closed():
        async for submission in subreddit.stream.submissions():
            if (submission.link_flair_text == "Release" or submission.link_flair_text == "New Game Repack") and submission.created_utc >= started_at:
                print("new submission, sending...")
                await send_submission(submission, channel)

def init():
    print("Connecting...")
    discord_client.run(discord_client_key)

if __name__ == "__main__":
   init()
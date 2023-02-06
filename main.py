import praw, discord, os
from datetime import datetime

reddit_client_id = os.environ.get("reddit_client_id")
reddit_client_secret = os.environ.get("reddit_client_secret")

discord_client_key = os.environ.get("discord_client_key")
discord_channel_id = os.environ.get("discord_channel_id")

started_at = datetime.utcnow().timestamp()

r = praw.Reddit(
    client_id = reddit_client_id,
    client_secret = reddit_client_secret,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    check_for_async=False,
)

client = discord.Client()

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

@client.event
async def on_ready():
    channel = client.get_channel(discord_channel_id)

    page = r.subreddit("CrackWatch").stream.submissions()
    for post in page:
        flair = post.link_flair_text
        if (
            flair == "Release" or flair == "New Game Repack"
        ) and post.created_utc >= started_at:
            await send_submission(post, channel)

if __name__ == "__main__":
    print("Connecting")
    client.run(discord_client_key)

import praw, discord, os
from datetime import datetime

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
client_key = os.environ.get("client_key")
started_at = datetime.utcnow().timestamp()

print(client_id, client_secret, client_key)

r = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    check_for_async=False,
)


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


client = discord.Client()


@client.event
async def on_ready():
    channel = client.get_channel(851958776168841246)

    await channel.send("Connected")

    page = r.subreddit("CrackWatch").stream.submissions()
    for post in page:
        flair = post.link_flair_text
        if (
            flair == "Release" or flair == "New Game Repack"
        ) and post.created_utc >= started_at:
            await send_submission(post, channel)

if __name__ == "__main__":
    print("Connecting")
    client.run(client_key)
